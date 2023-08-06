# For reference
# https://cql.hl7.org/09-b-cqlreference.html
# https://rszalski.github.io/magicmethods/

# CQL Structured types implemented as Python classes:
# 1.1 CqlAny
# 1.3 Code
# 1.4 CodeSystem
# 1.5 Concept
# 1.6 Date (technically a CQL simple type, but CQL uncertainty and date precision concepts require class implementation)
# 1.7 DateTime (technically a CQL simple type, but CQL uncertainty and date precision concepts require class implementation)
# 1.11 Quantity
# 1.12 Ratio (not yet implemented)
# 1.14 Time (not yet implemented, technically a CQL simple type, but CQL uncertainty and time precision concepts require class implementation)
# 1.15 ValueSet (extended to include a codes property)
# 1.16 Vocabulary (not yet implemented)
# Parameter (technically not a type, but implemented as one)

# CQL Simple types implemented as native Python types:
# 1.2 Boolean (bool)
# 1.8 Decimal (float)
# 1.9 Long (int)
# 1.10 Integer (int)
# 1.13 String (str)


from abc import ABCMeta, abstractmethod
from typing import Union
import json
from datetime import datetime


class Null:
    def __eq__(self, compare: object) -> object:
        return compare == Null

    def __getitem__(self, query: str) -> object:
        return Null()


class CqlAny(metaclass=ABCMeta):
    """
    All Cql types inherit from the CqlAny base class.
    """

    @property
    @abstractmethod
    def value(self):  # the return type depends on the class
        """
        A representation of the Cql type as a python type that is useful for comparison operations.
        """
        pass

    @abstractmethod
    def parse_fhir_json(
        self, fhir_json: object
    ):  # -> the Cql type implemented by the class.
        """
        This method will instatiate the instance with the appropriate state based on snippet of FHIR represented as an object.
        The object should be in the format that would appear in FHIR json.
        This method returns a reference to the instance to support one line syntax such as: return my_cql_string.parse_fhir_json("foo")
        """
        pass

    @abstractmethod
    def parse_cql(self, cql: str):  # -> the Cql type implemented by the class.
        """
        This method will instatiate the instance with the appropriate state based on snippet of CQL represented as a string.
        This method returns a reference to the instance to support one line syntax such as: return my_cql_string.parse_cql("foo")
        This method will generally be called from the constructor so that the type can be instantiated in one line: return CqlString("foo")
        """
        pass


class CodeSystem(CqlAny):
    def __init__(
        self,
        id: str = None,
        version: str = None,
    ):
        self.id = id
        self.version = version

    def __str__(self) -> str:
        return "id:" + str(self.id) + ", version:" + str(self.version)

    @property
    def value(self) -> tuple:
        return self.id, self.version

    def parse_cql(self, cql: str = None):  # -> CodeSystem:
        self.id = None
        self.version = None

        return self

    def parse_fhir_json(self, fhir_json: object):  # -> CodeSystem:
        self.id = None
        self.version = None

        return self


class Code(CqlAny):
    def __init__(
        self,
        system: Union[str, CodeSystem] = None,
        code: str = None,
        display: str = None,
        version: str = None,
    ):
        self.code = code
        self.display = display
        self.system = system
        self.version = version

    def __str__(self) -> str:
        return (
            "code:"
            + str(self.code)
            + ", display:"
            + str(self.display)
            + ", system:"
            + str(self.system)
        )

    @property
    def value(self) -> tuple:
        return self.system, self.code, self.version

    def parse_cql(self, cql: str = None):  # -> Code:
        self.code = None
        self.display = None
        self.system = None
        self.version = None

        return self

    def parse_fhir_json(self, fhir_json: object):  # -> Code:
        self.code = fhir_json["code"] if "code" in fhir_json else ""
        self.display = fhir_json["display"] if "display" in fhir_json else ""
        self.system = fhir_json["system"] if "system" in fhir_json else ""
        self.version = fhir_json["version"] if "version" in fhir_json else ""

        return self


class Concept(CqlAny):
    """
    Concept represents a FHIR codeable concept as a list of Code
    The FHIR codeable concept will be represented in json following the pattern of the following example:

    {
        'coding': [
                    {
                        'system': 'http://anthem.com/codes/Facets/DiagnosisCode',
                        'code': '78099',
                        'display': 'Other general symptoms',
                        'userSelected': True
                    },
                    {
                        'system': 'http://fhir.carevolution.com/codes/z-ICD9-DONOTUSE/DiagnosisCode',
                        'version': 'LEGACY',
                        'code': '78099',
                        'display': 'Other general symptoms',
                        'userSelected': False
                    },
                    {
                        'system': 'http://hl7.org/fhir/sid/icd-9-cm',
                        'code': '780.99',
                        'display':
                        'Other general symptoms',
                        'userSelected': False
                    },
                    {
                        'system': 'http://fhir.carevolution.com/codes/ICD9/DiagnosisCode',
                        'code': '78099',
                        'display': 'Other general symptoms',
                        'userSelected': False
                    }
                ]
    }
    """

    def __init__(self, codes: list = []):
        self.codes = codes
        self.display = ""

    def __str__(self) -> str:
        return "display= , codes = " + str([str(code) for code in self.codes])

    @property
    def value(self) -> list:
        return self.codes

    def parse_cql(self, cql: str = None):  # -> Concept:
        self.codes = []
        self.display = ""

        return self

    def parse_fhir_json(self, fhir_json: dict[str, dict[str, str]]):  # -> Concept:
        if "coding" in fhir_json:
            self.codes = [
                Code().parse_fhir_json(fhir_code) for fhir_code in fhir_json["coding"]
            ]
        else:
            self.codes = []
        self.display = ""

        return self


class DateTime(CqlAny):
    def __init__(
        self,
        year: int = None,
        month: int = None,
        day: int = None,
        hour: int = None,
        minute: int = None,
        second: int = None,
        millisecond: int = None,
    ):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.millisecond = millisecond

    def __str__(self) -> str:
        return str(self.value)

    @property
    def value(self) -> datetime:
        return datetime(
            self.year, self.month, self.day, self.hour, self.minute, self.second
        )

    def parse_cql(self, cql: str = None):  # -> DateTime:
        if cql:
            cql = cql.replace("@", "").strip()

            self.year = int(cql[0:4])
            self.month = int(cql[5:7]) if len(cql) > 6 else 0
            self.day = int(cql[8:10]) if len(cql) > 9 else 0
            self.hour = int(cql[11:13]) if len(cql) > 12 else 0
            self.minute = int(cql[14:16]) if len(cql) > 15 else 0
            self.second = int(cql[17:19]) if len(cql) > 18 else 0
        else:
            self.year = 0
            self.month = 0
            self.day = 0
            self.hour = 0
            self.minute = 0
            self.second = 0

        return self

    def parse_fhir_json(self, fhir_json: object):  # -> DateTime:
        fhir_value = json.dumps(fhir_json).replace('"', "").strip()

        # 2019-05-30T00:00:00-00:00
        # 0         1         2
        # 012345678901234567890123456789
        self.year = int(fhir_value[0:4])
        self.month = int(fhir_value[5:7])
        self.day = int(fhir_value[8:10])
        self.hour = int(fhir_value[11:13]) if len(fhir_value) > 12 else 0
        self.minute = int(fhir_value[14:16]) if len(fhir_value) > 15 else 0
        self.second = int(fhir_value[17:19]) if len(fhir_value) > 18 else 0

        return self

    def parse_datetime(self, value: datetime):  # -> DateTime:
        self.year = value.year
        self.month = value.month
        self.day = value.day
        self.hour = value.hour
        self.minute = value.minute
        self.second = value.second

        return self


class Date(DateTime):
    def __init__(self, year: int = None, month: int = None, day: int = None):
        super().__init__(year, month, day)


class Interval(CqlAny):
    def __init__(
        self,
        low: Union[DateTime, Date, int, float] = None,
        low_closed: bool = None,
        high: Union[DateTime, Date, int, float] = None,
        high_closed: bool = None,
        generic_type=None,
    ):
        self.low = low
        self.low_closed = low_closed
        self.high = high
        self.high_closed = high_closed

        self.generic_type = generic_type

    def __str__(self) -> str:
        return (
            ("[" if self.low_closed else "(")
            + str(self.low)
            + ", "
            + str(self.high)
            + ("]" if self.high_closed else ")")
        )

    @property
    def value(self) -> tuple:
        return self.low, self.low_closed, self.high, self.high_closed

    def parse_cql(self, cql: str = None):  # -> Interval:
        if cql:
            cql = cql.replace("Interval", "")

            self.low_closed = cql[:1] == "["
            self.high_closed = cql[-1] == "]"
            self.low = self.generic_type().parse_cql(cql.split(",")[0][1:])
            self.high = self.generic_type().parse_cql(cql.split(",")[1][:-1])
        else:
            self.low_closed = None
            self.high_closed = None
            self.low = None
            self.high = None

        return self

    def parse_fhir_json(self, fhir_json: object):  # -> Interval:
        self.low = self.generic_type().parse_fhir_json(fhir_json["start"])

        if "end" in fhir_json:
            self.high = self.generic_type().parse_fhir_json(fhir_json["end"])
        else:
            self.high = self.low

        self.low_closed = True
        self.high_closed = True

        return self


class Parameter:
    def __init__(self, name: str, type_name: str, default_value: str = None):
        self.name = name
        self.type_name = type_name
        self.default_value = default_value

    def __str__(self):
        return self.name


class Quantity(CqlAny):
    def __init__(self, value: float = None, unit: str = None):
        self._value = value
        self._unit = unit

    def __str__(self) -> str:
        return str(self._value) + " " + self._unit

    @property
    def value(self) -> str:
        return self._value

    @property
    def unit(self) -> str:
        return self._unit

    def parse_cql(self, cql: str = None):  # -> Quantity:
        return self

    def parse_fhir_json(self, fhir_json: object):  # -> Quantity:
        return self


class ValueSet(CqlAny):
    def __init__(self, value_set_id: str = None, name: str = None, version: str = None):
        self.id = value_set_id
        self.name = name
        self.version = version
        self.codes = []

    def __str__(self) -> str:
        return (
            "id:" + self.id
            or "" + ", version:" + self.version
            or "" + ", codes:" + str([str(code) for code in self.codes])
        )

    @property
    def value(self) -> list:
        return self.codes

    def parse_cql(self, cql: str = None):  # -> ValueSet:
        self.id = ""
        self.version = ""
        self.name = ""
        self.codes = []

        return self

    def parse_fhir_json(self, fhir_json: object):  # -> ValueSet:
        # self.id = fhir_json["id"]
        self.version = fhir_json["version"]
        self.name = fhir_json["name"]
        includes = fhir_json["compose"]["include"]
        self.codes = []
        for include in includes:
            self.codes = [
                *self.codes,
                *[
                    Code(
                        system=include["system"] if "system" in include else "",
                        code=concept["code"],
                        display=concept["display"] if "display" in concept else "",
                        version=include["version"] if "version" in include else "",
                    )
                    for concept in include["concept"]
                ],
            ]

        return self
