from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.document_search_sort_authority import DocumentSearchSortAuthority
from ..models.document_search_sort_citations import DocumentSearchSortCitations
from ..models.document_search_sort_code import DocumentSearchSortCode
from ..models.document_search_sort_date import DocumentSearchSortDate
from ..models.document_search_sort_popularity import DocumentSearchSortPopularity
from ..models.document_search_sort_source import DocumentSearchSortSource
from ..models.document_search_sort_year import DocumentSearchSortYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="DocumentSearchSort")


@attr.s(auto_attribs=True)
class DocumentSearchSort:
    """
    Attributes:
        date (Union[Unset, DocumentSearchSortDate]):
        citations (Union[Unset, DocumentSearchSortCitations]):
        source (Union[Unset, DocumentSearchSortSource]):
        year (Union[Unset, DocumentSearchSortYear]):
        authority (Union[Unset, DocumentSearchSortAuthority]):
        popularity (Union[Unset, DocumentSearchSortPopularity]):
        code (Union[Unset, DocumentSearchSortCode]):
    """

    date: Union[Unset, DocumentSearchSortDate] = UNSET
    citations: Union[Unset, DocumentSearchSortCitations] = UNSET
    source: Union[Unset, DocumentSearchSortSource] = UNSET
    year: Union[Unset, DocumentSearchSortYear] = UNSET
    authority: Union[Unset, DocumentSearchSortAuthority] = UNSET
    popularity: Union[Unset, DocumentSearchSortPopularity] = UNSET
    code: Union[Unset, DocumentSearchSortCode] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.value

        citations: Union[Unset, str] = UNSET
        if not isinstance(self.citations, Unset):
            citations = self.citations.value

        source: Union[Unset, str] = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value

        year: Union[Unset, str] = UNSET
        if not isinstance(self.year, Unset):
            year = self.year.value

        authority: Union[Unset, str] = UNSET
        if not isinstance(self.authority, Unset):
            authority = self.authority.value

        popularity: Union[Unset, str] = UNSET
        if not isinstance(self.popularity, Unset):
            popularity = self.popularity.value

        code: Union[Unset, str] = UNSET
        if not isinstance(self.code, Unset):
            code = self.code.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if date is not UNSET:
            field_dict["date"] = date
        if citations is not UNSET:
            field_dict["citations"] = citations
        if source is not UNSET:
            field_dict["source"] = source
        if year is not UNSET:
            field_dict["year"] = year
        if authority is not UNSET:
            field_dict["authority"] = authority
        if popularity is not UNSET:
            field_dict["popularity"] = popularity
        if code is not UNSET:
            field_dict["code"] = code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _date = d.pop("date", UNSET)
        date: Union[Unset, DocumentSearchSortDate]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = DocumentSearchSortDate(_date)

        _citations = d.pop("citations", UNSET)
        citations: Union[Unset, DocumentSearchSortCitations]
        if isinstance(_citations, Unset):
            citations = UNSET
        else:
            citations = DocumentSearchSortCitations(_citations)

        _source = d.pop("source", UNSET)
        source: Union[Unset, DocumentSearchSortSource]
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = DocumentSearchSortSource(_source)

        _year = d.pop("year", UNSET)
        year: Union[Unset, DocumentSearchSortYear]
        if isinstance(_year, Unset):
            year = UNSET
        else:
            year = DocumentSearchSortYear(_year)

        _authority = d.pop("authority", UNSET)
        authority: Union[Unset, DocumentSearchSortAuthority]
        if isinstance(_authority, Unset):
            authority = UNSET
        else:
            authority = DocumentSearchSortAuthority(_authority)

        _popularity = d.pop("popularity", UNSET)
        popularity: Union[Unset, DocumentSearchSortPopularity]
        if isinstance(_popularity, Unset):
            popularity = UNSET
        else:
            popularity = DocumentSearchSortPopularity(_popularity)

        _code = d.pop("code", UNSET)
        code: Union[Unset, DocumentSearchSortCode]
        if isinstance(_code, Unset):
            code = UNSET
        else:
            code = DocumentSearchSortCode(_code)

        document_search_sort = cls(
            date=date,
            citations=citations,
            source=source,
            year=year,
            authority=authority,
            popularity=popularity,
            code=code,
        )

        document_search_sort.additional_properties = d
        return document_search_sort

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
