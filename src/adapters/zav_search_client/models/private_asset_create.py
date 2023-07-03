from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PrivateAssetCreate")


@attr.s(auto_attribs=True)
class PrivateAssetCreate:
    """
    Attributes:
        filename (str):
        private_doc_id (Union[Unset, str]):
    """

    filename: str
    private_doc_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        filename = self.filename
        private_doc_id = self.private_doc_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filename": filename,
            }
        )
        if private_doc_id is not UNSET:
            field_dict["private_doc_id"] = private_doc_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        filename = d.pop("filename")

        private_doc_id = d.pop("private_doc_id", UNSET)

        private_asset_create = cls(
            filename=filename,
            private_doc_id=private_doc_id,
        )

        private_asset_create.additional_properties = d
        return private_asset_create

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
