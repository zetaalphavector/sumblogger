from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.expert_response_retrieval_method import ExpertResponseRetrievalMethod
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.expert_item import ExpertItem


T = TypeVar("T", bound="ExpertResponse")


@attr.s(auto_attribs=True)
class ExpertResponse:
    """
    Attributes:
        retrieval_method (ExpertResponseRetrievalMethod):  Example: keyword.
        query_string (str):  Example: Recurrent Neural Networks.
        total_hits (int):  Example: 16.
        took (float):  Example: 0.01.
        experts (List['ExpertItem']):
        page (Union[Unset, int]):  Example: 1.
        number_of_pages (Union[Unset, int]):  Example: 2.
        next_ (Union[Unset, str]):  Example:
            /v1.1/entities/person/search?page=2&query_string=CNN&retrieval_method=keyword.
        previous (Union[Unset, str]):
    """

    retrieval_method: ExpertResponseRetrievalMethod
    query_string: str
    total_hits: int
    took: float
    experts: List["ExpertItem"]
    page: Union[Unset, int] = UNSET
    number_of_pages: Union[Unset, int] = UNSET
    next_: Union[Unset, str] = UNSET
    previous: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        retrieval_method = self.retrieval_method.value

        query_string = self.query_string
        total_hits = self.total_hits
        took = self.took
        experts = []
        for experts_item_data in self.experts:
            experts_item = experts_item_data.to_dict()

            experts.append(experts_item)

        page = self.page
        number_of_pages = self.number_of_pages
        next_ = self.next_
        previous = self.previous

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "retrieval_method": retrieval_method,
                "query_string": query_string,
                "total_hits": total_hits,
                "took": took,
                "experts": experts,
            }
        )
        if page is not UNSET:
            field_dict["page"] = page
        if number_of_pages is not UNSET:
            field_dict["number_of_pages"] = number_of_pages
        if next_ is not UNSET:
            field_dict["next"] = next_
        if previous is not UNSET:
            field_dict["previous"] = previous

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.expert_item import ExpertItem

        d = src_dict.copy()
        retrieval_method = ExpertResponseRetrievalMethod(d.pop("retrieval_method"))

        query_string = d.pop("query_string")

        total_hits = d.pop("total_hits")

        took = d.pop("took")

        experts = []
        _experts = d.pop("experts")
        for experts_item_data in _experts:
            experts_item = ExpertItem.from_dict(experts_item_data)

            experts.append(experts_item)

        page = d.pop("page", UNSET)

        number_of_pages = d.pop("number_of_pages", UNSET)

        next_ = d.pop("next", UNSET)

        previous = d.pop("previous", UNSET)

        expert_response = cls(
            retrieval_method=retrieval_method,
            query_string=query_string,
            total_hits=total_hits,
            took=took,
            experts=experts,
            page=page,
            number_of_pages=number_of_pages,
            next_=next_,
            previous=previous,
        )

        expert_response.additional_properties = d
        return expert_response

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
