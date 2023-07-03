# flake8: noqa
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, cast

import attr

if TYPE_CHECKING:
    from ..models.creator import Creator


T = TypeVar("T", bound="HitMetadata")


@attr.s(auto_attribs=True)
class HitMetadata:
    """
    Attributes:
        identifiers (List[str]):
        creator (List['Creator']):
        abstract (Optional[str]):  Example: In this paper we discuss a novel method to do fancy stuff on difficult
            tasks..
        title (Optional[str]):  Example: Quasi-Recurrent Neural Networks.
        created (Optional[str]):  Example: 2016-11-04 00:00:00+00:00.
        date (Optional[int]):  Example: 2016.
        identifier (Optional[str]):  Example: D2085021.
        source (Optional[str]):  Example: arXiv.
    """

    identifiers: List[str]
    creator: List["Creator"]
    abstract: Optional[str]
    title: Optional[str]
    created: Optional[str]
    date: Optional[int]
    identifier: Optional[str]
    source: Optional[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        identifiers = self.identifiers

        creator = []
        for creator_item_data in self.creator:
            creator_item = creator_item_data.to_dict()

            creator.append(creator_item)

        abstract = self.abstract
        title = self.title
        created = self.created
        date = self.date
        identifier = self.identifier
        source = self.source

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "identifiers": identifiers,
                "creator": creator,
                "abstract": abstract,
                "title": title,
                "created": created,
                "date": date,
                "identifier": identifier,
                "source": source,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.creator import Creator

        d = src_dict.copy()
        identifiers = cast(List[str], d.pop("identifiers"))

        creator = []
        _creator = d.pop("creator")
        for creator_item_data in _creator:
            creator_item = Creator.from_dict(creator_item_data)

            creator.append(creator_item)

        abstract = d.pop("abstract")

        title = d.pop("title")

        created = d.pop("created")

        date = d.pop("date")

        identifier = d.pop("identifier")

        source = d.pop("source")

        hit_metadata = cls(
            identifiers=identifiers,
            creator=creator,
            abstract=abstract,
            title=title,
            created=created,
            date=date,
            identifier=identifier,
            source=source,
        )

        hit_metadata.additional_properties = d
        return hit_metadata

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
