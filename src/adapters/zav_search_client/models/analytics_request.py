# flake8: noqa
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.analytics_ner_item import AnalyticsNERItem
    from ..models.analytics_request_query import AnalyticsRequestQuery
    from ..models.filters import Filters


T = TypeVar("T", bound="AnalyticsRequest")


@attr.s(auto_attribs=True)
class AnalyticsRequest:
    """Request body for analytics

    Attributes:
        query (AnalyticsRequestQuery):  Example: {'query': 'tensorflow vs pytorch'}.
        ner (List['AnalyticsNERItem']): NER for analytics Example: [{'entity_type': 'CONCEPT', 'entity_class': 'Software
            Framework', 'mention': 'tensorflow', 'start_offset': 0, 'end_offset': 9, 'link': 'EN_1000000', 'node_type':
            'instance'}, {'entity_type': 'CONCEPT', 'entity_class': 'Software Framework', 'mention': 'pytorch',
            'start_offset': 14, 'end_offset': 20, 'link': 'EN_100001', 'node_type': 'instance'}].
        tenant (str):  Example: zetaalpha.
        target (Union[Unset, None, str]):
        filters (Union[Unset, Filters]): Filters grouped by the filter type. Example: {'range': [{'name': 'years',
            'lower_bound': 2001, 'upper_bound': 2020}], 'term': [{'name': 'cited_by', 'value': 'CO_00002'}, {'name':
            'cites', 'value': 'CO_10063396'}, {'name': 'authored_by', 'value': 'PE_001902'}], 'terms': [{'name':
            'document_type', 'values': ['citation']}, {'name': 'source', 'values': ['arXiv', 'ICLR']}, {'name':
            'location_cities', 'values': ['Amsterdam', 'London']}, {'name': 'location_countries', 'values': ['Netherlands',
            'United States']}, {'name': 'organizations', 'values': ['Google', 'Universiteit van Amsterdam']}], 'exists':
            [{'name': 'with_code', 'value': True}]}.
        default_plot (Union[Unset, bool]):
    """

    query: "AnalyticsRequestQuery"
    ner: List["AnalyticsNERItem"]
    tenant: str
    target: Union[Unset, None, str] = UNSET
    filters: Union[Unset, "Filters"] = UNSET
    default_plot: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        query = self.query.to_dict()

        ner = []
        for componentsschemas_analytics_ner_item_data in self.ner:
            componentsschemas_analytics_ner_item = (
                componentsschemas_analytics_ner_item_data.to_dict()
            )

            ner.append(componentsschemas_analytics_ner_item)

        tenant = self.tenant
        target = self.target
        filters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = self.filters.to_dict()

        default_plot = self.default_plot

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
                "ner": ner,
                "tenant": tenant,
            }
        )
        if target is not UNSET:
            field_dict["target"] = target
        if filters is not UNSET:
            field_dict["filters"] = filters
        if default_plot is not UNSET:
            field_dict["default_plot"] = default_plot

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.analytics_ner_item import AnalyticsNERItem
        from ..models.analytics_request_query import AnalyticsRequestQuery
        from ..models.filters import Filters

        d = src_dict.copy()
        query = AnalyticsRequestQuery.from_dict(d.pop("query"))

        ner = []
        _ner = d.pop("ner")
        for componentsschemas_analytics_ner_item_data in _ner:
            componentsschemas_analytics_ner_item = AnalyticsNERItem.from_dict(
                componentsschemas_analytics_ner_item_data
            )

            ner.append(componentsschemas_analytics_ner_item)

        tenant = d.pop("tenant")

        target = d.pop("target", UNSET)

        _filters = d.pop("filters", UNSET)
        filters: Union[Unset, Filters]
        if isinstance(_filters, Unset):
            filters = UNSET
        else:
            filters = Filters.from_dict(_filters)

        default_plot = d.pop("default_plot", UNSET)

        analytics_request = cls(
            query=query,
            ner=ner,
            tenant=tenant,
            target=target,
            filters=filters,
            default_plot=default_plot,
        )

        analytics_request.additional_properties = d
        return analytics_request

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
