from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Expert")


@attr.s(auto_attribs=True)
class Expert:
    """Person information

    Attributes:
        full_name (str):  Example: John Doe.
        uid (str):  Example: PE_00284294.
        affiliations (Union[Unset, List[str]]):
        city (Union[Unset, None, str]):  Example: Amsterdam.
        country (Union[Unset, None, str]):  Example: The Netherlands.
        number_of_publications (Union[Unset, None, int]):  Example: 10.
        h_index (Union[Unset, None, int]):  Example: 2.
        picture (Union[Unset, None, str]):  Example: http://cdn.picture.it/john.
        first_name (Union[Unset, None, str]):  Example: John.
        last_name (Union[Unset, None, str]):  Example: Doe.
    """

    full_name: str
    uid: str
    affiliations: Union[Unset, List[str]] = UNSET
    city: Union[Unset, None, str] = UNSET
    country: Union[Unset, None, str] = UNSET
    number_of_publications: Union[Unset, None, int] = UNSET
    h_index: Union[Unset, None, int] = UNSET
    picture: Union[Unset, None, str] = UNSET
    first_name: Union[Unset, None, str] = UNSET
    last_name: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        full_name = self.full_name
        uid = self.uid
        affiliations: Union[Unset, List[str]] = UNSET
        if not isinstance(self.affiliations, Unset):
            affiliations = self.affiliations

        city = self.city
        country = self.country
        number_of_publications = self.number_of_publications
        h_index = self.h_index
        picture = self.picture
        first_name = self.first_name
        last_name = self.last_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "full_name": full_name,
                "uid": uid,
            }
        )
        if affiliations is not UNSET:
            field_dict["affiliations"] = affiliations
        if city is not UNSET:
            field_dict["city"] = city
        if country is not UNSET:
            field_dict["country"] = country
        if number_of_publications is not UNSET:
            field_dict["number_of_publications"] = number_of_publications
        if h_index is not UNSET:
            field_dict["h_index"] = h_index
        if picture is not UNSET:
            field_dict["picture"] = picture
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        full_name = d.pop("full_name")

        uid = d.pop("uid")

        affiliations = cast(List[str], d.pop("affiliations", UNSET))

        city = d.pop("city", UNSET)

        country = d.pop("country", UNSET)

        number_of_publications = d.pop("number_of_publications", UNSET)

        h_index = d.pop("h_index", UNSET)

        picture = d.pop("picture", UNSET)

        first_name = d.pop("first_name", UNSET)

        last_name = d.pop("last_name", UNSET)

        expert = cls(
            full_name=full_name,
            uid=uid,
            affiliations=affiliations,
            city=city,
            country=country,
            number_of_publications=number_of_publications,
            h_index=h_index,
            picture=picture,
            first_name=first_name,
            last_name=last_name,
        )

        expert.additional_properties = d
        return expert

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
