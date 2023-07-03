from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.entity import Entity


T = TypeVar("T", bound="ParsedEntity")


@attr.s(auto_attribs=True)
class ParsedEntity:
    """Parsed entity from query string

    Attributes:
        start_offset (int):
        end_offset (int):  Example: 3.
        entity (Entity): Entity representation
    """

    start_offset: int
    end_offset: int
    entity: "Entity"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        start_offset = self.start_offset
        end_offset = self.end_offset
        entity = self.entity.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_offset": start_offset,
                "end_offset": end_offset,
                "entity": entity,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.entity import Entity

        d = src_dict.copy()
        start_offset = d.pop("start_offset")

        end_offset = d.pop("end_offset")

        entity = Entity.from_dict(d.pop("entity"))

        parsed_entity = cls(
            start_offset=start_offset,
            end_offset=end_offset,
            entity=entity,
        )

        parsed_entity.additional_properties = d
        return parsed_entity

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
