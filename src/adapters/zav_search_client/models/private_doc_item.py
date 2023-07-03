from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.private_doc_metadata import PrivateDocMetadata


T = TypeVar("T", bound="PrivateDocItem")


@attr.s(auto_attribs=True)
class PrivateDocItem:
    """
    Attributes:
        id (str):  Example: 07389afefe1b087aee5523cae78f105ce78f105c_0.
        guid (str):  Example: 07389afefe1b087aee5523cae78f105ce78f105c.
        date_created (str):
        metadata (PrivateDocMetadata):
        organize_doc_id (str):  Example: 2cd44b68b00e0355684f7c940b2c7bd9329050f5_0.
        date_modified (Optional[str]):
        uri (Optional[str]):
        access_roles (Union[Unset, List[str]]):
        private_asset_id (Union[Unset, None, str]):
    """

    id: str
    guid: str
    date_created: str
    metadata: "PrivateDocMetadata"
    organize_doc_id: str
    date_modified: Optional[str]
    uri: Optional[str]
    access_roles: Union[Unset, List[str]] = UNSET
    private_asset_id: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        guid = self.guid
        date_created = self.date_created
        metadata = self.metadata.to_dict()

        organize_doc_id = self.organize_doc_id
        date_modified = self.date_modified
        uri = self.uri
        access_roles: Union[Unset, List[str]] = UNSET
        if not isinstance(self.access_roles, Unset):
            access_roles = self.access_roles

        private_asset_id = self.private_asset_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "guid": guid,
                "date_created": date_created,
                "metadata": metadata,
                "organize_doc_id": organize_doc_id,
                "date_modified": date_modified,
                "uri": uri,
            }
        )
        if access_roles is not UNSET:
            field_dict["access_roles"] = access_roles
        if private_asset_id is not UNSET:
            field_dict["private_asset_id"] = private_asset_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.private_doc_metadata import PrivateDocMetadata

        d = src_dict.copy()
        id = d.pop("id")

        guid = d.pop("guid")

        date_created = d.pop("date_created")

        metadata = PrivateDocMetadata.from_dict(d.pop("metadata"))

        organize_doc_id = d.pop("organize_doc_id")

        date_modified = d.pop("date_modified")

        uri = d.pop("uri")

        access_roles = cast(List[str], d.pop("access_roles", UNSET))

        private_asset_id = d.pop("private_asset_id", UNSET)

        private_doc_item = cls(
            id=id,
            guid=guid,
            date_created=date_created,
            metadata=metadata,
            organize_doc_id=organize_doc_id,
            date_modified=date_modified,
            uri=uri,
            access_roles=access_roles,
            private_asset_id=private_asset_id,
        )

        private_doc_item.additional_properties = d
        return private_doc_item

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
