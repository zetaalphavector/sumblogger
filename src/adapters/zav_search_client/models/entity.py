from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Entity")


@attr.s(auto_attribs=True)
class Entity:
    """Entity representation

    Attributes:
        entity_type (str):  Example: CONCEPTS.
        entity_class (str):  Example: Machine Learning Algorithm.
        name (str):  Example: CNN.
        uid (str):  Example: EN_1000443.
        node_type (Union[Unset, str]):  Example: instance.
    """

    entity_type: str
    entity_class: str
    name: str
    uid: str
    node_type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        entity_type = self.entity_type
        entity_class = self.entity_class
        name = self.name
        uid = self.uid
        node_type = self.node_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entity_type": entity_type,
                "entity_class": entity_class,
                "name": name,
                "uid": uid,
            }
        )
        if node_type is not UNSET:
            field_dict["node_type"] = node_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity_type = d.pop("entity_type")

        entity_class = d.pop("entity_class")

        name = d.pop("name")

        uid = d.pop("uid")

        node_type = d.pop("node_type", UNSET)

        entity = cls(
            entity_type=entity_type,
            entity_class=entity_class,
            name=name,
            uid=uid,
            node_type=node_type,
        )

        entity.additional_properties = d
        return entity

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
