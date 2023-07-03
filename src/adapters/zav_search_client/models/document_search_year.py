from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DocumentSearchYear")


@attr.s(auto_attribs=True)
class DocumentSearchYear:
    """
    Attributes:
        lower_bound (Union[Unset, str]):  Example: 2010.
        upper_bound (Union[Unset, str]):  Example: 2019.
    """

    lower_bound: Union[Unset, str] = UNSET
    upper_bound: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        lower_bound = self.lower_bound
        upper_bound = self.upper_bound

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if lower_bound is not UNSET:
            field_dict["lower_bound"] = lower_bound
        if upper_bound is not UNSET:
            field_dict["upper_bound"] = upper_bound

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        lower_bound = d.pop("lower_bound", UNSET)

        upper_bound = d.pop("upper_bound", UNSET)

        document_search_year = cls(
            lower_bound=lower_bound,
            upper_bound=upper_bound,
        )

        document_search_year.additional_properties = d
        return document_search_year

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
