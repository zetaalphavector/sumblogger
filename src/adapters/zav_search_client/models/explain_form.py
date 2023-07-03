from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.retrieval_unit import RetrievalUnit
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExplainForm")


@attr.s(auto_attribs=True)
class ExplainForm:
    """
    Attributes:
        document_ids (List[str]):
        passage (str): Query string Default: ''. Example: What is a CNN?.
        retrieval_unit (RetrievalUnit):  Example: document.
        context_fields (List[str]):
        prompt_template (Union[Unset, str]):
    """

    document_ids: List[str]
    retrieval_unit: RetrievalUnit
    context_fields: List[str]
    passage: str = ""
    prompt_template: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        document_ids = self.document_ids

        passage = self.passage
        retrieval_unit = self.retrieval_unit.value

        context_fields = self.context_fields

        prompt_template = self.prompt_template

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "document_ids": document_ids,
                "passage": passage,
                "retrieval_unit": retrieval_unit,
                "context_fields": context_fields,
            }
        )
        if prompt_template is not UNSET:
            field_dict["prompt_template"] = prompt_template

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        document_ids = cast(List[str], d.pop("document_ids"))

        passage = d.pop("passage")

        retrieval_unit = RetrievalUnit(d.pop("retrieval_unit"))

        context_fields = cast(List[str], d.pop("context_fields"))

        prompt_template = d.pop("prompt_template", UNSET)

        explain_form = cls(
            document_ids=document_ids,
            passage=passage,
            retrieval_unit=retrieval_unit,
            context_fields=context_fields,
            prompt_template=prompt_template,
        )

        explain_form.additional_properties = d
        return explain_form

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
