# flake8: noqa
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.base_creator import BaseCreator


T = TypeVar("T", bound="ExternalDocFormMetadata")


@attr.s(auto_attribs=True)
class ExternalDocFormMetadata:
    """
    Attributes:
        title (str):  Example: Quasi-Recurrent Neural Networks.
        created_at (str):  Example: 2016-11-04 00:00:00+00:00.
        authors (List['BaseCreator']):
        abstract (Optional[str]):  Example: In this paper we discuss a novel method to do fancy stuff on difficult
            tasks..
        source (Optional[str]):  Example: arXiv.
    """

    title: str
    created_at: str
    authors: List["BaseCreator"]
    abstract: Optional[str]
    source: Optional[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        created_at = self.created_at
        authors = []
        for authors_item_data in self.authors:
            authors_item = authors_item_data.to_dict()

            authors.append(authors_item)

        abstract = self.abstract
        source = self.source

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "created_at": created_at,
                "authors": authors,
                "abstract": abstract,
                "source": source,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.base_creator import BaseCreator

        d = src_dict.copy()
        title = d.pop("title")

        created_at = d.pop("created_at")

        authors = []
        _authors = d.pop("authors")
        for authors_item_data in _authors:
            authors_item = BaseCreator.from_dict(authors_item_data)

            authors.append(authors_item)

        abstract = d.pop("abstract")

        source = d.pop("source")

        external_doc_form_metadata = cls(
            title=title,
            created_at=created_at,
            authors=authors,
            abstract=abstract,
            source=source,
        )

        external_doc_form_metadata.additional_properties = d
        return external_doc_form_metadata

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
