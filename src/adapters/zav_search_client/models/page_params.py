from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="PageParams")


@attr.s(auto_attribs=True)
class PageParams:
    """
    Attributes:
        page (float):
        page_size (float):
    """

    page: float
    page_size: float
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        page = self.page
        page_size = self.page_size

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "page": page,
                "page_size": page_size,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        page = d.pop("page")

        page_size = d.pop("page_size")

        page_params = cls(
            page=page,
            page_size=page_size,
        )

        page_params.additional_properties = d
        return page_params

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
