from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.expert import Expert
    from ..models.hit import Hit


T = TypeVar("T", bound="ExpertItem")


@attr.s(auto_attribs=True)
class ExpertItem:
    """
    Attributes:
        expert (Expert): Person information
        evidence (List['Hit']):
    """

    expert: "Expert"
    evidence: List["Hit"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        expert = self.expert.to_dict()

        evidence = []
        for evidence_item_data in self.evidence:
            evidence_item = evidence_item_data.to_dict()

            evidence.append(evidence_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expert": expert,
                "evidence": evidence,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.expert import Expert
        from ..models.hit import Hit

        d = src_dict.copy()
        expert = Expert.from_dict(d.pop("expert"))

        evidence = []
        _evidence = d.pop("evidence")
        for evidence_item_data in _evidence:
            evidence_item = Hit.from_dict(evidence_item_data)

            evidence.append(evidence_item)

        expert_item = cls(
            expert=expert,
            evidence=evidence,
        )

        expert_item.additional_properties = d
        return expert_item

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
