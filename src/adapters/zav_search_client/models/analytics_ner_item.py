from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="AnalyticsNERItem")


@attr.s(auto_attribs=True)
class AnalyticsNERItem:
    """
    Attributes:
        entity_type (str):
        entity_class (str):
        end_offset (int):
        mention (str):
        start_offset (int):
        link (str):
        node_type (str):
    """

    entity_type: str
    entity_class: str
    end_offset: int
    mention: str
    start_offset: int
    link: str
    node_type: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        entity_type = self.entity_type
        entity_class = self.entity_class
        end_offset = self.end_offset
        mention = self.mention
        start_offset = self.start_offset
        link = self.link
        node_type = self.node_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entity_type": entity_type,
                "entity_class": entity_class,
                "end_offset": end_offset,
                "mention": mention,
                "start_offset": start_offset,
                "link": link,
                "node_type": node_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity_type = d.pop("entity_type")

        entity_class = d.pop("entity_class")

        end_offset = d.pop("end_offset")

        mention = d.pop("mention")

        start_offset = d.pop("start_offset")

        link = d.pop("link")

        node_type = d.pop("node_type")

        analytics_ner_item = cls(
            entity_type=entity_type,
            entity_class=entity_class,
            end_offset=end_offset,
            mention=mention,
            start_offset=start_offset,
            link=link,
            node_type=node_type,
        )

        analytics_ner_item.additional_properties = d
        return analytics_ner_item

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
