import importlib.util
import sys
from subprocess import CompletedProcess
from typing import Any, List

pih_is_exists = importlib.util.find_spec("pih.pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")
from pih import PIH, A, NotFound, ActionValue, ActionStack, Input, Output, Session
from pih.tools import EnumTool, FullNameTool, ResultTool, DataTool, StringTool
from pih.const import CONST, MarkType, PASSWORD, USER_PROPERTY, FIELD_COLLECTION, PasswordSettings, CheckableSections
from pih.collection import Mark, User, FullName, MarkDivision, UserContainer, LoginPasswordPair, MarkGroup, Result, FieldItemList, WorkstationDescription, ResourceStatus, SiteResourceStatus, CTIndicationValue, CTIndicationDS

class ConsoleAppsApi:

    LINE: str = "........................................................"

    def __init__(self, pih: PIH = None):
        self.pih = pih or PIH
        self.full_name: FullName = None
        self.tab_number: str = None
        self.telephone_number: str = None
        self.division_id: int = None
        self.user_is_exists: bool = False
        self.login: str = None
        self.password: str = None
        self.internal_email: str = None
        self.external_email: str = None
        self.email_password: str = None
        self.polibase_login: str = None
        self.polibase_password: str = None
        self.user_container: UserContainer
        self.description: str = None
        self.use_template_user: bool
        self.need_to_create_mark: bool = None

    def check_resources_and_indications(self, checkable_section_list: List[CheckableSections], ask_for_update_before: bool = False, force_update: bool = False, all: bool = False) -> None:
        if CheckableSections.RESOURCES in checkable_section_list or CheckableSections.WS in checkable_section_list:
            def label_function(resource: ResourceStatus) -> str:
                result: list[str] = []
                accessable: bool = resource.accessable
                result.append(self.bold(self.output.blue_str(resource.name)) + ": " + (
                    self.output.good_str("доступен") if accessable else self.bold(self.output.red_str("не доступен!"))))
                if isinstance(resource, SiteResourceStatus):
                    if resource.check_free_space_status:
                        free_space_result_list: str = resource.free_space_status.split(
                            " ")
                        result.append(self.output.black_str(
                            f"Cвободное место: {free_space_result_list[0]} ({free_space_result_list[1]})"))
                    if resource.check_certificate_status:
                        result.append(self.output.black_str(
                            f"Сертификат доступен до: {resource.certificate_status}"))
                return "\n".join(result)
            force_update = force_update or (ask_for_update_before and self.input.yes_no(
                "Обновить перед получением"))
            if force_update:
                self.output.write_line(
                    self.italic(f"{self.get_formatted_given_name()}, ожидайте получение результата..."))
            for checkable_section in [CheckableSections.RESOURCES, CheckableSections.WS]:
                self.output.new_line()
                self.output.write_result(A.R_RM.get_status_list([checkable_section], force_update, all if len(checkable_section_list) == 1 and CheckableSections.WS in checkable_section_list else False), False, label_function=label_function, separated_result_item=True, title = (self.output.bold(CONST.VISUAL.BULLET + (" Основные ресурсы" if checkable_section == CheckableSections.RESOURCES else " Наблюдаемые компьютеры")) ) if all else None )
        if CheckableSections.INDICATIONS in checkable_section_list:
            self.output.new_line()
            self.output.write_result(A.R_I.get_last_values(), title=self.output.bold((CONST.VISUAL.BULLET + " " if all else "") + "Показания в помещение КТ"))

    @property
    def output(self) -> Output:
        return self.pih.output

    @property
    def input(self) -> Input:
        return self.pih.input

    def send_whatsapp_message(self, telephone_number: str, message: str) -> bool:
        return A.ME_WH_W.send(telephone_number, message, CONST.MESSAGE.WHATSAPP.WAPPI.PROFILE.IT)

    def find_mark(self, value: str = None) -> None:
        self.output.mark.by_any(value or self.input.mark.any())

    def arg(self, index: int = 0, default_value: Any = None) -> Any:
        return self.session.arg(index, default_value)

    def register_ct_indications(self) -> None:
        text: str = f"число, которое может содержать дробную часть разделенную {self.bold('точкой')} или {self.bold('запятой')}"
        number_format_notification_text: str = f"- {self.italic(text)}"
        def float_check_function(value: str | None, show_error: bool = True) -> str | None:
            result: float | None = None
            if value is not None:
                result = A.D_E.float(value)
            if show_error and result is None:
                self.output.error(
                    f"Введите {self.bold('число')} {number_format_notification_text}")
            return None if result is None else str(result)
        temperature: float = float_check_function(self.arg(), False) or self.input.input(
            f"Введите значение {self.bold('температуры')} {number_format_notification_text}", check_function=float_check_function)
        humidity: float = float_check_function(self.arg(1), False) or self.input.input(
            f"Введите значение {self.bold('влажности')} {number_format_notification_text}", check_function=float_check_function)
        indication: CTIndicationValue = CTIndicationValue(temperature, humidity)
        if A.A_I_CT.register(indication):
            with self.output.send_to_group(CONST.MESSAGE.WHATSAPP.GROUP.RD_INDICATIONS):
                self.output.write_result(
                    Result(FIELD_COLLECTION.INDICATIONS.CT, indication), title=f"{self.get_formatted_given_name()}, отправил следующие показания в помещение КТ:")
            self.output.good("спасибо, показания отправлены")

    def find_free_mark(self, value: str = None) -> None:
        self.output.mark.result(A.R_M.by_any(
            value or self.input.mark.any()), "Список свободных карт доступа:")

    def find_user(self, value: str = None) -> None:
        try:
            result: Result[list[User]] = A.R_U.by_any(
                value or self.input.user.title_any())
        except NotFound as error:
            self.output.error(error.get_details())
        else:
            self.output.user.result(result, "Пользователи:")

    def create_password(self) -> str:
        password: str = None
        password_settings: PasswordSettings = PASSWORD.get(self.input.indexed_field_list(
            "Выберите тип пароля", FIELD_COLLECTION.POLICY.PASSWORD_TYPE))
        while True:
            password = self.input.user.generate_password(
                True, password_settings)
            self.output.value("Пароль", password)
            if self.input.yes_no("Использовать", True):
                break
        if self.input.yes_no("Отправить в ИТ отдел"):
            A.L.from_it_bot(f"Сгенерированный пароль:")
            A.L.from_it_bot(password)
        return password

    def make_mark_as_free(self, value: str = None) -> None:
        mark: Mark = self.input.mark.by_any(value)
        mark_type: int = EnumTool.get(MarkType, mark.type)
        if mark_type == MarkType.FREE:
            self.output.error(
                "Карта доступа с введенным номером уже свободная")
        else:
            if self.input.yes_no("Сделать карту свободной"):
                if mark_type == MarkType.TEMPORARY:
                    temporary_tab_number: int = mark.TabNumber
                    mark = A.R_M.temporary_mark_owner(
                        mark).data
                if A.A_M.make_as_free_by_tab_number(mark.TabNumber):
                    if mark_type == MarkType.TEMPORARY:
                        A.L_C.it_notify_about_temporary_mark_return(
                            mark, temporary_tab_number)
                    else:
                        A.L_C.it_notify_about_mark_return(mark)
                    self.output.good(
                        f"Карта доступа с номером {mark.TabNumber} стала свободной")
                else:
                    self.output.error("Ошибка")
            else:
                self.output.error("Отмена")

    def who_lost_the_mark(self, tab_number: str = None):
        try:
            tab_number = tab_number or self.input.tab_number()
            if tab_number is not None:
                try:
                    mark: Mark = self.pih.RESULT.MARK.by_tab_number(
                        tab_number).data
                    mark_type: MarkType = EnumTool.get(MarkType, mark.type)
                    if mark_type == MarkType.FREE:
                        self.output.good("Это свободная карта доступа")
                    elif mark_type == MarkType.GUEST:
                        self.output.good("Это гостевая карта доступа")
                    else:
                        if mark_type == MarkType.TEMPORARY:
                            mark = self.pih.RESULT.MARK.temporary_mark_owner(
                                mark).data
                            tab_number = mark.TabNumber
                            self.output.good("Это временная карта доступа")
                        if mark is not None:
                            telephone_number: str = mark.telephoneNumber
                            self.output.value("Персона", mark.FullName)
                            if not self.pih.CHECK.telephone_number(telephone_number):
                                user: User = A.R_U.by_tab_number(
                                    tab_number).data
                                if user is not None:
                                    telephone_number = user.telephoneNumber
                            if not self.pih.CHECK.telephone_number(telephone_number):
                                self.output.error(f"Телефон не указан")
                            else:
                                self.output.value(
                                    "Телефон", telephone_number)
                                if self.input.yes_no("Отправить сообщение", True):
                                    details: str = self.input.input(
                                        f"{self.get_formatted_given_name()}, уточните, где забрать найденную карту")
                                    if self.send_whatsapp_message(
                                            telephone_number, f"День добрый, {FullNameTool.to_given_name(mark.FullName)}, вашу карту доступа ({tab_number}) нашли, заберите ее {details}"):
                                        self.output.good(
                                            "Сообщение отправлено")
                                    else:
                                        self.output.error(
                                            "Ошибка при отправке сообщения")
                        else:
                            self.output.error("Телефон не указан")
                except NotFound:
                    self.output.error(
                        "Карта доступа, с введенным номером не найдена")
        except KeyboardInterrupt:
            pass

    def bold(self, value: str) -> str:
        return self.output.bold(value)

    def italic(self, value: str) -> str:
        return self.output.italic(value)

    def run_command(self, command_list: List[str] = None) -> None:
        default_host: str = CONST.HOST.DC2.NAME
        host: str = None
        def get_command_list() -> list[str]:
            command_list: tuple[list[str], list[str]] = StringTool.dequotes(
                self.pih.input.input("Введите команду"))
            return list(filter(lambda item: not DataTool.is_empty(item), command_list[0] + command_list[1]))
        command_list = command_list or get_command_list()
        use_psexec: bool = DataTool.is_empty([value for value in list(map(
            lambda item: item.lower(), command_list)) if value in CONST.PSTOOLS.COMMAND_LIST])
        result: CompletedProcess = None
        if use_psexec:
            if DataTool.is_empty(host):
                if self.input.yes_no(f"Использовать хост {self.bold(default_host)}, для выполнения команды", no_label=f"{self.bold('Или введите название хоста')}"):
                    host = default_host
                else:
                    host = self.input.answer
            while True:
                host = host.lower()
                if A.C_RM.accessibility_by_ping(host, count=1):
                    self.output.write_line(
                        f"Команда будет запущена на хосте {self.bold(host)}\n")
                    break
                else:
                    self.output.error(f"Хост {self.bold(host)} не доступен")
                    host = self.input.input(
                        "Введите имя хоста, на котором будет выполнена команда")
            self.output.write_line(
                f"{self.get_formatted_given_name()}, ожидайте окончания выполнения команды...")
            result = A.PS.execute_command_list(A.PS.create_command_list_for_psexec_command(
                command_list, host, interactive=True, run_from_system_account=True, run_with_elevetion=True), True, True)
        else:
            self.output.write_line(
                f"{self.get_formatted_given_name()}, ожидайте окончания выполнения команды...")
            result = A.PS.execute_command_list(
                A.PS.create_command_list_for_pstools_command(command_list[0], command_list[1:]), True, True)
        result_out: str = result.stdout
        if not DataTool.is_empty(result_out):
            self.output.write_line(result_out)
        if result.returncode != 0:
            error: str = result.stderr
            self.output.write_line(error)

    def create_new_mark(self):

        self.full_name = None
        self.tab_number = None
        self.telephone_number = None
        self.division_id = None

        def get_full_name() -> ActionValue:
            self.output.header("Заполните ФИО персоны")
            self.full_name = self.input.full_name(True)
            user_is_exsits: bool = not self.pih.CHECK.MARK.exists_by_full_name(
                self.full_name)
            if user_is_exsits:
                self.output.error(
                    "Персона с данной фамилией, именем и отчеством уже есть!")
                if not self.input.yes_no("Продолжить"):
                    self.session.exit()
            return self.output.get_action_value("ФИО персоны", FullNameTool.to_string(self.full_name))

        def get_telephone_number() -> ActionValue:
            self.output.header("Заполните номер телефона")
            self.telephone_number = self.input.telephone_number()
            return self.output.get_action_value("Номер телефона", self.telephone_number, False)

        def get_tab_number() -> ActionValue:
            self.output.header("Выбор группы и номера для карты доступа")
            free_mark: Mark = self.input.mark.free()
            group_name: str = free_mark.GroupName
            self.tab_number = free_mark.TabNumber
            self.output.value("Группа карты доступа", group_name)
            return self.output.get_action_value("Номер карты пропуска", self.tab_number)

        def get_division() -> ActionValue:
            self.output.header("Выбор подразделения")
            person_division: MarkDivision = self.input.mark.person_division()
            self.division_id = person_division.id
            return self.output.get_action_value("Подразделение, к которому прикреплена персона", person_division.name)

        ActionStack("Данные пользователя",
                    get_full_name,
                    get_division,
                    get_telephone_number,
                    get_tab_number,
                    input=self.input,
                    output=self.output
                    )
        if self.input.yes_no("Создать карту доступа для персоны", True):
            if self.pih.ACTION.MARK.create(self.full_name, self.division_id, self.tab_number, self.telephone_number):
                self.output.good("Карты доступа создана!")
                self.pih.LOG.COMMAND.it_notify_about_create_new_mark(
                    self.full_name)
                if self.input.yes_no("Уведомить персону", True):
                    self.send_whatsapp_message(
                        self.telephone_number, f"Сообщение от ИТ отдела Pacific International Hospital: День добрый, {FullNameTool.to_given_name(self.full_name)}, Вам выдана карта доступа с номером {self.tab_number}")
            else:
                self.output.error("Карта доступа не создана!")

    def send_workstation_message_to_all(self) -> None:
        message: str = self.input.message(
            f"{self.get_formatted_given_name()}, введите сообщение для всех пользователей")
        A.ME_WS.to_all_workstations(
            message, None, [CONST.HOST.WS255], self.session)

    @property
    def user(self) -> User:
        return self.session.user

    @property
    def user_description(self) -> str:
        return A.D_F.description(self.user.description)

    def send_workstation_message(self, recipient_name: str = None, use_dialog: bool = False) -> None:
        recipient: User | WorkstationDescription = None
        while True:
            try:
                recipient = DataTool.get_first_item(
                    self.input.user.by_any(recipient_name, True))
                if recipient is not None:
                    break
            except NotFound as error:
                value: str = error.get_value()
                if A.C_WS.name(value):
                    if A.C_WS.exists(value):
                        recipient = A.R_WS.by_name(value).data
                        break
                if recipient is None:
                    recipient_name = None
                    self.output.error(error.get_details())
        if isinstance(recipient, User) and ResultTool.is_empty(A.R_WS.by_login(recipient.samAccountName)):
            self.output.error(
                f"Пользователь {recipient.name} ({recipient.samAccountName}) не залогинен ни за одним компьютером.")
        else:
            try:
                use_dialog = use_dialog or self.input.yes_no("Начать диалог")
                while True:
                    user_given_name: str = self.get_formatted_given_name(self.user_given_name)
                    if isinstance(recipient, User):
                        message: str = self.input.message(
                            f"{user_given_name}, введите сообщение для пользователя {self.get_formatted_given_name(FullNameTool.to_given_name(recipient))}", f"Сообщение от {self.user_given_name} ({self.user_description}): {FullNameTool.to_given_name(recipient)}, ")
                        if A.ME_WS.to_user(recipient, message):
                            self.output.good("сообщение отправлено")
                    else:
                        message: str = self.input.message(
                            f"{user_given_name}, введите сообщение для компьютера {recipient.name}", f"Сообщение от {self.user_given_name} ({self.user_description}): ")
                        if A.ME_WS.to_workstation(recipient, message):
                            self.output.good("сообщение отправлено")
                    if use_dialog:
                        self.output.separated_line()
                    else:
                        break
            except KeyboardInterrupt:
                if use_dialog:
                    A.O.error("Выход из диалога...")
                else:
                    A.O.error("Отмена...")

    @property
    def user_given_name(self) -> str:
        return self.session.user_given_name
    
    def get_formatted_given_name(self, value: str = None) -> str:
        return self.output.user.get_formatted_given_name(value or self.user_given_name)

    def create_temporary_mark(self, owner_mark: Mark = None) -> None:
        owner_mark = owner_mark or self.input.mark.by_any()
        mark_group: MarkGroup = None
        if self.input.yes_no("Выдать временную карту доступа из той же группы доступа"):
            mark_group = owner_mark
        temporary_mark: Mark = self.input.mark.free(mark_group)
        self.output.temporary_candidate_for_mark(temporary_mark)
        full_name: str = owner_mark.FullName
        tab_number: str = temporary_mark.TabNumber
        if self.input.yes_no(f"Создать временную карту для {full_name} с табельным номеров {tab_number}", True):
            if A.A_M.make_as_temporary(temporary_mark, owner_mark):
                self.output.good("Временная карта создана")
                telephone_number: str = owner_mark.telephoneNumber
                A.L_C.it_notify_about_create_temporary_mark(
                    full_name, tab_number)
                if not A.C.telephone_number(telephone_number):
                    user: User = ResultTool.get_first_element(A.R_U.by_any(
                        owner_mark))
                    if user is not None:
                        telephone_number = user.telephoneNumber
                if A.C.telephone_number(telephone_number):
                    if self.input.yes_no("Уведомить персону", True):
                        self.send_whatsapp_message(
                            telephone_number, f"Сообщение от ИТ отдела: День добрый, {self.get_formatted_given_name(full_name)}, Вам выдана временная карта доступа с номером {tab_number}")
            else:
                self.output.error("Ошибка при создании временной карты")
        else:
            self.output.error("Отмена")

    def telephone_number_fix_action(self, user: User) -> None:
        try:
            telephone: str = self.input.telephone_number()
            if A.A_U.set_telephone_number(user, telephone):
                self.output.good("Сохранен")
                self.output.line()
            else:
                self.output.error("Ошибка")
        except KeyboardInterrupt:
            self.output.new_line()
            self.output.error("Отмена")
            self.output.new_line()

    def start_user_telephone_number_editor(self) -> None:
        only_empty_phones_edit: bool = self.input.yes_no(
            "Редактировать только телефоны, которые не заданы", True)
        result: Result[list[User]] = A.R_U.list(True)
        for user in result.data:
            user: User = user
            if A.C_U.user(user):
                if user.telephoneNumber is None:
                    self.output.error(f"{user.name}: нет телефона")
                    self.telephone_number_fix_action(user)
                elif not A.C.telephone_number(user.telephoneNumber):
                    fixed_telephone: str = A.D_F.telephone_number(
                        user.telephoneNumber)
                    if A.C.telephone_number(fixed_telephone):
                        self.output.good(f"{user.name} телефон исправлен")
                        A.A_U.set_telephone_number(
                            user, fixed_telephone)
                    else:
                        self.output.yellow(
                            f"{user.name}: неправильный формат телефона ({user.telephoneNumber})")
                else:
                    if not only_empty_phones_edit:
                        self.output.good(
                            f"{user.name}: телефон присутствует")
                        self.telephone_number_fix_action(user)
            else:
                self.output.notify(
                    f"{user.name}, похоже не пользователь, у которого должен быть номер телефона")

    def start_user_property_setter(self, property_name: str, search_value: str = None, choose_user: bool = False) -> None:
        try:
            user_list: list[User] = None
            fields: FieldItemList = FIELD_COLLECTION.AD.USER
            active: bool | None = True if (
                property_name == USER_PROPERTY.PASSWORD or property_name == USER_PROPERTY.TELEPHONE_NUMBER) else None
            if choose_user:
                user_list = self.input.user.by_any(search_value, active)
            else:
                result: Result[list[User]] = A.R_U.by_any(
                    self.input.user.title_any(), active)
                user_list = result.data
            if property_name == USER_PROPERTY.USER_STATUS:
                for status in [CONST.AD.ACTIVE_USERS_CONTAINER_DN, CONST.AD.INACTIVE_USERS_CONTAINER_DN]:
                    work_user_list: list[User] = self.pih.DATA.FILTER.users_by_dn(
                        user_list, CONST.AD.INACTIVE_USERS_CONTAINER_DN if status == CONST.AD.ACTIVE_USERS_CONTAINER_DN else CONST.AD.ACTIVE_USERS_CONTAINER_DN)
                    for index, user in enumerate(work_user_list):
                        try:
                            self.output.user.result(Result(fields, [user]))
                            if self.input.yes_no(f"{'Активировать' if status == CONST.AD.ACTIVE_USERS_CONTAINER_DN else 'Деактивировать' } пользователя"):
                                if status == CONST.AD.ACTIVE_USERS_CONTAINER_DN:
                                    if self.input.yes_no("Использовать шаблон для пользователя", True):
                                        user_container = self.input.user.template()
                                    else:
                                        user_container = self.input.user.container()
                                else:
                                    user_container = UserContainer(
                                        distinguishedName=CONST.AD.INACTIVE_USERS_CONTAINER_DN)
                                if self.pih.ACTION.USER.set_status(user, status, user_container):
                                    self.output.good("Успешно")
                                else:
                                    self.output.error("Ошибка")
                            else:
                                self.output.new_line()
                                self.output.error("Отмена")
                        except KeyboardInterrupt:
                            self.output.new_line()
                            if index == len(user_list) - 1:
                                self.output.error("Отмена")
                            else:
                                self.output.error("Отмена - следующий")
                            self.output.new_line()
            else:
                for index, user in enumerate(user_list):
                    try:
                        if property_name == USER_PROPERTY.TELEPHONE_NUMBER:
                            self.output.user.result(
                                Result(fields, [user]), None)
                            telephone = self.input.telephone_number()
                            if self.pih.CHECK.telephone_number(telephone) and self.input.yes_no("Установить", True):
                                if self.pih.ACTION.USER.set_telephone_number(user, telephone):
                                    self.output.good("Успешно")
                                else:
                                    self.output.error("Ошибка")
                            else:
                                self.output.error("Отмена")
                        elif property_name == USER_PROPERTY.PASSWORD:
                            self.output.user.result(
                                Result(fields, [user]), "Пользователи:")
                            password: str = None
                            while True:
                                password = self.input.user.generate_password(True, PASSWORD.get(
                                    self.input.indexed_field_list("Выберите тип пароля", FIELD_COLLECTION.POLICY.PASSWORD_TYPE)))
                                self.output.value("Пароль", password)
                                if self.input.yes_no("Использовать", True):
                                    break
                            if self.input.yes_no("Установить", True):
                                if self.pih.ACTION.USER.set_password(user, password):
                                    self.output.good("Успешно")
                                else:
                                    self.output.error("Ошибка")
                            else:
                                self.output.error("Отмена")
                    except KeyboardInterrupt:
                        self.output.new_line()
                        self.output.error(
                            "Отмена" + (" - следующий" if index != len(user_list) - 1 else ""))
                        self.output.new_line()
        except NotFound as error:
            self.output.error(error.get_details())

    @property
    def session(self) -> Session:
        return self.pih.session

    def create_new_user(self) -> None:

        self.full_name = None
        self.tab_number = None
        self.telephone_number = None
        self.division_id = None
        self.user_is_exists = False
        self.login = None
        self.password = None
        self.internal_email = None
        self.external_email = None
        self.email_password = None
        self.polibase_login = None
        self.polibase_password = None
        self.user_container = None
        self.description = None
        self.use_template_user = None
        self.need_to_create_mark = None

        def get_full_name() -> ActionValue:
            self.output.header("Заполнение ФИО пользователя")
            self.full_name = self.input.full_name(True)
            self.user_is_exists = self.pih.CHECK.USER.exists_by_full_name(
                self.full_name)
            if self.user_is_exists:
                self.output.error(
                    "Пользователем с данной фамилией, именем и отчеством уже есть!")
                if not self.input.yes_no("Продолжить"):
                    self.session.exit()
            return self.output.get_action_value("ФИО пользователя", FullNameTool.to_string(self.full_name))

        def get_login() -> ActionValue:
            self.output.header("Создание логина для аккаунта пользователя")
            self.login = self.input.user.generate_login(self.full_name)
            return self.output.get_action_value("Логин пользователя", self.login)

        def get_telephone_number() -> ActionValue:
            self.output.header("Заполнение номера телефона")
            self.telephone_number = self.input.telephone_number()
            return self.output.get_action_value("Номер телефона", self.telephone_number, False)

        def get_description() -> ActionValue:
            self.output.header("Заполнение описания пользователя")
            self.description = self.input.description()
            return self.output.get_action_value("Описание", self.description, False)

        def get_template_user_container_or_user_container() -> ActionValue:
            self.output.header("Выбор контейнера для пользователя")
            if self.input.yes_no("Использовать шаблон для создания аккаунта пользователя", True):
                self.user_container, self.use_template_user = (
                    self.input.user.template(), True)
                return self.output.get_action_value("Контейнер пользователя", self.user_container.description)
            else:
                self.user_container, self.use_template_user = (
                    self.input.user.container(), False)
                return self.output.get_action_value("Контейнер пользователя", self.user_container.distinguishedName)

        def get_pc_password() -> ActionValue:
            self.output.header("Создание пароля для аккаунта пользователя")
            self.password = self.input.user.generate_password(
                settings=PASSWORD.SETTINGS.PC)
            return self.output.get_action_value("Пароль", self.password, False)

        def get_internal_email() -> ActionValue:
            self.output.header("Создание корпоративной электронной почты")
            if self.input.yes_no("Создать", True):
                self.internal_email = A.D.create_email(self.login)
            return self.output.get_action_value("Адресс корпоративной электронной почты пользователя", self.internal_email)

        def get_email_password() -> ActionValue:
            if self.internal_email:
                self.output.header(
                    "Создание пароля для корпоротивной электронной почты")
                if self.input.yes_no("Использовать пароль от аккаунта пользователя", True):
                    self.email_password = self.password
                else:
                    self.email_password = self.input.user.generate_password(
                        settings=PASSWORD.SETTINGS.EMAIL)
                return self.output.get_action_value("Пароль электронной почты",  self.email_password, False)
            return None

        def get_external_email() -> ActionValue:
            self.output.header("Добавление внешней почты")
            if self.input.yes_no("Добавить"):
                self.external_email = self.input.email()
            return self.output.get_action_value("Адресс внешней электронной почты пользователя", self.external_email if self.external_email else "Нет", False)

        def get_division() -> ActionValue:
            full_name_string: str = FullNameTool.to_string(self.full_name)
            mark: Mark = self.pih.RESULT.MARK.by_name(
                full_name_string, True).data
            if mark is not None:
                if self.input.yes_no(
                        f"Найдена карта доступа для персоны {full_name_string} с номером {mark.TabNumber}. Использовать", True):
                    self.need_to_create_mark = False
                    return None
            self.need_to_create_mark = self.input.yes_no(
                f"Создать карту доступа для персоны '{full_name_string}'", True)
            if self.need_to_create_mark:
                self.output.header("Выбор подразделения")
                person_division: MarkDivision = self.input.mark.person_division()
                self.division_id = person_division.id
                return self.output.get_action_value("Подразделение персоны, которой принадлежит карта доступа", person_division.name)
            return None

        def get_tab_number() -> ActionValue:
            if self.need_to_create_mark:
                self.output.header("Создание карты доступа")
                free_mark: Mark = self.input.mark.free()
                group_name: str = free_mark.GroupName
                self.tab_number = free_mark.TabNumber
                self.output.value("Группа карты доступа", group_name)
                return self.output.get_action_value("Номер карты доступа", self.tab_number)
            return None

        ActionStack(
            "Данные пользователя",
            get_full_name,
            get_login,
            get_telephone_number,
            get_description,
            get_template_user_container_or_user_container,
            get_pc_password,
            get_internal_email,
            get_email_password,
            get_external_email,
            get_division,
            get_tab_number,
            input=self.input,
            output=self.output
        )
        polibase_login: str = self.login
        polibase_password: str = self.password
        if self.input.yes_no("Создать аккаунт для пользователя", True):
            if self.use_template_user:
                self.pih.ACTION.USER.create_from_template(
                    self.user_container.distinguishedName, self.full_name, self.login, self.password, self.description, self.telephone_number, self.internal_email or self.external_email)
            else:
                self.pih.ACTION.USER.create_in_container(
                    self.user_container.distinguishedName, self.full_name, self.login, self.password, self.description, self.telephone_number, self.internal_email or self.external_email)
            if self.need_to_create_mark:
                self.tab_number = self.tab_number or self.pih.RESULT.MARK.by_name(
                    FullNameTool.to_string(self.full_name), True).data.TabNumber
                self.pih.ACTION.MARK.create(
                    self.full_name, self.division_id, self.tab_number, self.telephone_number)
            user_account_document_path: str = self.pih.PATH.USER.get_document_name(
                FullNameTool.to_string(self.full_name), self.login if self.user_is_exists else None)
            if self.pih.ACTION.DOCUMENTS.create_for_user(user_account_document_path, self.full_name, self.tab_number, LoginPasswordPair(self.login, self.password), LoginPasswordPair(
                    polibase_login, polibase_password), LoginPasswordPair(self.internal_email, self.email_password)):
                self.pih.LOG.COMMAND.hr_notify_about_new_employee(self.login)
                self.pih.LOG.COMMAND.it_notify_about_user_creation(
                    self.login, self.password)
                if self.need_to_create_mark:
                    self.pih.LOG.COMMAND.it_notify_about_create_new_mark(
                        self.full_name)
                if self.input.yes_no("Сообщить пользователю о создании документов", True):
                    self.send_whatsapp_message(
                        self.telephone_number, f"Сообщение от ИТ отдела Pacific International Hospital: День добрый, {FullNameTool.to_given_name(self.full_name)}, Вас ожидает документы и карта доступа с номером {self.tab_number} в отделе")
                if self.input.yes_no("Отправить пользователю данные об аккаунте", True):
                    self.send_whatsapp_message(
                        self.telephone_number, f"Сообщение от ИТ отдела Pacific International Hospital: День добрый, {FullNameTool.to_given_name(self.full_name)}, данные Вашего аккаунта:\nЛогин: {self.login}\nПароль: {self.password}\nЭлектронная почта: {self.internal_email}")
