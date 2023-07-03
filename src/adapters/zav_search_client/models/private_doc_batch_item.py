from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="PrivateDocBatchItem")


@attr.s(auto_attribs=True)
class PrivateDocBatchItem:
    """
    Attributes:
        batch_id (int):
        batch_name (str):
        batch_file_name (str):
    """

    batch_id: int
    batch_name: str
    batch_file_name: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        batch_id = self.batch_id
        batch_name = self.batch_name
        batch_file_name = self.batch_file_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "batch_id": batch_id,
                "batch_name": batch_name,
                "batch_file_name": batch_file_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        batch_id = d.pop("batch_id")

        batch_name = d.pop("batch_name")

        batch_file_name = d.pop("batch_file_name")

        private_doc_batch_item = cls(
            batch_id=batch_id,
            batch_name=batch_name,
            batch_file_name=batch_file_name,
        )

        private_doc_batch_item.additional_properties = d
        return private_doc_batch_item

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
