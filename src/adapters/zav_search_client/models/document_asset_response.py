from typing import Any, Dict, List, Optional, Type, TypeVar

import attr

T = TypeVar("T", bound="DocumentAssetResponse")


@attr.s(auto_attribs=True)
class DocumentAssetResponse:
    """
    Attributes:
        download_url (str):
        file_size (Optional[int]):
    """

    download_url: str
    file_size: Optional[int]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        download_url = self.download_url
        file_size = self.file_size

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "download_url": download_url,
                "file_size": file_size,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        download_url = d.pop("download_url")

        file_size = d.pop("file_size")

        document_asset_response = cls(
            download_url=download_url,
            file_size=file_size,
        )

        document_asset_response.additional_properties = d
        return document_asset_response

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
