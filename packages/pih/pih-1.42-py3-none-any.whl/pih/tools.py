from enum import Enum
import ntpath
from datetime import date, datetime, timedelta
import importlib.util
import pathlib
import platform
import re
import string
import random
import json
import os
import subprocess
import sys
from typing import Any, Callable, List, Tuple
import dataclasses

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")
from pih.const import PASSWORD_GENERATION_ORDER, FIELD_COLLECTION_ALIAS
from pih.collection import R, T, FieldItem, FieldItemList, FullName, Result, User, PolibasePerson

class EnumTool:

    @staticmethod
    def get(cls: Enum, key: str, default_value: Any = None) -> Any:
        if key not in cls._member_map_:
            return default_value
        return cls._member_map_[key]

    @staticmethod
    def get_by_value(cls: Enum, value: Any, default_value: str = None) -> Any:
        if isinstance(value, Enum):
            return value
        map: Any = cls._value2member_map_
        return default_value if value not in map else map[value]
    
    @staticmethod
    def get_by_value_or_key(cls: Enum, value: Any) -> Any:
        return EnumTool.get_by_value(cls, value) or EnumTool.get(cls, value)

    @staticmethod
    def get_value(value: Any, default_value: str = None) -> Any:
        if value is not None and isinstance(value, Enum):
            return value.value
        return value or default_value

class DataTool:

    @staticmethod
    def by_index(data: List, index: int, default_value: Any = None) -> Any:
        if data is None:
            return default_value
        if len(data) <= index:
            return default_value
        return data[index]

    @staticmethod
    def represent(data: FieldItemList) -> str:
        return json.dumps(data, cls=PIHEncoder)

    @staticmethod
    def rpc_represent(data: dict) -> str:
        return json.dumps(data, cls=PIHEncoder) if data is not None else ""

    @staticmethod
    def rpc_unrepresent(value: str) -> dict:
        return json.loads(value) if value is not None and value != "" else None

    @staticmethod
    def to_result(result_string: str, class_type_holder: Any = None, first_data_item: bool = False) -> Result:
        result_object: dict = DataTool.rpc_unrepresent(result_string)
        if result_object is None:
            return Result(None, None)
        data: dict = result_object["data"]
        data = DataTool.get_first_item(data) if first_data_item else data
        def obtain_data():
            return (list(map(lambda item: DataTool.fill_data_from_source(class_type_holder(item) if callable(class_type_holder) else class_type_holder(), item), data)) if isinstance(data, list)
                    and class_type_holder is not None else DataTool.fill_data_from_source(class_type_holder(data) if callable(class_type_holder) else class_type_holder(), data) if class_type_holder is not None else data) if data is not None else None
        if "fields_alias" in result_object:
            return Result(FieldItemList(EnumTool.get(FIELD_COLLECTION_ALIAS, result_object["fields_alias"]).value), obtain_data())
        else:
            fields = None if "fields" not in result_object else result_object["fields"]
        field_list: List[FieldItem] = None
        if fields is not None:
            field_list = []
            for field_item in fields:
                for field_name in field_item:
                    field_list.append(DataTool.fill_data_from_source(FieldItem(), field_item[field_name]))
        return Result(FieldItemList(field_list) if field_list else None, obtain_data())

    @staticmethod
    def as_list(value: Any) -> List[Any]:
        if isinstance(value, (List, Tuple)):
            return value
        if DataTool.is_empty(value):
            return [] 
        return [value]

    @staticmethod
    def to_list(value: Any) -> List[Any]:
        result: List[Any] = []
        for item in value:
            result.append(item)
        return result

    def triple_bool(value: bool, false_result: Any, true_result: Any, none_reult: Any) -> Any:
        if value is None:
            return none_reult
        return true_result if value else false_result

    @staticmethod
    def to_result_with_fields(data: str, fields: FieldItemList, cls=None, first_data_item: bool = False) -> Result:
        return Result(fields, DataTool.to_result(data, cls, first_data_item))

    @staticmethod
    def to_string(obj: object, join_symbol: str = "") -> str:
        return join_symbol.join(obj.__dict__.values())

    @staticmethod
    def to_data(obj: object) -> dict:
        return obj.__dict__

    @staticmethod
    def fill_data_from_source(data: object, source: Any) -> object:
        if dataclasses.is_dataclass(source):
            source = source.__dict__
        if source is not None:
            for item in data.__dataclass_fields__:
                if item in source:
                    data.__setattr__(item, source[item])
        else:
            return None
        return data

    @staticmethod
    def fill_data_from_list_source(class_type, source: List) -> object:
        return list(map(lambda item: DataTool.fill_data_from_source(class_type(), item), source))

    def fill_data_from_rpc_str(data: T, source: str) -> T:
        return DataTool.fill_data_from_source(data, DataTool.rpc_unrepresent(source))

    @staticmethod
    def get_first_item(value: List[T], default_value: Any = None) -> Any:
        return DataTool.check(value is not None and len(value) > 0, lambda: value[0], default_value)

    @staticmethod
    def check(check_value: bool, return_value: Callable, default_value: Any = None) -> Any:
        return return_value() if check_value else default_value

    @staticmethod
    def not_none_check(check_value: Any, return_value: Callable, default_value: Any = None) -> Any:
        return DataTool.check(check_value is not None, return_value, default_value() if default_value is not None and isinstance(default_value, Callable) else default_value)

    @staticmethod
    def if_not_none(check_value: Any, return_value: Callable[[Any], Any], default_value: Any = None) -> Any:
        return default_value if check_value is None else return_value(check_value)

    @staticmethod
    def is_empty(data: Any) -> bool:
        return data is None or (isinstance(data, (list, str, dict)) and len(data) == 0)


class StringTool:

    @staticmethod
    def dequotes(value: str) -> Tuple[List[str], List[str]]:
        quotes: List[str] = ["'", "\""]
        value_list: List[str] = list(
            filter(lambda item: not DataTool.is_empty(item), value.split(" ")))
        result: List[str] = []
        count_quote: int = value.count(quotes[0])
        count_quote2: int = value.count(quotes[1])
        if (count_quote + count_quote2) > 0:
            do_first_cut: bool = (count_quote + count_quote2) % 2 == 1
            arg_list: List[str] = []
            for index, list_item in enumerate(value_list):
                is_quoted: bool = list_item[0] in quotes
                if is_quoted:
                    break
            arg_list = value_list[index:]
            value_list = [item for item in value_list if item not in arg_list]
            if do_first_cut:
                for index, arg in enumerate(arg_list):
                    if arg[0] in quotes:
                        arg_list[index] = arg[1:]
                        break
            quotes_map: List[Tuple[int, int]] = []
            for index, arg in enumerate(arg_list):
                if arg[0] in quotes:
                    quotes_map.append((index, -1))
                if arg[-1] in quotes:
                    length: int = len(quotes_map) - 1
                    quotes_map[length] = (quotes_map[length][0], index)
            for index, quote in enumerate(quotes_map):
                value: str = None
                if index == 0:
                    result += arg_list[0:quote[0]]
                value = " ".join(arg_list[quote[0]: quote[1] + 1])
                if not DataTool.is_empty(value):
                    result.append(value[1:-1])
                if index < len(quotes_map) - 1:
                    value = " ".join(
                        arg_list[quote[1] + 1: quotes_map[index + 1][0]])
                    if not DataTool.is_empty(value):
                        result.append(value)
            if len(quotes_map) > 0:
                result += arg_list[quote[1] + 1:]
            else:
                result += arg_list
        return value_list, result

    @staticmethod
    def list_to_string(value: List, escaped_string: bool = False, separator: str = ", ", start: str = "", end: str = "", filter_empty: bool = False) -> str:
        return start + separator.join(list(map(lambda item: f"'{item}'" if escaped_string else str(item) if item is not None else "", list(filter(lambda item: not filter_empty or not DataTool.is_empty(item), value))))) + end

    @staticmethod
    def capitalize(value: str) -> str:
        if DataTool.is_empty(value):
            return ""
        if len(value) == 1:
            return value[0].upper()
        return value[0].upper() + value[1:]
    
    def decapitalize(value: str) -> str:
        if DataTool.is_empty(value):
            return ""
        return value[0].lower() + value[1:]

    @staticmethod
    def from_russian_keyboard_layout(value: str) -> str:
        dictionary: dict[str, str] = {'Й': 'Q', 'Ц': 'W', 'У': 'E', 'К': 'R', 'Е': 'T',
                    'Н': 'Y', 'Г': 'U', 'Ш': 'I', 'Щ': 'O', 'З': 'P',
                    'Х': '{', 'Ъ': '}', 'Ф': 'A', 'Ы': 'S', 'В': 'D',
                    'А': 'F', 'П': 'G', 'Р': 'H', 'О': 'J', 'Л': 'K',
                    'Д': 'L', 'Ж': ':', 'Э': '"', 'Я': 'Z', 'Ч': 'X',
                    'С': 'C', 'М': 'V', 'И': 'B', 'Т': 'N', 'Ь': 'M',
                    'Б': '<', 'Ю': '>', 'Ё': '~', 'й': 'q', 'ц': 'w',
                    'у': 'e', 'к': 'r', 'е': 't', 'н': 'y', 'г': 'u',
                    'ш': 'i', 'щ': 'o', 'з': 'p', 'х': '[', 'ъ': ']',
                    'ф': 'a', 'ы': 's', 'в': 'd', 'а': 'f', 'п': 'g',
                    'р': 'h', 'о': 'j', 'л': 'k', 'д': 'l', 'ж': ';',
                    'э': "'", 'я': 'z', 'ч': 'x', 'с': 'c', 'м': 'v',
                    'и': 'b', 'т': 'n', 'ь': 'm', 'б': ',', 'ю': '.',
                    'ё': '`'} 
        result: str = ""
        for item in value:
            result += dictionary[item] if item in dictionary else item
        return result

class ParameterList:

    def __init__(self, list: Any):
        self.list = list if isinstance(
            list, List) or isinstance(self, Tuple) else [list]
        self.index = 0

    def next(self, object: Any = None, default_value: Any = None) -> Any:
        if self.index >= len(self.list):
            return default_value
        value = self.list[self.index]
        self.index = self.index + 1
        if object is not None:
            value = DataTool.fill_data_from_source(object, value)
        return value

    def get(self, index: int = 0, object: Any = None, default_value: Any = None) -> Any:
        tmp_index: int = self.index
        self.index = index
        result: Any = self.next(object, default_value)
        self.index = tmp_index
        return result

    def set(self, index: int, value: Any) -> None:
        self.list[index] = value

class DateTimeTool:

    @staticmethod
    def timestamp() -> int:
        return int(datetime.now().timestamp())

    def date_or_today_string(date: datetime, format: str = None) -> str:
        return DateTimeTool.to_string(date, format) if date is not None else DateTimeTool.today_string(format)

    @staticmethod
    def today_string(format: str = None, subtract: int = 0) -> str:
        return DateTimeTool.to_string(DateTimeTool.today(subtract).date(), format)

    @staticmethod
    def to_string(date: datetime, format: str = None) -> str:
        if date is None:
            return None
        return date.isoformat() if format is None else date.strftime(format)

    @staticmethod
    def date_to_string(date: datetime, format: str = None) -> str:
        return DateTimeTool.to_string(date.date(), format)

    @staticmethod
    def to_date_string(date: str) -> str:
        list : List[str] = date.split("T")
        return list[0]

    @staticmethod
    def today(delta_days: int = 0) -> datetime:
        return datetime.today() + timedelta(days=delta_days)

    @staticmethod
    def now() -> datetime:
        return datetime.now()

    @staticmethod
    def now_time_string(format: str = None, delta_minutes: int = 0) -> str:
        return DateTimeTool.to_string(DateTimeTool.now_time(delta_minutes), format)

    @staticmethod
    def now_time(delta_minutes: int = 0) -> datetime:
        return datetime.combine(date.today(), datetime.now().time()) + timedelta(minutes=delta_minutes)

    @staticmethod
    def now_string(format: str) -> str:
        return DateTimeTool.to_string(DateTimeTool.now(), format)

    @staticmethod
    def from_string(value: str, format: str = None) -> datetime:
        return datetime.fromisoformat(value) if format is None else datetime.strptime(value, format)

    @staticmethod
    def is_equal_by_time(date: datetime, value: Any) -> bool:
        if isinstance(value, tuple):
            return date.hour == value[0] and date.minute == value[1]
        if isinstance(value, datetime):
            return date.hour == value.hour and date.minute == value.minute
        return None

class ResultTool:

    @staticmethod
    def pack(fields: Any, data: Any) -> dict:
        result: dict = {"data": data}
        if isinstance(fields, FIELD_COLLECTION_ALIAS):
            result["fields_alias"] = fields.name
        else:
            result["fields"] = fields
        return result

    @staticmethod
    def is_empty(result: Result) -> bool:
        return result is None or DataTool.is_empty(result.data)

    @staticmethod
    def get_first_element(result: Result[T], default_value: Any = None) -> T:
        return DataTool.get_first_item(result.data, default_value)

    @staticmethod
    def with_first_element(result: Result[T], default_value: Any = None) -> Result[T]:
        result.data = ResultTool.get_first_element(result, default_value)
        return result

    @staticmethod
    def to_string(result: Result[T], use_index: bool = True, item_separator: str = "\n", value_separator: str = None, show_caption: bool = True) -> str:
        result_string_list: List[str] = []
        data: List = DataTool.as_list(result.data)
        item_result_string_list: List[str] = None
        for index, data_item in enumerate(data):
            if use_index and len(data) > 1:
                result_string_list.append(f"*{str(index + 1)}*:")
            if value_separator is not None:
                item_result_string_list = []
            for field_item in result.fields.list:
                field: FieldItem = field_item
                if not field.visible:
                    continue
                data_value: str = None
                if isinstance(data_item, dict):
                    data_value = data_item[field.name]
                elif dataclasses.is_dataclass(data_item):
                    data_value = data_item.__getattribute__(field.name)
                data_value = data_value or "Нет"
                if value_separator is None:
                    if show_caption:
                        result_string_list.append(f"{field.caption}: {data_value}")
                    else:
                        result_string_list.append(data_value)
                else:
                    if show_caption:
                        item_result_string_list.append(f"{field.caption}: {data_value}")
                    else:
                        item_result_string_list.append(data_value)
            if value_separator is not None:
                result_string_list.append(value_separator.join(item_result_string_list))
        return item_separator.join(result_string_list)

    @staticmethod 
    def as_list(result: Result[T]) -> Result[List[T]]:
        return Result(result.fields, [] if result.data is None else [result.data] if not isinstance(result.data, List) else result.data)

    @staticmethod
    def filter(result: Result[List[T]], filter_function: Callable) -> Result[List[T]]:
        if filter_function is not None:
            try:
                result.data = list(filter(filter_function, result.data))
            except StopIteration:
               pass 
        return result

    @staticmethod
    def sort(result: Result[List[T]], sort_function: Callable) -> Result[List[T]]:
        if sort_function is not None:
            result.data.sort(key=sort_function)
        return result


    @staticmethod
    def every(result: Result[List[T]], action_function: Callable[[T], None]) -> Result[List[T]]:
        for item in result.data:
            action_function(item)
        return result

    @staticmethod
    def map(result: Result[List[T]], map_function: Callable[[T], R], map_on_each_data_item: bool = True) -> Result[List[R]]:
        result.data = list(map(map_function, result.data)
                           ) if map_on_each_data_item else map_function(result.data)
        return result

class TranslateTool:

    def ru_to_en(value: str) -> str:
        return value.translate(dict(zip(map(ord,  
        "йцукенгшщзхъфывапролджэячсмитьбю.ё"
        'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'),
        "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
        'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~')))

class BitMask:

    @staticmethod
    def set(value: int, bit: Any) -> int:
        bits: List[int] = bit if isinstance(bit, list) else [bit]
        for bit in bits:
            value |= bit
        return value

    @staticmethod
    def has(value: int, bit: Any) -> bool:
        bits: List[int] = bit if isinstance(bit, list) else [bit]
        result: bool = False
        if len(bits) > 1:
            for bit in bits:
                result = BitMask.has(value, bit)
                if result:
                    break
        else:
            if isinstance(bit, int):
                result = (value & bit) == bit
            elif isinstance(bit, Enum):
                result = BitMask.has(value, bit.value)
        return result

    @staticmethod
    def unset(value: int, bit: int) -> int:
        if BitMask.has(value, bit):
            value ^= bit
        return value

class ResultUnpack:

    @staticmethod
    def unpack(result: dict) -> Tuple[FieldItemList, Any]:
        return ResultUnpack.unpack_fields(result), ResultUnpack.unpack_data(result)

    @staticmethod
    def unpack_fields(data: dict) -> Any:
        if "fields_alias" in data:
            return FIELD_COLLECTION_ALIAS._member_map_[data["fields_alias"]].value,
        return data["fields"]

    @staticmethod
    def unpack_data(result: dict) -> Any:
        return result["data"]

   
class PathTool:

    @staticmethod
    def makedir_if_not_exists(path: str) -> bool:
        try:
            is_exist = os.path.exists(path)
            if not is_exist:
                os.makedirs(path)
                return True
            return False
        except:
            return None

    @staticmethod
    def get_current_full_path(file_name: str) -> str:
        return os.path.join(sys.path[0], file_name)

    @staticmethod
    def add_extension(file_path: str, extension: str) -> str:
        dot_index: int = file_path.find(".")
        if dot_index != -1:
            source_extension: str = file_path.split(".")[-1]
            if source_extension == extension:
                file_path = file_path[0: dot_index]
        return f"{file_path}.{extension}"

    @staticmethod
    def get_file_name(path: str, with_extension:bool = False):
        head, tail = ntpath.split(path)
        value = tail or ntpath.basename(head)
        if not with_extension:
            value = value[0: value.rfind(".")]
        return value

    @staticmethod
    def get_extension(file_path: str, ) -> str:
        dot_index: int = file_path.find(".")
        if dot_index != -1:
            return file_path[dot_index + 1:]
        return ""

    @staticmethod
    def replace_prohibited_symbols_from_path_with_symbol(path: str, replaced_symbol: str = "_") -> str:
        return path.replace("\\", replaced_symbol).replace("/", replaced_symbol).replace("?", replaced_symbol).replace("<", replaced_symbol).replace(">", replaced_symbol).replace("*", replaced_symbol).replace(":", replaced_symbol).replace("\"", replaced_symbol)

    @staticmethod
    def resolve(src_path: str, host_nane: str = None) -> str:
        src_path = str(pathlib.Path(src_path).resolve())
        if src_path[1] == ":" and host_nane is not None:
            lan_adress: str = f"\\\\{host_nane}\\"
            src_path = f"{lan_adress}{src_path[0]}${src_path[2:]}"
        return src_path


class PIHEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, FieldItem):
            return {f"{obj.name}": obj.__dict__}
        if isinstance(obj, FieldItemList):
            return obj.list
        if isinstance(obj, Enum):
            return obj.name
        if isinstance(obj, ParameterList):
                return obj.list
        if dataclasses.is_dataclass(obj):
            return DataTool.to_data(obj)
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        
        return json.JSONEncoder.default(self, obj)

class NetworkTool:

    @staticmethod
    def is_accessable(host_or_ip: str, packets: int = 1, timeout: int = 100):
        if platform.system().lower() == "windows":
            command = ["ping", "-4", "-n", str(packets), "-w", str(timeout), host_or_ip]
            result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                    stderr=subprocess.DEVNULL, creationflags=0x08000000)
            return result.returncode == 0 and b"TTL=" in result.stdout
        else:
            command = ["ping", "-c", str(packets), "-w", str(timeout), host_or_ip]
            result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return result.returncode == 0
        
class FullNameTool:

    SPLIT_SYMBOL: str = " "
    FULL_NAME_LENGTH: int = 3

    @staticmethod
    def to_string(full_name: FullName, join_symbol: str = SPLIT_SYMBOL) -> str:
        return DataTool.to_string(full_name, join_symbol)

    @staticmethod
    def to_given_name(full_name_holder: Any, join_symbol: str = SPLIT_SYMBOL) -> str:
        if isinstance(full_name_holder, PolibasePerson):
            return FullNameTool.to_given_name(full_name_holder.FullName)
        if isinstance(full_name_holder, User):
            return FullNameTool.to_given_name(full_name_holder.name)
        if isinstance(full_name_holder, FullName):
            return join_symbol.join(list(filter(lambda item: len(item) > 0, [full_name_holder.first_name, full_name_holder.middle_name])))
        elif isinstance(full_name_holder, str):
            full_name_holder = full_name_holder.strip()
            if FullNameTool.is_full_name(full_name_holder):
                return FullNameTool.to_given_name(FullNameTool.from_string(full_name_holder, join_symbol))
            else:
                return full_name_holder

    @staticmethod
    def from_string(value: str, split_symbol: str = SPLIT_SYMBOL) -> FullName:
        full_name_string_list: List[str] = list(filter(lambda item: len(item) > 0, value.split(split_symbol)))
        return FullName(full_name_string_list[0], full_name_string_list[1], full_name_string_list[2])

    @staticmethod
    def is_full_name(value: str, split_symbol: str = SPLIT_SYMBOL) -> bool:
        return len(list(filter(lambda item: len(item) > 0, value.split(split_symbol)))) >= FullNameTool.FULL_NAME_LENGTH

    @staticmethod
    def is_equal(fn_a: FullName, fn_b: FullName) -> bool:
        return fn_a.first_name == fn_b.first_name and fn_a.middle_name == fn_b.middle_name and fn_a.last_name == fn_b.last_name

    @staticmethod
    def is_intersect(fn_a: FullName, fn_b: FullName) -> bool:
        al: List[str] = [fn_a.last_name, fn_a.first_name, fn_a.middle_name]
        bl: List[str] = [fn_b.last_name, fn_b.first_name, fn_b.middle_name]
        return len([value for value in al if value in bl]) == FullNameTool.FULL_NAME_LENGTH

class Clipboard:

    @staticmethod
    def copy(value: str):
        import pyperclip as pc
        pc.copy(value)

    '''
    @staticmethod
    def copy(value: str):
        cmd = 'echo '+value.strip()+'|clip'
        return subprocess.check_call(cmd, shell=True)
    '''

class UserTools:

    @staticmethod
    def get_given_name(user: User) -> str:
        return FullNameTool.to_given_name(user.name)

class PasswordTools:

    @staticmethod
    def check_password(value: str, length: int, special_characters: str) -> bool:
        regexp_string = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[" + special_characters + \
            "])[A-Za-z\d" + special_characters + "]{" + str(length) + ",}$"
        password_checker = re.compile(regexp_string)
        return re.fullmatch(password_checker, value) is not None

    @staticmethod
    def generate_random_password(length: int, special_characters: str, order_list: List[str], special_characters_count: int, alphabets_lowercase_count: int, alphabets_uppercase_count: int, digits_count: int, shuffled: bool):
        # characters to generate password from
        alphabets_lowercase = list(string.ascii_lowercase)
        alphabets_uppercase = list(string.ascii_uppercase)
        digits = list(string.digits)
        characters = list(string.ascii_letters +
                          string.digits + special_characters)
        characters_count = alphabets_lowercase_count + \
            alphabets_uppercase_count + digits_count + special_characters_count
        # check the total length with characters sum count
        # print not valid if the sum is greater than length
        if characters_count > length:
            return
        # initializing the password
        password: List[str] = []
        for order_item in order_list:
            if order_item == PASSWORD_GENERATION_ORDER.SPECIAL_CHARACTER:
             # picking random alphabets
                for i in range(special_characters_count):
                    password.append(random.choice(special_characters))
            elif order_item == PASSWORD_GENERATION_ORDER.LOWERCASE_ALPHABET:
                # picking random lowercase alphabets
                for i in range(alphabets_lowercase_count):
                    password.append(random.choice(alphabets_lowercase))
            elif order_item == PASSWORD_GENERATION_ORDER.UPPERCASE_ALPHABET:
                # picking random lowercase alphabets
                for i in range(alphabets_uppercase_count):
                    password.append(random.choice(alphabets_uppercase))
            elif order_item == PASSWORD_GENERATION_ORDER.DIGIT:
                # picking random digits
                for i in range(digits_count):
                    password.append(random.choice(digits))
        # if the total characters count is less than the password length
        # add random characters to make it equal to the length
        if characters_count < length:
            random.shuffle(characters)
            for i in range(length - characters_count):
                password.append(random.choice(characters))
        # shuffling the resultant password
        if shuffled:
            random.shuffle(password)
        # converting the list to string
        # printing the list
        return "".join(password)
