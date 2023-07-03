# flake8: noqa
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar

import attr

from ..models.document_type_string import DocumentTypeString
from ..models.search_engine_string import SearchEngineString

if TYPE_CHECKING:
    from ..models.external_doc_form_metadata import ExternalDocFormMetadata
    from ..models.resources_item import ResourcesItem


T = TypeVar("T", bound="ExternalDocForm")


@attr.s(auto_attribs=True)
class ExternalDocForm:
    """
    Attributes:
        id (str):  Example: 07389afefe1b087aee5523cae78f105ce78f105c_0.
        uid (str):  Example: CO_100456.
        guid (str):  Example: 07389afefe1b087aee5523cae78f105ce78f105c.
        search_engine (SearchEngineString):
        resources (List['ResourcesItem']):
        document_type (DocumentTypeString):
        metadata (ExternalDocFormMetadata):
        uri (Optional[str]):  Example: https://arxiv.org/abs/1611.01576.
        cited_by_count (Optional[int]):
    """

    id: str
    uid: str
    guid: str
    search_engine: SearchEngineString
    resources: List["ResourcesItem"]
    document_type: DocumentTypeString
    metadata: "ExternalDocFormMetadata"
    uri: Optional[str]
    cited_by_count: Optional[int]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        uid = self.uid
        guid = self.guid
        search_engine = self.search_engine.value

        resources = []
        for componentsschemas_resources_item_data in self.resources:
            componentsschemas_resources_item = (
                componentsschemas_resources_item_data.to_dict()
            )

            resources.append(componentsschemas_resources_item)

        document_type = self.document_type.value

        metadata = self.metadata.to_dict()

        uri = self.uri
        cited_by_count = self.cited_by_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "uid": uid,
                "guid": guid,
                "search_engine": search_engine,
                "resources": resources,
                "document_type": document_type,
                "metadata": metadata,
                "uri": uri,
                "cited_by_count": cited_by_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.external_doc_form_metadata import ExternalDocFormMetadata
        from ..models.resources_item import ResourcesItem

        d = src_dict.copy()
        id = d.pop("id")

        uid = d.pop("uid")

        guid = d.pop("guid")

        search_engine = SearchEngineString(d.pop("search_engine"))

        resources = []
        _resources = d.pop("resources")
        for componentsschemas_resources_item_data in _resources:
            componentsschemas_resources_item = ResourcesItem.from_dict(
                componentsschemas_resources_item_data
            )

            resources.append(componentsschemas_resources_item)

        document_type = DocumentTypeString(d.pop("document_type"))

        metadata = ExternalDocFormMetadata.from_dict(d.pop("metadata"))

        uri = d.pop("uri")

        cited_by_count = d.pop("cited_by_count")

        external_doc_form = cls(
            id=id,
            uid=uid,
            guid=guid,
            search_engine=search_engine,
            resources=resources,
            document_type=document_type,
            metadata=metadata,
            uri=uri,
            cited_by_count=cited_by_count,
        )

        external_doc_form.additional_properties = d
        return external_doc_form

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
