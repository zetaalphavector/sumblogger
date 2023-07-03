from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PrivateAssetCreateResponse")


@attr.s(auto_attribs=True)
class PrivateAssetCreateResponse:
    """
    Attributes:
        private_asset_id (str):
        upload_url (str):
        filename (str):
        private_doc_id (Union[Unset, str]):
    """

    private_asset_id: str
    upload_url: str
    filename: str
    private_doc_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        private_asset_id = self.private_asset_id
        upload_url = self.upload_url
        filename = self.filename
        private_doc_id = self.private_doc_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "private_asset_id": private_asset_id,
                "upload_url": upload_url,
                "filename": filename,
            }
        )
        if private_doc_id is not UNSET:
            field_dict["private_doc_id"] = private_doc_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        private_asset_id = d.pop("private_asset_id")

        upload_url = d.pop("upload_url")

        filename = d.pop("filename")

        private_doc_id = d.pop("private_doc_id", UNSET)

        private_asset_create_response = cls(
            private_asset_id=private_asset_id,
            upload_url=upload_url,
            filename=filename,
            private_doc_id=private_doc_id,
        )

        private_asset_create_response.additional_properties = d
        return private_asset_create_response

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
