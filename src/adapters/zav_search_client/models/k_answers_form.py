from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.retrieval_unit import RetrievalUnit
from ..types import UNSET, Unset

T = TypeVar("T", bound="KAnswersForm")


@attr.s(auto_attribs=True)
class KAnswersForm:
    """
    Attributes:
        document_id (str):  Example: 07389afefe1b087aee5523cae78f105ce78f105c_0.
        question (str): Query string Default: ''. Example: What is a CNN?.
        reformulate_question (bool):  Default: True.
        retrieval_unit (RetrievalUnit):  Example: document.
        context_fields (List[str]):
        prompt_template (Union[Unset, str]):
    """

    document_id: str
    retrieval_unit: RetrievalUnit
    context_fields: List[str]
    question: str = ""
    reformulate_question: bool = True
    prompt_template: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        document_id = self.document_id
        question = self.question
        reformulate_question = self.reformulate_question
        retrieval_unit = self.retrieval_unit.value

        context_fields = self.context_fields

        prompt_template = self.prompt_template

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "document_id": document_id,
                "question": question,
                "reformulate_question": reformulate_question,
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
        document_id = d.pop("document_id")

        question = d.pop("question")

        reformulate_question = d.pop("reformulate_question")

        retrieval_unit = RetrievalUnit(d.pop("retrieval_unit"))

        context_fields = cast(List[str], d.pop("context_fields"))

        prompt_template = d.pop("prompt_template", UNSET)

        k_answers_form = cls(
            document_id=document_id,
            question=question,
            reformulate_question=reformulate_question,
            retrieval_unit=retrieval_unit,
            context_fields=context_fields,
            prompt_template=prompt_template,
        )

        k_answers_form.additional_properties = d
        return k_answers_form

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
