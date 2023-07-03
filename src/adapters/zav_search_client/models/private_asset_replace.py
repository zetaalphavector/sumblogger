from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="PrivateAssetReplace")


@attr.s(auto_attribs=True)
class PrivateAssetReplace:
    """
    Attributes:
        filename (str):
    """

    filename: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        filename = self.filename

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filename": filename,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        filename = d.pop("filename")

        private_asset_replace = cls(
            filename=filename,
        )

        private_asset_replace.additional_properties = d
        return private_asset_replace

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
