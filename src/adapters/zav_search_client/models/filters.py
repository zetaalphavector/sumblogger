# flake8: noqa
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.date_range import DateRange
    from ..models.filter_exists import FilterExists
    from ..models.filter_term_item import FilterTermItem
    from ..models.filter_terms_item import FilterTermsItem
    from ..models.year_range import YearRange


T = TypeVar("T", bound="Filters")


@attr.s(auto_attribs=True)
class Filters:
    """Filters grouped by the filter type.

    Example:
        {'range': [{'name': 'years', 'lower_bound': 2001, 'upper_bound': 2020}], 'term': [{'name': 'cited_by', 'value':
            'CO_00002'}, {'name': 'cites', 'value': 'CO_10063396'}, {'name': 'authored_by', 'value': 'PE_001902'}], 'terms':
            [{'name': 'document_type', 'values': ['citation']}, {'name': 'source', 'values': ['arXiv', 'ICLR']}, {'name':
            'location_cities', 'values': ['Amsterdam', 'London']}, {'name': 'location_countries', 'values': ['Netherlands',
            'United States']}, {'name': 'organizations', 'values': ['Google', 'Universiteit van Amsterdam']}], 'exists':
            [{'name': 'with_code', 'value': True}]}

    Attributes:
        terms (Union[Unset, List['FilterTermsItem']]): Terms filters select results that contain one or more terms
            provided by the values.
        term (Union[Unset, List['FilterTermItem']]): Term filters select results that contain the exact term provided by
            the value.
        range_ (Union[Unset, List[Union['DateRange', 'YearRange']]]): Range filters select results that contain terms
            with the range provided by the lower and upper bound.
        exists (Union[Unset, List['FilterExists']]): Exists filters select results that contain given field in the
            document.
    """

    terms: Union[Unset, List["FilterTermsItem"]] = UNSET
    term: Union[Unset, List["FilterTermItem"]] = UNSET
    range_: Union[Unset, List[Union["DateRange", "YearRange"]]] = UNSET
    exists: Union[Unset, List["FilterExists"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.year_range import YearRange

        terms: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.terms, Unset):
            terms = []
            for componentsschemas_filter_terms_item_data in self.terms:
                componentsschemas_filter_terms_item = (
                    componentsschemas_filter_terms_item_data.to_dict()
                )

                terms.append(componentsschemas_filter_terms_item)

        term: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.term, Unset):
            term = []
            for componentsschemas_filter_term_item_data in self.term:
                componentsschemas_filter_term_item = (
                    componentsschemas_filter_term_item_data.to_dict()
                )

                term.append(componentsschemas_filter_term_item)

        range_: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.range_, Unset):
            range_ = []
            for componentsschemas_filter_range_item_data in self.range_:
                componentsschemas_filter_range_item: Dict[str, Any]

                if isinstance(componentsschemas_filter_range_item_data, YearRange):
                    componentsschemas_filter_range_item = (
                        componentsschemas_filter_range_item_data.to_dict()
                    )

                else:
                    componentsschemas_filter_range_item = (
                        componentsschemas_filter_range_item_data.to_dict()
                    )

                range_.append(componentsschemas_filter_range_item)

        exists: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.exists, Unset):
            exists = []
            for componentsschemas_filters_exists_item_data in self.exists:
                componentsschemas_filters_exists_item = (
                    componentsschemas_filters_exists_item_data.to_dict()
                )

                exists.append(componentsschemas_filters_exists_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if terms is not UNSET:
            field_dict["terms"] = terms
        if term is not UNSET:
            field_dict["term"] = term
        if range_ is not UNSET:
            field_dict["range"] = range_
        if exists is not UNSET:
            field_dict["exists"] = exists

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.date_range import DateRange
        from ..models.filter_exists import FilterExists
        from ..models.filter_term_item import FilterTermItem
        from ..models.filter_terms_item import FilterTermsItem
        from ..models.year_range import YearRange

        d = src_dict.copy()
        terms = []
        _terms = d.pop("terms", UNSET)
        for componentsschemas_filter_terms_item_data in _terms or []:
            componentsschemas_filter_terms_item = FilterTermsItem.from_dict(
                componentsschemas_filter_terms_item_data
            )

            terms.append(componentsschemas_filter_terms_item)

        term = []
        _term = d.pop("term", UNSET)
        for componentsschemas_filter_term_item_data in _term or []:
            componentsschemas_filter_term_item = FilterTermItem.from_dict(
                componentsschemas_filter_term_item_data
            )

            term.append(componentsschemas_filter_term_item)

        range_ = []
        _range_ = d.pop("range", UNSET)
        for componentsschemas_filter_range_item_data in _range_ or []:

            def _parse_componentsschemas_filter_range_item(
                data: object,
            ) -> Union["DateRange", "YearRange"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_filter_range_item_type_0 = YearRange.from_dict(
                        data
                    )

                    return componentsschemas_filter_range_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_filter_range_item_type_1 = DateRange.from_dict(data)

                return componentsschemas_filter_range_item_type_1

            componentsschemas_filter_range_item = (
                _parse_componentsschemas_filter_range_item(
                    componentsschemas_filter_range_item_data
                )
            )

            range_.append(componentsschemas_filter_range_item)

        exists = []
        _exists = d.pop("exists", UNSET)
        for componentsschemas_filters_exists_item_data in _exists or []:
            componentsschemas_filters_exists_item = FilterExists.from_dict(
                componentsschemas_filters_exists_item_data
            )

            exists.append(componentsschemas_filters_exists_item)

        filters = cls(
            terms=terms,
            term=term,
            range_=range_,
            exists=exists,
        )

        filters.additional_properties = d
        return filters

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
