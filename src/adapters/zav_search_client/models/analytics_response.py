# flake8: noqa
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.analytics_response_data_item import AnalyticsResponseDataItem


T = TypeVar("T", bound="AnalyticsResponse")


@attr.s(auto_attribs=True)
class AnalyticsResponse:
    """Response of the /analytics

    Example:
        {'name': 'Interest over time', 'x_axis': 'Time', 'y_axis': 'Number of publications', 'data': [{'label':
            'tensorflow', 'ID': 'EN_1000084', 'data': [{'x': '2019-03-01T00:00:00.000Z', 'y': 1}, {'x':
            '2019-04-01T00:00:00.000Z', 'y': 0}, {'x': '2019-05-01T00:00:00.000Z', 'y': 0}, {'x':
            '2019-06-01T00:00:00.000Z', 'y': 0}, {'x': '2019-07-01T00:00:00.000Z', 'y': 0}, {'x':
            '2019-08-01T00:00:00.000Z', 'y': 0}, {'x': '2019-09-01T00:00:00.000Z', 'y': 0}, {'x':
            '2019-10-01T00:00:00.000Z', 'y': 0}, {'x': '2019-11-01T00:00:00.000Z', 'y': 0}, {'x':
            '2019-12-01T00:00:00.000Z', 'y': 1}, {'x': '2020-01-01T00:00:00.000Z', 'y': 0}, {'x':
            '2020-02-01T00:00:00.000Z', 'y': 0}, {'x': '2020-03-01T00:00:00.000Z', 'y': 1}]}, {'label': 'pytorch', 'ID':
            'EN_1000085', 'data': [{'x': '2019-05-01T00:00:00.000Z', 'y': 1}, {'x': '2019-06-01T00:00:00.000Z', 'y': 3},
            {'x': '2019-07-01T00:00:00.000Z', 'y': 0}, {'x': '2019-08-01T00:00:00.000Z', 'y': 1}, {'x':
            '2019-09-01T00:00:00.000Z', 'y': 1}, {'x': '2019-10-01T00:00:00.000Z', 'y': 1}, {'x':
            '2019-11-01T00:00:00.000Z', 'y': 1}, {'x': '2019-12-01T00:00:00.000Z', 'y': 0}, {'x':
            '2020-01-01T00:00:00.000Z', 'y': 1}, {'x': '2020-02-01T00:00:00.000Z', 'y': 3}, {'x':
            '2020-03-01T00:00:00.000Z', 'y': 1}, {'x': '2020-04-01T00:00:00.000Z', 'y': 3}, {'x':
            '2020-05-01T00:00:00.000Z', 'y': 0}, {'x': '2020-06-01T00:00:00.000Z', 'y': 3}, {'x':
            '2020-07-01T00:00:00.000Z', 'y': 1}]}]}

    Attributes:
        name (str):
        x_axis (str):
        y_axis (str):
        query (str):
        data (List['AnalyticsResponseDataItem']):
    """

    name: str
    x_axis: str
    y_axis: str
    query: str
    data: List["AnalyticsResponseDataItem"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        x_axis = self.x_axis
        y_axis = self.y_axis
        query = self.query
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()

            data.append(data_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "x_axis": x_axis,
                "y_axis": y_axis,
                "query": query,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.analytics_response_data_item import AnalyticsResponseDataItem

        d = src_dict.copy()
        name = d.pop("name")

        x_axis = d.pop("x_axis")

        y_axis = d.pop("y_axis")

        query = d.pop("query")

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = AnalyticsResponseDataItem.from_dict(data_item_data)

            data.append(data_item)

        analytics_response = cls(
            name=name,
            x_axis=x_axis,
            y_axis=y_axis,
            query=query,
            data=data,
        )

        analytics_response.additional_properties = d
        return analytics_response

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
