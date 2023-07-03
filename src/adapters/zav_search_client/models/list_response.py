from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.retrieval_unit import RetrievalUnit
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.hit import Hit


T = TypeVar("T", bound="ListResponse")


@attr.s(auto_attribs=True)
class ListResponse:
    """
    Attributes:
        number_of_pages (int):  Example: 1000.
        total_hits (int):  Example: 111947.
        retrieval_unit (RetrievalUnit):  Example: document.
        hits (List['Hit']):
        page (Union[Unset, float]):  Example: 1.
        took (Union[Unset, float]):  Example: 0.01.
        next_ (Union[Unset, str]):  Example:
            /document/chunk/list?property_name=guid&property_values=43436432643264_0&page=3.
        previous (Union[Unset, str]):  Example:
            /document/chunk/list?property_name=guid&property_values=43436432643264_0&page=1.
    """

    number_of_pages: int
    total_hits: int
    retrieval_unit: RetrievalUnit
    hits: List["Hit"]
    page: Union[Unset, float] = UNSET
    took: Union[Unset, float] = UNSET
    next_: Union[Unset, str] = UNSET
    previous: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        number_of_pages = self.number_of_pages
        total_hits = self.total_hits
        retrieval_unit = self.retrieval_unit.value

        hits = []
        for hits_item_data in self.hits:
            hits_item = hits_item_data.to_dict()

            hits.append(hits_item)

        page = self.page
        took = self.took
        next_ = self.next_
        previous = self.previous

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "number_of_pages": number_of_pages,
                "total_hits": total_hits,
                "retrieval_unit": retrieval_unit,
                "hits": hits,
            }
        )
        if page is not UNSET:
            field_dict["page"] = page
        if took is not UNSET:
            field_dict["took"] = took
        if next_ is not UNSET:
            field_dict["next"] = next_
        if previous is not UNSET:
            field_dict["previous"] = previous

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.hit import Hit

        d = src_dict.copy()
        number_of_pages = d.pop("number_of_pages")

        total_hits = d.pop("total_hits")

        retrieval_unit = RetrievalUnit(d.pop("retrieval_unit"))

        hits = []
        _hits = d.pop("hits")
        for hits_item_data in _hits:
            hits_item = Hit.from_dict(hits_item_data)

            hits.append(hits_item)

        page = d.pop("page", UNSET)

        took = d.pop("took", UNSET)

        next_ = d.pop("next", UNSET)

        previous = d.pop("previous", UNSET)

        list_response = cls(
            number_of_pages=number_of_pages,
            total_hits=total_hits,
            retrieval_unit=retrieval_unit,
            hits=hits,
            page=page,
            took=took,
            next_=next_,
            previous=previous,
        )

        list_response.additional_properties = d
        return list_response

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
