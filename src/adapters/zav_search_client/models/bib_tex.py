# flake8: noqa
from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="BibTex")


@attr.s(auto_attribs=True)
class BibTex:
    """
    Attributes:
        uid (str):  Example: 07389afefe1b087aee5523cae78f105ce78f105c_e49f6dbb-0136-4707-a4ee-a02bbc8a8d9a.
        value (str):  Example: @inproceedings{you2019isanaffine,
                author = {Chong You and Chunyuan Li and Daniel P Robinson and Rene Vidal},
                title = {Is an affine constraint needed for affine subspace clustering?},
             year = 2019,
                booktitle = {ICLR},
                pages = {1--2},
                volume = {2}
            }
            .
    """

    uid: str
    value: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uid = self.uid
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uid": uid,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        uid = d.pop("uid")

        value = d.pop("value")

        bib_tex = cls(
            uid=uid,
            value=value,
        )

        bib_tex.additional_properties = d
        return bib_tex

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
