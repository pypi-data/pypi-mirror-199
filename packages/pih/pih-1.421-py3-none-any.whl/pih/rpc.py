from collections import defaultdict
from copy import copy
from dataclasses import dataclass
from datetime import datetime, timedelta
import importlib.util
import sys
import threading
from typing import Any, Callable, Tuple, List
import grpc
from concurrent import futures

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")
from pih.collection import ServiceRoleInformation, ServiceRoleDescription
from pih.rpc_collection import Subscriber, Subscribtion
from pih.tools import DataTool, EnumTool, ParameterList, BitMask as BM
from pih.const import CONST, ServiceCommands, ServiceRoles, SubscribtionTypes
import pih.rpcCommandCall_pb2_grpc as pb2_grpc
import pih.rpcCommandCall_pb2 as pb2

@dataclass
class Error(BaseException):
    details: str
    code: Tuple

@dataclass
class RoleStub:
    name: str = "stub"

class RPC:

    class SESSION:

        start_time: datetime
        life_time: timedelta

    @staticmethod
    def create_error(context, message: str = "", code: Any = None) -> Any:
        context.set_details(message)
        context.set_code(code)
        return pb2.rpcCommandResult()

    class UnaryService(pb2_grpc.UnaryServicer):

        def __init__(self, role: ServiceRoles, handler: Callable, *args, **kwargs):
            self.role = role
            self.handler = handler
            #[ServiceCommands, dict[ServiceRoles]]
            self.subscriber_map: dict = defaultdict(dict)

        def internal_handler(self, command_name: str, parameters: str, context) -> Any:
            try:
                print(f"rpc call: {command_name} {parameters}")
                command: ServiceCommands = EnumTool.get(ServiceCommands, command_name)
                parameter_list: ParameterList = ParameterList(parameters)
                if command is not None:
                    if command == ServiceCommands.ping:
                        service_role_info: dict = copy(DataTool.to_data(self.role.value))
                        service_role_info["subscribers"] = self.get_subscriber_list()
                        del service_role_info["modules"]
                        del service_role_info["commands"]
                        return service_role_info
                    elif command == ServiceCommands.subscribe:
                        return self.subscribe(parameter_list)
                    elif command == ServiceCommands.unsubscribe_all:
                        self.unsubscribe_all()
                        return True
                    elif command == ServiceCommands.heat_beat:
                        date_string: str = parameter_list.get()
                        date: datetime = datetime.strptime(
                            date_string, CONST.DATE_TIME_FORMAT)
                        parameter_list.set(0, date)
                        RPC.SESSION.life_time = date - RPC.SESSION.start_time
                result: Any = self.handler(command_name, self.call_subscribers_before(command, parameter_list), context)
                self.call_subscribers_after(command, parameter_list, result)
                return result
            except Exception as error:
                A = sys.modules["pih.pih"].A
                A.E.global_except_hook(type(error), error, error.__traceback__)
           
        def get_subscriber_list(self) -> dict:
            subscriber_list: list[Subscriber] = []
            for service_command in self.subscriber_map:
                for role_item in self.subscriber_map[service_command]:
                    subscriber_list.append(self.subscriber_map[service_command][role_item])
            return subscriber_list

        def unsubscribe_all(self) -> None:
            def unsubscribe_all_internal() -> None:
                for service_command in self.subscriber_map:
                    for role_item in self.subscriber_map[service_command]:
                        subscriber: Subscriber = self.subscriber_map[service_command][role_item]
                        DataTool.rpc_unrepresent(RPC.internal_call(
                            subscriber.role, ServiceCommands.unsubscribe, (service_command, subscriber.name)))
                self.subscriber_map = {}
            threading.Thread(target=unsubscribe_all_internal).start()
            
        def subscribe(self, parameter_list: ParameterList) -> bool:
            role: ServiceRoles = EnumTool.get(
                ServiceRoles, parameter_list.next())
            service_command: ServiceCommands = EnumTool.get(
                ServiceCommands, parameter_list.next())
            type: int = parameter_list.next()
            name: str = parameter_list.next()
            if service_command in self.subscriber_map:
                if role in self.subscriber_map[service_command]:
                    subscriber: Subscriber = self.subscriber_map[service_command][role]
                    if subscriber.role == role and (subscriber.type & type) != 0:
                        self.subscriber_map[service_command][role].enabled = True
                else:
                    self.subscriber_map[service_command][role] = Subscriber(
                        role, type, name)
            else:
                self.subscriber_map[service_command][role] = Subscriber(role, type, name)
            return True

        def call_subscribers_before(self, service_command: ServiceCommands, in_result: ParameterList):
            out_result: ParameterList = in_result
            if service_command in self.subscriber_map:
                for role_item in self.subscriber_map[service_command]:
                    subscriber: Subscriber = self.subscriber_map[service_command][role_item]
                    role: ServiceRoles = subscriber.role
                    if (subscriber.type & SubscribtionTypes.BEFORE) != 0 and subscriber.enabled:
                        subscriber.available = RPC.check_availability(role)
                        if subscriber.available:
                            out_result = ParameterList(DataTool.rpc_unrepresent(RPC.internal_call(
                                role, service_command, in_result)))
                        else:
                            service_role_value: ServiceRoleDescription = role.value
                            if service_role_value.weak_subscribtion:
                                subscriber.enabled = False
            return out_result

        def call_subscribers_after(self, service_command: ServiceCommands, parameter_list: ParameterList, result: Any) -> None:
            def call_subscribers_after_internal():
              if service_command in self.subscriber_map:
                    for role_item in list(self.subscriber_map[service_command]):
                        subscriber: Subscriber = self.subscriber_map[service_command][role_item]
                        if (subscriber.type & SubscribtionTypes.AFTER) != 0 and subscriber.enabled:
                            role: ServiceRoles = subscriber.role
                            subscriber.available = RPC.check_availability(role)
                            if subscriber.available:
                                RPC.internal_call(role, service_command, (result, parameter_list))
                            else:
                                service_role_value: ServiceRoleDescription = role.value
                                if service_role_value.weak_subscribtion:
                                    subscriber.enabled = False
            threading.Thread(target=call_subscribers_after_internal).start()

        def rpcCallCommand(self, command, context):
            parameters = command.parameters
            if not DataTool.is_empty(parameters):
                parameters = DataTool.rpc_unrepresent(parameters)
            result: Any = self.internal_handler(command.name, parameters, context)
            if context.code() is None:
                return pb2.rpcCommandResult(data=DataTool.rpc_represent(result))
            return result

    class Service:

        MAX_WORKERS: int = 10
        role: ServiceRoles = None
        #[ServiceRoles, List[Subscribtion]]
        subscribtion_map: dict = defaultdict(dict)


        @staticmethod
        def serve(role: ServiceRoles, call_handler: Callable, isolate: bool = False, service_started_handler: Callable[[None], None] = None, depends_on_list: List[ServiceRoles] = [], max_workers=MAX_WORKERS) -> None:
            from pih import A
            from pih import while_not_do
            A.O.init()
            A.SRV.init()
            RPC.Service.role = role
            service_role_value: ServiceRoleDescription = role.value
            isolate_arg: str = A.SE.arg(1, None)
            if isolate_arg is not None:
                isolate = isolate_arg.lower() in ["true", "1", "yes"]
            service_role_value.isolated = isolate
            service_host: str = A.SRV.get_host(role)
            service_port: int = A.SRV.get_port(role)
            service_role_value.pih_version = A.V.local()
            service_role_value.pid = A.OS.get_pid()
            A.O.service_header(role)
            A.O.good(f"Сервис был запущен!")
            server = grpc.server(
                futures.ThreadPoolExecutor(max_workers=max_workers))
            pb2_grpc.add_UnaryServicer_to_server(
                RPC.UnaryService(role, call_handler), server)
            try:
                server.add_insecure_port(f"{service_host}:{service_port}") 
                RPC.SESSION.start_time = datetime.now().replace(second=0, microsecond=0)
                server.start() 
                A.L_C.service_starts(role)
                if not DataTool.is_empty(depends_on_list):
                    A.O.write_line("Dependency availability check...")
                    while_not_do(lambda: len(list(filter(lambda item: A.SRV.check_accessibility(item), depends_on_list))) == len(depends_on_list), sleep_time=1)
                    A.O.write_line("All dependencies online")
                if service_started_handler is not None:
                    service_started_handler()
                RPC.Service.create_subscribtions() 
                A.L_C.service_started(role)
                server.wait_for_termination()
            except RuntimeError as error:
                A.L_C.service_not_started(role, "".join(error.args))

        @staticmethod
        def create_subscribtions() -> None:
            def create_subscribtions_internal() -> None:
                subscribtion_map: dict = RPC.Service.subscribtion_map
                for role in subscribtion_map:
                    if RPC.check_availability(role):
                        for service_command in subscribtion_map[role]:
                            subscribtion: Subscribtion = subscribtion_map[role][service_command]
                            if not subscribtion.actiated:
                                if DataTool.rpc_unrepresent(RPC.internal_call(role, ServiceCommands.subscribe, (RPC.Service.role, subscribtion.service_command, subscribtion.type, subscribtion.name))):
                                    subscribtion.actiated = True
                    else:
                        pass
            threading.Thread(target=create_subscribtions_internal).start()


        @staticmethod
        def subscribe_on(service_command: ServiceCommands, type: int = SubscribtionTypes.AFTER, name: str = None) -> bool:
            service_role: ServiceRoles = RPC.Service.role
            service_role_value: ServiceRoleDescription = service_role.value
            if service_role is not None:
                if not service_role_value.isolated:
                    from pih.pih import A
                    subscriber_service_role: ServiceRoles = A.SRV.get_role_by_command(
                        service_command)
                    if subscriber_service_role is not None:
                        if subscriber_service_role != service_role:
                            subscribtion_map: dict = RPC.Service.subscribtion_map
                            if service_command not in subscribtion_map[subscriber_service_role]:
                                subscribtion_map[subscriber_service_role][service_command] = Subscribtion(service_command, type, name)
                            else:
                                subscribtion: Subscribtion = subscribtion_map[subscriber_service_role][service_command]
                                subscribtion.enabled = True
                                subscribtion.type |= type
                            return True
            return False

        @staticmethod
        def unsubscribe(role: ServiceRoles, service_command: ServiceCommands = None, type: int = None) -> bool:
            pass

        @staticmethod
        def unsubscribe_all(role: ServiceRoles) -> bool:
            return RPC.Service.unsubscribe(role)

    class CommandClient():

        def __init__(self, host: str, port: int):
            self.stub = pb2_grpc.UnaryStub(grpc.insecure_channel(f"{host}:{port}"))

        def call_command(self, name: str, parameters: str = None, timeout: int = None):
            return self.stub.rpcCallCommand(pb2.rpcCommand(name=name, parameters=parameters), timeout=timeout)

    @staticmethod
    def ping(role: ServiceRoles) -> ServiceRoleInformation:
        try:
            return DataTool.fill_data_from_rpc_str(ServiceRoleInformation(), RPC.internal_call(role, ServiceCommands.ping, ((RPC.Service.role or RoleStub()).name), ))
        except Error:
            return None

    @staticmethod
    def check_availability(role: ServiceRoles) -> bool:
        return not DataTool.is_empty(RPC.ping(role))
    
    @staticmethod
    def internal_call(role: ServiceRoles, command: ServiceCommands, parameters: Any = None) -> str:
        A = sys.modules["pih.pih"].A
        A.SRV.init()
        try:
            if role is None:
                role = A.SRV.get_role_by_command(command)
            service_host: str = A.SRV.get_host(role)
            service_port: int = A.SRV.get_port(role)
            timeout: int = None 
            if RPC.Service.role is None or RPC.Service.role.value.isolated or role.value.isolated:
                if command == ServiceCommands.ping:
                    timeout = CONST.RPC.TIMEOUT_FOR_PING
                else:
                    timeout = CONST.RPC.TIMEOUT
            return RPC.CommandClient(service_host, service_port).call_command(command.name, DataTool.rpc_represent(parameters), timeout).data
        except grpc.RpcError as error:
            code: Tuple = error.code()
            details: str = f"Service role:{role.name}\nHost: {service_host}:{service_port}\nCommand: {command.name}\nDetails: {error.details()}\nCode: {code}"
            A.E.rpc_error_handler(details, code, role, command)

    @staticmethod
    def call(command: ServiceCommands, parameters: Any = None) -> str:
        return RPC.internal_call(None, command, parameters)