# flake8: noqa
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.analytics_response_data_item_data_item import (
        AnalyticsResponseDataItemDataItem,
    )


T = TypeVar("T", bound="AnalyticsResponseDataItem")


@attr.s(auto_attribs=True)
class AnalyticsResponseDataItem:
    """
    Attributes:
        label (str):
        id (str):
        data (List['AnalyticsResponseDataItemDataItem']):
    """

    label: str
    id: str
    data: List["AnalyticsResponseDataItemDataItem"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        id = self.id
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()

            data.append(data_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "label": label,
                "ID": id,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.analytics_response_data_item_data_item import (
            AnalyticsResponseDataItemDataItem,
        )

        d = src_dict.copy()
        label = d.pop("label")

        id = d.pop("ID")

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = AnalyticsResponseDataItemDataItem.from_dict(data_item_data)

            data.append(data_item)

        analytics_response_data_item = cls(
            label=label,
            id=id,
            data=data,
        )

        analytics_response_data_item.additional_properties = d
        return analytics_response_data_item

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
