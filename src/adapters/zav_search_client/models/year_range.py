from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="YearRange")


@attr.s(auto_attribs=True)
class YearRange:
    """Limit results to those in year range (inclusive)

    Attributes:
        name (Union[Unset, str]): Name of the filter
        lower_bound (Union[Unset, int]): Minimum value of range. Example: 2019.
        upper_bound (Union[Unset, int]): Maximum value of range. Example: 2020.
    """

    name: Union[Unset, str] = UNSET
    lower_bound: Union[Unset, int] = UNSET
    upper_bound: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        lower_bound = self.lower_bound
        upper_bound = self.upper_bound

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if lower_bound is not UNSET:
            field_dict["lower_bound"] = lower_bound
        if upper_bound is not UNSET:
            field_dict["upper_bound"] = upper_bound

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        lower_bound = d.pop("lower_bound", UNSET)

        upper_bound = d.pop("upper_bound", UNSET)

        year_range = cls(
            name=name,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
        )

        year_range.additional_properties = d
        return year_range

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
