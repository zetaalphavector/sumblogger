from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PrivateAssetRetrieveResponse")


@attr.s(auto_attribs=True)
class PrivateAssetRetrieveResponse:
    """
    Attributes:
        private_asset_id (str):
        download_url (str):
        filename (str):
        file_size (Optional[int]):
        private_doc_id (Union[Unset, str]):
    """

    private_asset_id: str
    download_url: str
    filename: str
    file_size: Optional[int]
    private_doc_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        private_asset_id = self.private_asset_id
        download_url = self.download_url
        filename = self.filename
        file_size = self.file_size
        private_doc_id = self.private_doc_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "private_asset_id": private_asset_id,
                "download_url": download_url,
                "filename": filename,
                "file_size": file_size,
            }
        )
        if private_doc_id is not UNSET:
            field_dict["private_doc_id"] = private_doc_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        private_asset_id = d.pop("private_asset_id")

        download_url = d.pop("download_url")

        filename = d.pop("filename")

        file_size = d.pop("file_size")

        private_doc_id = d.pop("private_doc_id", UNSET)

        private_asset_retrieve_response = cls(
            private_asset_id=private_asset_id,
            download_url=download_url,
            filename=filename,
            file_size=file_size,
            private_doc_id=private_doc_id,
        )

        private_asset_retrieve_response.additional_properties = d
        return private_asset_retrieve_response

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
