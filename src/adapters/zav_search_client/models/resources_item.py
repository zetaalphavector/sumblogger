from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="ResourcesItem")


@attr.s(auto_attribs=True)
class ResourcesItem:
    """
    Attributes:
        resource_type (str):
        resource_value (str):
    """

    resource_type: str
    resource_value: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        resource_type = self.resource_type
        resource_value = self.resource_value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_type": resource_type,
                "resource_value": resource_value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        resource_type = d.pop("resource_type")

        resource_value = d.pop("resource_value")

        resources_item = cls(
            resource_type=resource_type,
            resource_value=resource_value,
        )

        resources_item.additional_properties = d
        return resources_item

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
