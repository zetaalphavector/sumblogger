from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SourceListItem")


@attr.s(auto_attribs=True)
class SourceListItem:
    """
    Attributes:
        title (str):
        identifiers (Union[Unset, List[str]]):
        subsources (Union[Unset, List['SourceListItem']]):
    """

    title: str
    identifiers: Union[Unset, List[str]] = UNSET
    subsources: Union[Unset, List["SourceListItem"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        identifiers: Union[Unset, List[str]] = UNSET
        if not isinstance(self.identifiers, Unset):
            identifiers = self.identifiers

        subsources: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.subsources, Unset):
            subsources = []
            for subsources_item_data in self.subsources:
                subsources_item = subsources_item_data.to_dict()

                subsources.append(subsources_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
            }
        )
        if identifiers is not UNSET:
            field_dict["identifiers"] = identifiers
        if subsources is not UNSET:
            field_dict["subsources"] = subsources

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title")

        identifiers = cast(List[str], d.pop("identifiers", UNSET))

        subsources = []
        _subsources = d.pop("subsources", UNSET)
        for subsources_item_data in _subsources or []:
            subsources_item = SourceListItem.from_dict(subsources_item_data)

            subsources.append(subsources_item)

        source_list_item = cls(
            title=title,
            identifiers=identifiers,
            subsources=subsources,
        )

        source_list_item.additional_properties = d
        return source_list_item

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
