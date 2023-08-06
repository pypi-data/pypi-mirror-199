# For reference
# https://cql.hl7.org/09-b-cqlreference.html

from typing import Union
from enum import Enum
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from cqlpy.types import *


class DateTimePrecision(Enum):
    Year = 0
    Month = 1
    Day = 2
    Hour = 3
    Minute = 4
    Second = 5
    Millisecond = 6


# cql py Operators (not in spec)


def cql_in(item, argument) -> bool:
    if is_null(item) or is_null(argument):
        return False
    if isinstance(argument, Interval):
        return in_interval(item, argument)
    else:
        return in_list(item, argument)


def to_concept(code: Code) -> Concept:
    return Concept([code])


def to_list(*args) -> list:
    return [item for item in args]


# SECTION 3: Type Operators

# 3.20 ToDateTime https://cql.hl7.org/09-b-cqlreference.html#todatetime


def to_datetime(argument: Union[Date, DateTime]) -> DateTime:
    return argument


# Section 4: Nullological Operators

# 4.1 Coalese https://cql.hl7.org/09-b-cqlreference.html#coalesce


def coalese(*args) -> object:
    for arg in args:
        if not is_null(arg):
            return arg
    return Null()


# 4.2 IsNull https://cql.hl7.org/09-b-cqlreference.html#isnull


def is_null(argument: object) -> bool:
    return (
        (argument is None)
        or (argument == Null)
        or (
            hasattr(argument, "value")
            and ((argument.value is None) or (argument.value == Null))
        )
    )


# 4.3 IsFalse https://cql.hl7.org/09-b-cqlreference.html#isfalse


def is_false(argument: object) -> bool:
    return (argument == False) or (
        hasattr(argument, "value") and argument.value == False
    )


# 4.4 IsTrue https://cql.hl7.org/09-b-cqlreference.html#istrue


def is_true(argument: object) -> bool:
    return (argument == True) or (hasattr(argument, "value") and argument.value == True)


# SECTION 5: Comparison Operators

# 5.2 Equal https://cql.hl7.org/09-b-cqlreference.html#equal


def equal(left, right) -> bool:
    return left == right


# 5.3 Equivalent https://cql.hl7.org/09-b-cqlreference.html#equivalent


def equivalent(left, right) -> bool:
    if isinstance(left, Concept) and isinstance(right, Concept):
        for code_left in left.codes:
            for code_right in right.codes:
                if code_left.code == code_right.code:
                    return True
        return False
    else:
        return (
            hasattr(left, "value")
            and hasattr(right, "value")
            and (left.value == right.value)
        )


# 5.4 Greater https://cql.hl7.org/09-b-cqlreference.html#greater


def greater(left, right) -> bool:
    if is_null(left) or is_null(right):
        return False
    else:
        left_value = (
            left["value"]
            if left.__class__.__name__ == "Resource"
            else left.value
            if isinstance(left, Quantity)
            else left
        )
        right_value = (
            right["value"]
            if right.__class__.__name__ == "Resource"
            else right.value
            if isinstance(right, Quantity)
            else right
        )
        return left > right


# 5.5 Greater or Equal https://cql.hl7.org/09-b-cqlreference.html#greater-or-equal


def greater_or_equal(left, right) -> bool:
    if is_null(left) or is_null(right):
        return False
    else:
        left_value = (
            left["value"]
            if left.__class__.__name__ == "Resource"
            else left.value
            if isinstance(left, Quantity)
            else left
        )
        right_value = (
            right["value"]
            if right.__class__.__name__ == "Resource"
            else right.value
            if isinstance(right, Quantity)
            else right
        )
        return left >= right


# 5.6 Less https://cql.hl7.org/09-b-cqlreference.html#less


def less(left, right) -> bool:
    if is_null(left) or is_null(right):
        return False
    else:
        left_value = (
            left["value"]
            if left.__class__.__name__ == "Resource"
            else left.value
            if isinstance(left, Quantity)
            else left
        )
        right_value = (
            right["value"]
            if right.__class__.__name__ == "Resource"
            else right.value
            if isinstance(right, Quantity)
            else right
        )
        return left < right


# 5.7 Less or Equal https://cql.hl7.org/09-b-cqlreference.html#less-or-equal


def less_or_equal(left, right) -> bool:
    if is_null(left) or is_null(right):
        return False
    else:
        left_value = (
            left["value"]
            if left.__class__.__name__ == "Resource"
            else left.value
            if isinstance(left, Quantity)
            else left
        )
        right_value = (
            right["value"]
            if right.__class__.__name__ == "Resource"
            else right.value
            if isinstance(right, Quantity)
            else right
        )
        return left <= right


# 5.8 Not Equal https://cql.hl7.org/09-b-cqlreference.html#not-equal


def not_equal(left, right) -> bool:
    if is_null(left) or is_null(right):
        return False
    else:
        left_value = (
            left["value"]
            if left.__class__.__name__ == "Resource"
            else left.value
            if isinstance(left, Quantity)
            else left
        )
        right_value = (
            right["value"]
            if right.__class__.__name__ == "Resource"
            else right.value
            if isinstance(right, Quantity)
            else right
        )
        return left != right


# SECTION 6: Arithmetic Operators

# 6.11 Maximum https://cql.hl7.org/09-b-cqlreference.html#maximum


def max_value(type_name: str) -> CqlAny:
    if type_name == "DateTime":
        return DateTime(9999, 12, 31, 23, 59, 59, 999)
    else:
        return Null()


# 6.12 Minimum https://cql.hl7.org/09-b-cqlreference.html#minimum


def min_value(type_name: str) -> CqlAny:
    if type_name == "DateTime":
        return DateTime(1, 1, 1, 0, 0, 0, 0)
    else:
        return Null()


# SECTION 7: String Operators

# 7.3 EndsWith https://cql.hl7.org/09-b-cqlreference.html#endswith


def ends_with(argument: str, suffix: str) -> bool:
    return argument[-len(suffix) :] == suffix


# 7.11 Split https://cql.hl7.org/09-b-cqlreference.html#split


def split(string_to_split: str, separator: str) -> list[str]:
    return string_to_split.split(separator)


# SECTION 8: DateTime Operators

# 8.1 Add https://cql.hl7.org/09-b-cqlreference.html#add-1


def add(left: DateTime, right: Quantity) -> DateTime:
    if is_null(left) or is_null(right):
        return Null()
    else:
        if (right.unit == "days") or (right.unit == DateTimePrecision.Day):
            return DateTime().parse_datetime(left.value + timedelta(days=right.value))
        if (right.unit == "months") or (right.unit == DateTimePrecision.Month):
            return DateTime().parse_datetime(
                left.value + relativedelta(months=right.value)
            )
        if (right.unit == "years") or (right.unit == DateTimePrecision.Year):
            return DateTime().parse_datetime(
                left.value + relativedelta(years=right.value)
            )
        else:
            return Null()


# 8.2 After https://cql.hl7.org/09-b-cqlreference.html#after


def after(
    left: DateTime,
    right: DateTime,
    precision: DateTimePrecision = DateTimePrecision.Millisecond,
) -> bool:
    if is_null(left) or is_null(right):
        return Null()
    else:
        return left > right


# 8.3 Before https://cql.hl7.org/09-b-cqlreference.html#before


def before(
    left: DateTime,
    right: DateTime,
    precision: DateTimePrecision = DateTimePrecision.Millisecond,
) -> bool:
    if is_null(left) or is_null(right):
        return Null()
    else:
        return left < right


# 8.7 Difference https://cql.hl7.org/09-b-cqlreference.html#difference


def difference_between(
    low: DateTime, high: DateTime, precision: DateTimePrecision
) -> int:
    if is_null(low) or is_null(high):
        return Null()
    elif precision == DateTimePrecision.Day:
        return (high.value - low.value).days
    elif precision == DateTimePrecision.Month:
        (high.value.year - low.value.year) * 12 + high.value.month - low.value.month
    elif precision == DateTimePrecision.Year:
        return (high.value - low.value).years
    else:
        return Null()


# 8.8 Duration Between https://cql.hl7.org/09-b-cqlreference.html#duration


def duration_between(
    low: DateTime, high: DateTime, precision: DateTimePrecision
) -> int:
    if is_null(low) or is_null(high):
        return Null()
    elif precision == DateTimePrecision.Day:
        return (high.value - low.value).days
    elif precision == DateTimePrecision.Month:
        (high.value.year - low.value.year) * 12 + high.value.month - low.value.month
    elif precision == DateTimePrecision.Year:
        return (high.value - low.value).years
    else:
        return Null()


# 8.14 Same Or Before https://cql.hl7.org/09-b-cqlreference.html#same-or-before-1


def same_or_before(left: DateTime, right: DateTime) -> bool:
    if is_null(left) or is_null(right):
        return False
    else:
        return left.value <= right.value


# 8.15 Substract https://cql.hl7.org/09-b-cqlreference.html#subtract-1


def subtract(left: DateTime, right: Quantity) -> DateTime:
    if is_null(left) or is_null(right):
        return Null()
    else:
        if (right.unit == "days") or (right.unit == DateTimePrecision.Day):
            return DateTime().parse_datetime(left.value - timedelta(days=right.value))
        if (right.unit == "months") or (right.unit == DateTimePrecision.Month):
            return DateTime().parse_datetime(
                left.value - relativedelta(months=right.value)
            )
        if (right.unit == "years") or (right.unit == DateTimePrecision.Year):
            return DateTime().parse_datetime(
                left.value - relativedelta(years=right.value)
            )
        else:
            return Null()


# SECTION 9: Interval Operators

# 9.11 In https://cql.hl7.org/09-b-cqlreference.html#in


def in_interval(point, argument: Interval) -> bool:
    if (
        isinstance(point, DateTime)
        and isinstance(argument, Interval)
        and not is_null(argument.low)
        and not is_null(argument.high)
    ):
        return (
            (point.value > argument.low.value)
            and (point.value < argument.high.value)
            or (point.value == argument.low.value and argument.low_closed)
            or (point.value == argument.high.value and argument.high_closed)
        )

    return False


# 9.13 Included In https://cql.hl7.org/09-b-cqlreference.html#included-in


def included_in(left: Union[Interval, Date, DateTime, int], right: Interval) -> bool:
    if isinstance(left, Interval):
        return included_in(left.low, right) and included_in(left.high, right)

    if (
        isinstance(left, DateTime)
        and isinstance(right, Interval)
        and not is_null(right.low)
        and not is_null(right.high)
    ):
        return (
            (left.value > right.low.value)
            and (left.value < right.high.value)
            or (left.value == right.low.value and right.low_closed)
            or (left.value == right.high.value and right.high_closed)
        )

    return False


# 9.20 Overlaps https://cql.hl7.org/09-b-cqlreference.html#overlaps


def overlaps(left: Interval, right: Interval) -> bool:
    return (
        (not is_null(left))
        and (not is_null(right))
        and (
            included_in(left, right)
            or included_in(right, left)
            or included_in(left.low, right)
            or included_in(left.high, right)
        )
    )


# 9.28 Start https://cql.hl7.org/09-b-cqlreference.html#start


def start(argument: Interval) -> DateTime:
    if not is_null(argument):
        return argument.low
    else:
        return Null()


def end(argument: Interval) -> DateTime:
    if not is_null(argument):
        return argument.high
    else:
        return Null()


# def overlaps(self, cql_interval) -> bool:
#     return self.low.included_in(cql_interval) or self.high.included_in(cql_interval) or cql_interval.low.included_in(self)

# def intersect(self, cql_interval): # -> CqlList:
#     # this is just a placeholder to test syntax; implementation required
#     return self

# SECTION 10: List Operators

# 10.2 Distinct https://cql.hl7.org/09-b-cqlreference.html#distinct


def distinct(argument: list) -> list:
    result = []
    for item in argument:
        if not (item in result):
            result.append(item)
    return result


# 10.4 Intersect https://cql.hl7.org/09-b-cqlreference.html#intersect-1


def intersect(
    left: Union[list, Interval], right: Union[list, Interval]
) -> Union[list, Interval]:
    if (not is_null(left)) and (not is_null(right)):
        if isinstance(left, Interval) and isinstance(right, Interval):
            if overlaps(left, right):
                return Interval(
                    DateTime().parse_datetime(max(left.low.value, right.low.value)),
                    False,
                    DateTime().parse_datetime(min(left.high.value, right.high.value)),
                    False,
                )
            return Null()

        elif isinstance(left, list) and isinstance(right, list):
            return_list = []
            for left_item in left:
                for right_item in right:
                    if isinstance(left_item, Code) and isinstance(right_item, Code):
                        if left_item.code == right_item.code:
                            return_list.append(left_item)

                    else:
                        if left_item == right_item:
                            return_list.append(left_item)

            return return_list

    return Null()


# 10.6 Exists https://cql.hl7.org/09-b-cqlreference.html#exists


def exists(argument: list) -> bool:
    return (not is_null(argument)) and (len(argument) > 0)


# 10.7 Flatten https://cql.hl7.org/09-b-cqlreference.html#flatten


def flatten(argument: list) -> list:
    result = []
    for item in argument:
        result += item
    return result


# 10.8 First https://cql.hl7.org/09-b-cqlreference.html#first


def first(argument: list) -> object:
    if len(argument) == 0:
        return Null()
    else:
        return argument[0]


# 10.9 In https://cql.hl7.org/09-b-cqlreference.html#in-1


def in_list(element, argument: list) -> bool:
    for item in argument:
        if isinstance(element, Code) and isinstance(item, Code):
            return element.code == item.code
        elif element == item:
            return True

    return False


# 10.15 Last https://cql.hl7.org/09-b-cqlreference.html#last


def last(argument: list) -> object:
    if len(argument) == 0:
        return Null()
    else:
        return argument[-1]


# 10.21 Singleton From https://cql.hl7.org/09-b-cqlreference.html#singleton-from


def singleton_from(argument: list) -> object:
    # todo: handle situations where there is 0 or 2+ instances in the list
    return argument[0]


# 10.25 Union https://cql.hl7.org/09-b-cqlreference.html#union-1


def union(left: list, right: list) -> list:
    return left + right


# SECTION 11: List Operators

# 11.4 Count https://cql.hl7.org/09-b-cqlreference.html#count


def count(argument: list) -> int:
    return len(argument)


# SECTION 12: Clinical Operators

# 12.4 CalculateAgeAt https://cql.hl7.org/09-b-cqlreference.html#calculateageat


def calculate_age_at(
    birth_date: Union[Date, DateTime],
    as_of: Union[Date, DateTime],
    precision: DateTimePrecision = None,
) -> int:
    return (
        as_of.value.year
        - birth_date.value.year
        - (
            (as_of.value.month, as_of.value.day)
            < (birth_date.value.month, birth_date.value.day)
        )
    )


# 12.8 In (ValueSet) https://cql.hl7.org/09-b-cqlreference.html#in-valueset


def in_valueset(argument: Union[str, Code, Concept], value_set: ValueSet) -> bool:
    if is_null(argument):
        return False

    elif isinstance(argument, str):
        for value_set_code in value_set.codes:
            if argument.value == value_set.code:
                return True

    elif isinstance(argument, Code):
        for value_set_code in value_set.codes:
            if argument.code == value_set_code.code:
                return True

    elif isinstance(argument, Concept):
        for code in argument.codes:
            for value_set_code in value_set.codes:
                if code.code == value_set_code.code:
                    return True

    return False


def any_in_valueset(argument: list, value_set: ValueSet) -> bool:
    if not is_null(argument):
        for item in argument:
            if in_valueset(item, value_set):
                return True

    return False


# SORT Operators


def sort_by_column(input: list, field_name: str, direction: str = "asc") -> list:
    return sort_by_expression([(item[field_name], item) for item in input], direction)


def sort_by_direction(input: list, direction: str = "asc") -> list:
    input.sort(reverse=(direction == "desc"))
    return input


def sort_by_expression(input: list, direction: str = "asc") -> list:
    input.sort(reverse=(direction == "desc"), key=tuple_sort)
    return [item[1] for item in input]


def tuple_sort(item) -> object:
    return item[0]
