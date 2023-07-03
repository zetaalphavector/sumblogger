from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Creator")


@attr.s(auto_attribs=True)
class Creator:
    """
    Attributes:
        full_name (str):  Example: John Doe.
        uid (str):  Example: PE_00284294.
        first_name (Union[Unset, str]):  Example: John.
        last_name (Union[Unset, str]):  Example: Doe.
        h_index (Union[Unset, int]):  Example: 4.
        affiliations (Union[Unset, List[str]]):
        city (Union[Unset, str]):  Example: Amsterdam.
        country (Union[Unset, str]):  Example: Netherlands.
    """

    full_name: str
    uid: str
    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    h_index: Union[Unset, int] = UNSET
    affiliations: Union[Unset, List[str]] = UNSET
    city: Union[Unset, str] = UNSET
    country: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        full_name = self.full_name
        uid = self.uid
        first_name = self.first_name
        last_name = self.last_name
        h_index = self.h_index
        affiliations: Union[Unset, List[str]] = UNSET
        if not isinstance(self.affiliations, Unset):
            affiliations = self.affiliations

        city = self.city
        country = self.country

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "full_name": full_name,
                "uid": uid,
            }
        )
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if h_index is not UNSET:
            field_dict["h_index"] = h_index
        if affiliations is not UNSET:
            field_dict["affiliations"] = affiliations
        if city is not UNSET:
            field_dict["city"] = city
        if country is not UNSET:
            field_dict["country"] = country

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        full_name = d.pop("full_name")

        uid = d.pop("uid")

        first_name = d.pop("first_name", UNSET)

        last_name = d.pop("last_name", UNSET)

        h_index = d.pop("h_index", UNSET)

        affiliations = cast(List[str], d.pop("affiliations", UNSET))

        city = d.pop("city", UNSET)

        country = d.pop("country", UNSET)

        creator = cls(
            full_name=full_name,
            uid=uid,
            first_name=first_name,
            last_name=last_name,
            h_index=h_index,
            affiliations=affiliations,
            city=city,
            country=country,
        )

        creator.additional_properties = d
        return creator

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
