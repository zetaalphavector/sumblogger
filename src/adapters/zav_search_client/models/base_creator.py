from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="BaseCreator")


@attr.s(auto_attribs=True)
class BaseCreator:
    """
    Attributes:
        full_name (str):  Example: John Doe.
        uid (str):  Example: PE_00284294.
    """

    full_name: str
    uid: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        full_name = self.full_name
        uid = self.uid

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "full_name": full_name,
                "uid": uid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        full_name = d.pop("full_name")

        uid = d.pop("uid")

        base_creator = cls(
            full_name=full_name,
            uid=uid,
        )

        base_creator.additional_properties = d
        return base_creator

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
