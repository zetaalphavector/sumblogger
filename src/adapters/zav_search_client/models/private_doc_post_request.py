from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, cast

import attr

if TYPE_CHECKING:
    from ..models.private_doc_metadata import PrivateDocMetadata


T = TypeVar("T", bound="PrivateDocPostRequest")


@attr.s(auto_attribs=True)
class PrivateDocPostRequest:
    """
    Attributes:
        metadata (PrivateDocMetadata):
        access_roles (List[str]):
        uri (Optional[str]):
        private_asset_id (Optional[str]):
    """

    metadata: "PrivateDocMetadata"
    access_roles: List[str]
    uri: Optional[str]
    private_asset_id: Optional[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        metadata = self.metadata.to_dict()

        access_roles = self.access_roles

        uri = self.uri
        private_asset_id = self.private_asset_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadata": metadata,
                "access_roles": access_roles,
                "uri": uri,
                "private_asset_id": private_asset_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.private_doc_metadata import PrivateDocMetadata

        d = src_dict.copy()
        metadata = PrivateDocMetadata.from_dict(d.pop("metadata"))

        access_roles = cast(List[str], d.pop("access_roles"))

        uri = d.pop("uri")

        private_asset_id = d.pop("private_asset_id")

        private_doc_post_request = cls(
            metadata=metadata,
            access_roles=access_roles,
            uri=uri,
            private_asset_id=private_asset_id,
        )

        private_doc_post_request.additional_properties = d
        return private_doc_post_request

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
