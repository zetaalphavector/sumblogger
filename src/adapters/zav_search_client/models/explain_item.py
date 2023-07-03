from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.explain_evidence import ExplainEvidence


T = TypeVar("T", bound="ExplainItem")


@attr.s(auto_attribs=True)
class ExplainItem:
    """
    Attributes:
        passage (str): Query string Default: ''. Example: What is a CNN?.
        explanation (Union[Unset, str]):
        evidences (Union[Unset, List['ExplainEvidence']]):
    """

    passage: str = ""
    explanation: Union[Unset, str] = UNSET
    evidences: Union[Unset, List["ExplainEvidence"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        passage = self.passage
        explanation = self.explanation
        evidences: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.evidences, Unset):
            evidences = []
            for evidences_item_data in self.evidences:
                evidences_item = evidences_item_data.to_dict()

                evidences.append(evidences_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "passage": passage,
            }
        )
        if explanation is not UNSET:
            field_dict["explanation"] = explanation
        if evidences is not UNSET:
            field_dict["evidences"] = evidences

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.explain_evidence import ExplainEvidence

        d = src_dict.copy()
        passage = d.pop("passage")

        explanation = d.pop("explanation", UNSET)

        evidences = []
        _evidences = d.pop("evidences", UNSET)
        for evidences_item_data in _evidences or []:
            evidences_item = ExplainEvidence.from_dict(evidences_item_data)

            evidences.append(evidences_item)

        explain_item = cls(
            passage=passage,
            explanation=explanation,
            evidences=evidences,
        )

        explain_item.additional_properties = d
        return explain_item

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
