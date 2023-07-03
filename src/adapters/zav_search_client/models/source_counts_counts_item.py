from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SourceCountsCountsItem")


@attr.s(auto_attribs=True)
class SourceCountsCountsItem:
    """
    Attributes:
        source_name (Union[Unset, str]):
        count (Union[Unset, int]):
    """

    source_name: Union[Unset, str] = UNSET
    count: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        source_name = self.source_name
        count = self.count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if source_name is not UNSET:
            field_dict["source_name"] = source_name
        if count is not UNSET:
            field_dict["count"] = count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        source_name = d.pop("source_name", UNSET)

        count = d.pop("count", UNSET)

        source_counts_counts_item = cls(
            source_name=source_name,
            count=count,
        )

        source_counts_counts_item.additional_properties = d
        return source_counts_counts_item

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
