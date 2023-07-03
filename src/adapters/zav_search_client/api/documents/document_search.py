# flake8: noqa
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.document_search_collapse import DocumentSearchCollapse
from ...models.document_search_date import DocumentSearchDate
from ...models.document_search_document_types_item import (
    DocumentSearchDocumentTypesItem,
)
from ...models.document_search_retrieval_method import DocumentSearchRetrievalMethod
from ...models.document_search_retrieval_unit import DocumentSearchRetrievalUnit
from ...models.document_search_sort import DocumentSearchSort
from ...models.document_search_sort_order_item import DocumentSearchSortOrderItem
from ...models.document_search_year import DocumentSearchYear
from ...models.search_engine_string import SearchEngineString
from ...models.search_response import SearchResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    retrieval_unit: DocumentSearchRetrievalUnit,
    *,
    client: Client,
    tenant: str = "zetaalpha",
    query_string: str = "",
    retrieval_method: DocumentSearchRetrievalMethod = DocumentSearchRetrievalMethod.KEYWORD,
    sources: List[str],
    doc_ids: List[str],
    search_engine: SearchEngineString,
    year: Optional["DocumentSearchYear"],
    cited_by: Optional[str],
    cites: Optional[str],
    authored_by: Optional[str],
    date: Optional["DocumentSearchDate"],
    has_concept: Optional[str],
    with_content: Optional[bool] = True,
    document_types: List[DocumentSearchDocumentTypesItem],
    page: Optional[int] = 1,
    page_size: Optional[int] = 10,
    sort: "DocumentSearchSort",
    sort_order: List[DocumentSearchSortOrderItem],
    similar_to: Optional[List[str]],
    collapse: Optional[
        Union[Unset, None, DocumentSearchCollapse]
    ] = DocumentSearchCollapse.UID,
    rerank: Optional[bool] = False,
    reranker: Optional[Union[Unset, None, str]] = UNSET,
    rerank_top_n: Optional[int] = 30,
    aggregate_reranked_results: Optional[bool] = False,
    simplified_query: Optional[bool] = False,
    with_code: Optional[bool] = False,
    index_cluster: Optional[str],
    query_encoder_service: Optional[str],
    reranker_service: Optional[str],
    visibility: Optional[List[str]],
    location_cities: Optional[List[str]],
    location_countries: Optional[List[str]],
    organizations: Optional[List[str]],
    requester_uuid: Optional[str],
    user_roles: Optional[str],
) -> Dict[str, Any]:
    url = "{}/documents/{retrieval_unit}/search".format(
        client.base_url, retrieval_unit=retrieval_unit
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    headers["requester-uuid"] = requester_uuid if requester_uuid else ""

    headers["user-roles"] = user_roles if user_roles else ""

    params: Dict[str, Any] = {}
    params["tenant"] = tenant

    json_search_engine = search_engine.value

    params["search_engine"] = json_search_engine

    params["query_string"] = query_string

    json_retrieval_method = retrieval_method.value

    params["retrieval_method"] = json_retrieval_method

    if year:
        json_year = year.to_dict()
        params.update(json_year)

    json_sources = sources

    params["sources"] = json_sources

    params["cited_by"] = cited_by

    params["cites"] = cites

    params["authored_by"] = authored_by

    if date:
        json_date = date.to_dict()
        params.update(json_date)

    json_doc_ids = doc_ids

    params["doc_ids"] = ",".join(json_doc_ids)

    params["has_concept"] = has_concept

    params["with_content"] = with_content

    json_document_types = []
    for document_types_item_data in document_types:
        document_types_item = document_types_item_data.value

        json_document_types.append(document_types_item)

    params["document_types"] = json_document_types

    params["page"] = page

    params["page_size"] = page_size

    json_sort = sort.to_dict()

    params.update(json_sort)

    json_sort_order = []
    for sort_order_item_data in sort_order:
        sort_order_item = sort_order_item_data.value

        json_sort_order.append(sort_order_item)

    params["sort_order"] = json_sort_order

    json_similar_to = similar_to

    params["similar_to"] = json_similar_to

    json_collapse: Union[Unset, None, str] = UNSET
    if not isinstance(collapse, Unset):
        json_collapse = collapse.value if collapse else None

    params["collapse"] = json_collapse

    params["rerank"] = rerank

    params["reranker"] = reranker

    params["rerank_top_n"] = rerank_top_n

    params["aggregate_reranked_results"] = aggregate_reranked_results

    params["simplified_query"] = simplified_query

    params["with_code"] = with_code

    params["index_cluster"] = index_cluster

    params["query_encoder_service"] = query_encoder_service

    params["reranker_service"] = reranker_service

    json_visibility = visibility

    params["visibility"] = json_visibility

    json_location_cities = location_cities

    params["location_cities"] = json_location_cities

    json_location_countries = location_countries

    params["location_countries"] = json_location_countries

    json_organizations = organizations

    params["organizations"] = json_organizations

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[Any, SearchResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SearchResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.REQUEST_TIMEOUT:
        response_408 = cast(Any, None)
        return response_408
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, SearchResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    retrieval_unit: DocumentSearchRetrievalUnit,
    *,
    client: Client,
    tenant: str = "zetaalpha",
    query_string: str = "",
    retrieval_method: DocumentSearchRetrievalMethod = DocumentSearchRetrievalMethod.KEYWORD,
    sources: List[str],
    doc_ids: List[str],
    search_engine: SearchEngineString,
    year: Optional["DocumentSearchYear"],
    cited_by: Optional[str],
    cites: Optional[str],
    authored_by: Optional[str],
    date: Optional["DocumentSearchDate"],
    has_concept: Optional[str],
    with_content: Optional[bool] = True,
    document_types: List[DocumentSearchDocumentTypesItem],
    page: Optional[int] = 1,
    page_size: Optional[int] = 10,
    sort: "DocumentSearchSort",
    sort_order: List[DocumentSearchSortOrderItem],
    similar_to: Optional[List[str]],
    collapse: Optional[
        Union[Unset, None, DocumentSearchCollapse]
    ] = DocumentSearchCollapse.UID,
    rerank: Optional[bool] = False,
    reranker: Optional[Union[Unset, None, str]] = UNSET,
    rerank_top_n: Optional[int] = 30,
    aggregate_reranked_results: Optional[bool] = False,
    simplified_query: Optional[bool] = False,
    with_code: Optional[bool] = False,
    index_cluster: Optional[str],
    query_encoder_service: Optional[str],
    reranker_service: Optional[str],
    visibility: Optional[List[str]],
    location_cities: Optional[List[str]],
    location_countries: Optional[List[str]],
    organizations: Optional[List[str]],
    requester_uuid: Optional[str],
    user_roles: Optional[str],
) -> Response[Union[Any, SearchResponse]]:
    """Search documents based on query and parameters

    Args:
        retrieval_unit (DocumentSearchRetrievalUnit):
        tenant (str):  Default: 'zetaalpha'.
        search_engine (SearchEngineString):
        query_string (str): Query string Default: ''. Example: What is a CNN?.
        retrieval_method (DocumentSearchRetrievalMethod):  Default:
            DocumentSearchRetrievalMethod.KEYWORD.
        year (DocumentSearchYear):
        sources (List[str]):
        cited_by (str):
        cites (str):
        authored_by (str):
        date (DocumentSearchDate):
        doc_ids (List[str]):
        has_concept (str):
        with_content (bool):  Default: True.
        document_types (List[DocumentSearchDocumentTypesItem]):
        page (int):  Default: 1.
        page_size (int):  Default: 10.
        sort (DocumentSearchSort):
        sort_order (List[DocumentSearchSortOrderItem]):
        similar_to (List[str]):
        collapse (Union[Unset, None, DocumentSearchCollapse]):  Default:
            DocumentSearchCollapse.UID.
        rerank (bool):
        reranker (Union[Unset, None, str]):
        rerank_top_n (int):  Default: 30.
        aggregate_reranked_results (bool):
        simplified_query (bool):
        with_code (bool):
        index_cluster (str):
        query_encoder_service (str):
        reranker_service (str):
        visibility (List[str]):
        location_cities (List[str]):
        location_countries (List[str]):
        organizations (List[str]):
        requester_uuid (str):
        user_roles (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SearchResponse]]
    """

    kwargs = _get_kwargs(
        retrieval_unit=retrieval_unit,
        client=client,
        tenant=tenant,
        search_engine=search_engine,
        query_string=query_string,
        retrieval_method=retrieval_method,
        year=year,
        sources=sources,
        cited_by=cited_by,
        cites=cites,
        authored_by=authored_by,
        date=date,
        doc_ids=doc_ids,
        has_concept=has_concept,
        with_content=with_content,
        document_types=document_types,
        page=page,
        page_size=page_size,
        sort=sort,
        sort_order=sort_order,
        similar_to=similar_to,
        collapse=collapse,
        rerank=rerank,
        reranker=reranker,
        rerank_top_n=rerank_top_n,
        aggregate_reranked_results=aggregate_reranked_results,
        simplified_query=simplified_query,
        with_code=with_code,
        index_cluster=index_cluster,
        query_encoder_service=query_encoder_service,
        reranker_service=reranker_service,
        visibility=visibility,
        location_cities=location_cities,
        location_countries=location_countries,
        organizations=organizations,
        requester_uuid=requester_uuid,
        user_roles=user_roles,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    retrieval_unit: DocumentSearchRetrievalUnit,
    *,
    client: Client,
    tenant: str = "zetaalpha",
    query_string: str = "",
    retrieval_method: DocumentSearchRetrievalMethod = DocumentSearchRetrievalMethod.KEYWORD,
    sources: List[str],
    doc_ids: List[str],
    search_engine: SearchEngineString,
    year: Optional["DocumentSearchYear"],
    cited_by: Optional[str],
    cites: Optional[str],
    authored_by: Optional[str],
    date: Optional["DocumentSearchDate"],
    has_concept: Optional[str],
    with_content: Optional[bool] = True,
    document_types: List[DocumentSearchDocumentTypesItem],
    page: Optional[int] = 1,
    page_size: Optional[int] = 10,
    sort: "DocumentSearchSort",
    sort_order: List[DocumentSearchSortOrderItem],
    similar_to: Optional[List[str]],
    collapse: Optional[
        Union[Unset, None, DocumentSearchCollapse]
    ] = DocumentSearchCollapse.UID,
    rerank: Optional[bool] = False,
    reranker: Optional[Union[Unset, None, str]] = UNSET,
    rerank_top_n: Optional[int] = 30,
    aggregate_reranked_results: Optional[bool] = False,
    simplified_query: Optional[bool] = False,
    with_code: Optional[bool] = False,
    index_cluster: Optional[str],
    query_encoder_service: Optional[str],
    reranker_service: Optional[str],
    visibility: Optional[List[str]],
    location_cities: Optional[List[str]],
    location_countries: Optional[List[str]],
    organizations: Optional[List[str]],
    requester_uuid: Optional[str],
    user_roles: Optional[str],
) -> Optional[Union[Any, SearchResponse]]:
    """Search documents based on query and parameters

    Args:
        retrieval_unit (DocumentSearchRetrievalUnit):
        tenant (str):  Default: 'zetaalpha'.
        search_engine (SearchEngineString):
        query_string (str): Query string Default: ''. Example: What is a CNN?.
        retrieval_method (DocumentSearchRetrievalMethod):  Default:
            DocumentSearchRetrievalMethod.KEYWORD.
        year (DocumentSearchYear):
        sources (List[str]):
        cited_by (str):
        cites (str):
        authored_by (str):
        date (DocumentSearchDate):
        doc_ids (List[str]):
        has_concept (str):
        with_content (bool):  Default: True.
        document_types (List[DocumentSearchDocumentTypesItem]):
        page (int):  Default: 1.
        page_size (int):  Default: 10.
        sort (DocumentSearchSort):
        sort_order (List[DocumentSearchSortOrderItem]):
        similar_to (List[str]):
        collapse (Union[Unset, None, DocumentSearchCollapse]):  Default:
            DocumentSearchCollapse.UID.
        rerank (bool):
        reranker (Union[Unset, None, str]):
        rerank_top_n (int):  Default: 30.
        aggregate_reranked_results (bool):
        simplified_query (bool):
        with_code (bool):
        index_cluster (str):
        query_encoder_service (str):
        reranker_service (str):
        visibility (List[str]):
        location_cities (List[str]):
        location_countries (List[str]):
        organizations (List[str]):
        requester_uuid (str):
        user_roles (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SearchResponse]]
    """

    return sync_detailed(
        retrieval_unit=retrieval_unit,
        client=client,
        tenant=tenant,
        search_engine=search_engine,
        query_string=query_string,
        retrieval_method=retrieval_method,
        year=year,
        sources=sources,
        cited_by=cited_by,
        cites=cites,
        authored_by=authored_by,
        date=date,
        doc_ids=doc_ids,
        has_concept=has_concept,
        with_content=with_content,
        document_types=document_types,
        page=page,
        page_size=page_size,
        sort=sort,
        sort_order=sort_order,
        similar_to=similar_to,
        collapse=collapse,
        rerank=rerank,
        reranker=reranker,
        rerank_top_n=rerank_top_n,
        aggregate_reranked_results=aggregate_reranked_results,
        simplified_query=simplified_query,
        with_code=with_code,
        index_cluster=index_cluster,
        query_encoder_service=query_encoder_service,
        reranker_service=reranker_service,
        visibility=visibility,
        location_cities=location_cities,
        location_countries=location_countries,
        organizations=organizations,
        requester_uuid=requester_uuid,
        user_roles=user_roles,
    ).parsed


async def asyncio_detailed(
    retrieval_unit: DocumentSearchRetrievalUnit,
    *,
    client: Client,
    tenant: str = "zetaalpha",
    query_string: str = "",
    retrieval_method: DocumentSearchRetrievalMethod = DocumentSearchRetrievalMethod.KEYWORD,
    sources: List[str],
    doc_ids: List[str],
    search_engine: SearchEngineString,
    year: Optional["DocumentSearchYear"],
    cited_by: Optional[str],
    cites: Optional[str],
    authored_by: Optional[str],
    date: Optional["DocumentSearchDate"],
    has_concept: Optional[str],
    with_content: Optional[bool] = True,
    document_types: List[DocumentSearchDocumentTypesItem],
    page: Optional[int] = 1,
    page_size: Optional[int] = 10,
    sort: "DocumentSearchSort",
    sort_order: List[DocumentSearchSortOrderItem],
    similar_to: Optional[List[str]],
    collapse: Optional[
        Union[Unset, None, DocumentSearchCollapse]
    ] = DocumentSearchCollapse.UID,
    rerank: Optional[bool] = False,
    reranker: Optional[Union[Unset, None, str]] = UNSET,
    rerank_top_n: Optional[int] = 30,
    aggregate_reranked_results: Optional[bool] = False,
    simplified_query: Optional[bool] = False,
    with_code: Optional[bool] = False,
    index_cluster: Optional[str],
    query_encoder_service: Optional[str],
    reranker_service: Optional[str],
    visibility: Optional[List[str]],
    location_cities: Optional[List[str]],
    location_countries: Optional[List[str]],
    organizations: Optional[List[str]],
    requester_uuid: Optional[str],
    user_roles: Optional[str],
) -> Response[Union[Any, SearchResponse]]:
    """Search documents based on query and parameters

    Args:
        retrieval_unit (DocumentSearchRetrievalUnit):
        tenant (str):  Default: 'zetaalpha'.
        search_engine (SearchEngineString):
        query_string (str): Query string Default: ''. Example: What is a CNN?.
        retrieval_method (DocumentSearchRetrievalMethod):  Default:
            DocumentSearchRetrievalMethod.KEYWORD.
        year (DocumentSearchYear):
        sources (List[str]):
        cited_by (str):
        cites (str):
        authored_by (str):
        date (DocumentSearchDate):
        doc_ids (List[str]):
        has_concept (str):
        with_content (bool):  Default: True.
        document_types (List[DocumentSearchDocumentTypesItem]):
        page (int):  Default: 1.
        page_size (int):  Default: 10.
        sort (DocumentSearchSort):
        sort_order (List[DocumentSearchSortOrderItem]):
        similar_to (List[str]):
        collapse (Union[Unset, None, DocumentSearchCollapse]):  Default:
            DocumentSearchCollapse.UID.
        rerank (bool):
        reranker (Union[Unset, None, str]):
        rerank_top_n (int):  Default: 30.
        aggregate_reranked_results (bool):
        simplified_query (bool):
        with_code (bool):
        index_cluster (str):
        query_encoder_service (str):
        reranker_service (str):
        visibility (List[str]):
        location_cities (List[str]):
        location_countries (List[str]):
        organizations (List[str]):
        requester_uuid (str):
        user_roles (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SearchResponse]]
    """

    kwargs = _get_kwargs(
        retrieval_unit=retrieval_unit,
        client=client,
        tenant=tenant,
        search_engine=search_engine,
        query_string=query_string,
        retrieval_method=retrieval_method,
        year=year,
        sources=sources,
        cited_by=cited_by,
        cites=cites,
        authored_by=authored_by,
        date=date,
        doc_ids=doc_ids,
        has_concept=has_concept,
        with_content=with_content,
        document_types=document_types,
        page=page,
        page_size=page_size,
        sort=sort,
        sort_order=sort_order,
        similar_to=similar_to,
        collapse=collapse,
        rerank=rerank,
        reranker=reranker,
        rerank_top_n=rerank_top_n,
        aggregate_reranked_results=aggregate_reranked_results,
        simplified_query=simplified_query,
        with_code=with_code,
        index_cluster=index_cluster,
        query_encoder_service=query_encoder_service,
        reranker_service=reranker_service,
        visibility=visibility,
        location_cities=location_cities,
        location_countries=location_countries,
        organizations=organizations,
        requester_uuid=requester_uuid,
        user_roles=user_roles,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    retrieval_unit: DocumentSearchRetrievalUnit,
    *,
    client: Client,
    tenant: str = "zetaalpha",
    query_string: str = "",
    retrieval_method: DocumentSearchRetrievalMethod = DocumentSearchRetrievalMethod.KEYWORD,
    sources: List[str],
    doc_ids: List[str],
    search_engine: SearchEngineString,
    year: Optional["DocumentSearchYear"] = None,
    cited_by: Optional[str] = None,
    cites: Optional[str] = None,
    authored_by: Optional[str] = None,
    date: Optional["DocumentSearchDate"] = None,
    has_concept: Optional[str] = None,
    with_content: Optional[bool] = True,
    document_types: List[DocumentSearchDocumentTypesItem],
    page: Optional[int] = 1,
    page_size: Optional[int] = 10,
    sort: "DocumentSearchSort",
    sort_order: List[DocumentSearchSortOrderItem],
    similar_to: Optional[List[str]] = None,
    collapse: Optional[
        Union[Unset, None, DocumentSearchCollapse]
    ] = DocumentSearchCollapse.UID,
    rerank: Optional[bool] = None,
    reranker: Optional[Union[Unset, None, str]] = UNSET,
    rerank_top_n: Optional[int] = None,
    aggregate_reranked_results: Optional[bool] = False,
    simplified_query: Optional[bool] = False,
    with_code: Optional[bool] = False,
    index_cluster: Optional[str] = None,
    query_encoder_service: Optional[str] = None,
    reranker_service: Optional[str] = None,
    visibility: Optional[List[str]] = None,
    location_cities: Optional[List[str]] = None,
    location_countries: Optional[List[str]] = None,
    organizations: Optional[List[str]] = None,
    requester_uuid: Optional[str] = None,
    user_roles: Optional[str] = None,
) -> Optional[Union[Any, SearchResponse]]:
    """Search documents based on query and parameters

    Args:
        retrieval_unit (DocumentSearchRetrievalUnit):
        tenant (str):  Default: 'zetaalpha'.
        search_engine (SearchEngineString):
        query_string (str): Query string Default: ''. Example: What is a CNN?.
        retrieval_method (DocumentSearchRetrievalMethod):  Default:
            DocumentSearchRetrievalMethod.KEYWORD.
        year (DocumentSearchYear):
        sources (List[str]):
        cited_by (str):
        cites (str):
        authored_by (str):
        date (DocumentSearchDate):
        doc_ids (List[str]):
        has_concept (str):
        with_content (bool):  Default: True.
        document_types (List[DocumentSearchDocumentTypesItem]):
        page (int):  Default: 1.
        page_size (int):  Default: 10.
        sort (DocumentSearchSort):
        sort_order (List[DocumentSearchSortOrderItem]):
        similar_to (List[str]):
        collapse (Union[Unset, None, DocumentSearchCollapse]):  Default:
            DocumentSearchCollapse.UID.
        rerank (bool):
        reranker (Union[Unset, None, str]):
        rerank_top_n (int):  Default: 30.
        aggregate_reranked_results (bool):
        simplified_query (bool):
        with_code (bool):
        index_cluster (str):
        query_encoder_service (str):
        reranker_service (str):
        visibility (List[str]):
        location_cities (List[str]):
        location_countries (List[str]):
        organizations (List[str]):
        requester_uuid (str):
        user_roles (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SearchResponse]]
    """

    return (
        await asyncio_detailed(
            retrieval_unit=retrieval_unit,
            client=client,
            tenant=tenant,
            search_engine=search_engine,
            query_string=query_string,
            retrieval_method=retrieval_method,
            year=year,
            sources=sources,
            cited_by=cited_by,
            cites=cites,
            authored_by=authored_by,
            date=date,
            doc_ids=doc_ids,
            has_concept=has_concept,
            with_content=with_content,
            document_types=document_types,
            page=page,
            page_size=page_size,
            sort=sort,
            sort_order=sort_order,
            similar_to=similar_to,
            collapse=collapse,
            rerank=rerank,
            reranker=reranker,
            rerank_top_n=rerank_top_n,
            aggregate_reranked_results=aggregate_reranked_results,
            simplified_query=simplified_query,
            with_code=with_code,
            index_cluster=index_cluster,
            query_encoder_service=query_encoder_service,
            reranker_service=reranker_service,
            visibility=visibility,
            location_cities=location_cities,
            location_countries=location_countries,
            organizations=organizations,
            requester_uuid=requester_uuid,
            user_roles=user_roles,
        )
    ).parsed
