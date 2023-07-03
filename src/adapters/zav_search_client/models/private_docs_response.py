from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.page_params import PageParams
    from ..models.private_doc_item import PrivateDocItem


T = TypeVar("T", bound="PrivateDocsResponse")


@attr.s(auto_attribs=True)
class PrivateDocsResponse:
    """
    Attributes:
        count (float):
        results (List['PrivateDocItem']):
        next_ (Union[Unset, PageParams]):
        previous (Union[Unset, PageParams]):
    """

    count: float
    results: List["PrivateDocItem"]
    next_: Union[Unset, "PageParams"] = UNSET
    previous: Union[Unset, "PageParams"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        count = self.count
        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()

            results.append(results_item)

        next_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.next_, Unset):
            next_ = self.next_.to_dict()

        previous: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.previous, Unset):
            previous = self.previous.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
                "results": results,
            }
        )
        if next_ is not UNSET:
            field_dict["next"] = next_
        if previous is not UNSET:
            field_dict["previous"] = previous

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.page_params import PageParams
        from ..models.private_doc_item import PrivateDocItem

        d = src_dict.copy()
        count = d.pop("count")

        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = PrivateDocItem.from_dict(results_item_data)

            results.append(results_item)

        _next_ = d.pop("next", UNSET)
        next_: Union[Unset, PageParams]
        if isinstance(_next_, Unset):
            next_ = UNSET
        else:
            next_ = PageParams.from_dict(_next_)

        _previous = d.pop("previous", UNSET)
        previous: Union[Unset, PageParams]
        if isinstance(_previous, Unset):
            previous = UNSET
        else:
            previous = PageParams.from_dict(_previous)

        private_docs_response = cls(
            count=count,
            results=results,
            next_=next_,
            previous=previous,
        )

        private_docs_response.additional_properties = d
        return private_docs_response

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
