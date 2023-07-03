from typing import Any, Dict, List, Optional, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="PrivateDocMetadata")


@attr.s(auto_attribs=True)
class PrivateDocMetadata:
    """
    Attributes:
        authors (List[str]):
        title (Optional[str]):
        abstract_text (Optional[str]):
        year (Optional[int]):
        source (Optional[str]):
    """

    authors: List[str]
    title: Optional[str]
    abstract_text: Optional[str]
    year: Optional[int]
    source: Optional[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        authors = self.authors

        title = self.title
        abstract_text = self.abstract_text
        year = self.year
        source = self.source

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "authors": authors,
                "title": title,
                "abstract_text": abstract_text,
                "year": year,
                "source": source,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        authors = cast(List[str], d.pop("authors"))

        title = d.pop("title")

        abstract_text = d.pop("abstract_text")

        year = d.pop("year")

        source = d.pop("source")

        private_doc_metadata = cls(
            authors=authors,
            title=title,
            abstract_text=abstract_text,
            year=year,
            source=source,
        )

        private_doc_metadata.additional_properties = d
        return private_doc_metadata

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
