# flake8: noqa
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.expert import Expert


T = TypeVar("T", bound="PersonListResponse")


@attr.s(auto_attribs=True)
class PersonListResponse:
    """
    Attributes:
        experts (List['Expert']):
        previous (Union[Unset, int]):
        next_ (Union[Unset, int]):
    """

    experts: List["Expert"]
    previous: Union[Unset, int] = UNSET
    next_: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        experts = []
        for componentsschemas_experts_item_data in self.experts:
            componentsschemas_experts_item = (
                componentsschemas_experts_item_data.to_dict()
            )

            experts.append(componentsschemas_experts_item)

        previous = self.previous
        next_ = self.next_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "experts": experts,
            }
        )
        if previous is not UNSET:
            field_dict["previous"] = previous
        if next_ is not UNSET:
            field_dict["next"] = next_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.expert import Expert

        d = src_dict.copy()
        experts = []
        _experts = d.pop("experts")
        for componentsschemas_experts_item_data in _experts:
            componentsschemas_experts_item = Expert.from_dict(
                componentsschemas_experts_item_data
            )

            experts.append(componentsschemas_experts_item)

        previous = d.pop("previous", UNSET)

        next_ = d.pop("next", UNSET)

        person_list_response = cls(
            experts=experts,
            previous=previous,
            next_=next_,
        )

        person_list_response.additional_properties = d
        return person_list_response

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
