from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExplainEvidence")


@attr.s(auto_attribs=True)
class ExplainEvidence:
    """
    Attributes:
        document_id (Union[Unset, str]):
        text_extract (Union[Unset, str]):
    """

    document_id: Union[Unset, str] = UNSET
    text_extract: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        document_id = self.document_id
        text_extract = self.text_extract

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if document_id is not UNSET:
            field_dict["document_id"] = document_id
        if text_extract is not UNSET:
            field_dict["text_extract"] = text_extract

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        document_id = d.pop("document_id", UNSET)

        text_extract = d.pop("text_extract", UNSET)

        explain_evidence = cls(
            document_id=document_id,
            text_extract=text_extract,
        )

        explain_evidence.additional_properties = d
        return explain_evidence

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
