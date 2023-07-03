from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.best_answer_evidence import BestAnswerEvidence


T = TypeVar("T", bound="BestAnswerItem")


@attr.s(auto_attribs=True)
class BestAnswerItem:
    """
    Attributes:
        original_question (str): Query string Default: ''. Example: What is a CNN?.
        question (str): Query string Default: ''. Example: What is a CNN?.
        answer (Union[Unset, str]):
        evidences (Union[Unset, List['BestAnswerEvidence']]):
        explanation (Union[Unset, str]):
    """

    original_question: str = ""
    question: str = ""
    answer: Union[Unset, str] = UNSET
    evidences: Union[Unset, List["BestAnswerEvidence"]] = UNSET
    explanation: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        original_question = self.original_question
        question = self.question
        answer = self.answer
        evidences: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.evidences, Unset):
            evidences = []
            for evidences_item_data in self.evidences:
                evidences_item = evidences_item_data.to_dict()

                evidences.append(evidences_item)

        explanation = self.explanation

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "original_question": original_question,
                "question": question,
            }
        )
        if answer is not UNSET:
            field_dict["answer"] = answer
        if evidences is not UNSET:
            field_dict["evidences"] = evidences
        if explanation is not UNSET:
            field_dict["explanation"] = explanation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.best_answer_evidence import BestAnswerEvidence

        d = src_dict.copy()
        original_question = d.pop("original_question")

        question = d.pop("question")

        answer = d.pop("answer", UNSET)

        evidences = []
        _evidences = d.pop("evidences", UNSET)
        for evidences_item_data in _evidences or []:
            evidences_item = BestAnswerEvidence.from_dict(evidences_item_data)

            evidences.append(evidences_item)

        explanation = d.pop("explanation", UNSET)

        best_answer_item = cls(
            original_question=original_question,
            question=question,
            answer=answer,
            evidences=evidences,
            explanation=explanation,
        )

        best_answer_item.additional_properties = d
        return best_answer_item

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
