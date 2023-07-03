from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="PrivateDocBatchPostRequest")


@attr.s(auto_attribs=True)
class PrivateDocBatchPostRequest:
    """
    Attributes:
        batch_name (str):
        batch_file_name (str):
        batch_file_contents (str):
        access_roles (List[str]):
    """

    batch_name: str
    batch_file_name: str
    batch_file_contents: str
    access_roles: List[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        batch_name = self.batch_name
        batch_file_name = self.batch_file_name
        batch_file_contents = self.batch_file_contents
        access_roles = self.access_roles

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "batch_name": batch_name,
                "batch_file_name": batch_file_name,
                "batch_file_contents": batch_file_contents,
                "access_roles": access_roles,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        batch_name = d.pop("batch_name")

        batch_file_name = d.pop("batch_file_name")

        batch_file_contents = d.pop("batch_file_contents")

        access_roles = cast(List[str], d.pop("access_roles"))

        private_doc_batch_post_request = cls(
            batch_name=batch_name,
            batch_file_name=batch_file_name,
            batch_file_contents=batch_file_contents,
            access_roles=access_roles,
        )

        private_doc_batch_post_request.additional_properties = d
        return private_doc_batch_post_request

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
