# flake8: noqa
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, Union, cast

import attr

from ..models.document_type_string import DocumentTypeString
from ..models.private_doc_status import PrivateDocStatus
from ..models.private_doc_status_code import PrivateDocStatusCode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.git_hub_repo import GitHubRepo
    from ..models.hit_metadata import HitMetadata
    from ..models.representations import Representations
    from ..models.resources_item import ResourcesItem
    from ..models.tweet import Tweet


T = TypeVar("T", bound="Hit")


@attr.s(auto_attribs=True)
class Hit:
    """
    Attributes:
        field_id (str):  Example: 2cd44b68b00e0355684f7c940b2c7bd9329050f5_0.
        highlight (str):  Example: We present quasi-<strong>recurrent</strong> <strong>neural</strong>
            <strong>networks</strong> for <strong>neural</strong> sequence modeling.<br />Quasi-<strong>recurrent</strong>
            <strong>neural</strong> <strong>networks</strong> are related to several such recently described models,
            especially the strongly-typed <strong>recurrent</strong> <strong>neural</strong> <strong>networks</strong>
            (T-RNN)<br /><strong>Recurrent</strong> <strong>neural</strong> <strong>network</strong> based language model..
        document_type (DocumentTypeString):
        score (float):  Example: 130.56.
        uid (str):  Example: CO_100456.
        metadata (HitMetadata):
        organize_doc_id (str):  Example: 2cd44b68b00e0355684f7c940b2c7bd9329050f5_0.
        highlight_tokens (Union[Unset, List[str]]):
        guid (Optional[str]):  Example: 2cd44b68b00e0355684f7c940b2c7bd9329050f5.
        uri (Optional[str]):  Example: https://arxiv.org/abs/1611.01576.
        representations (Union[Unset, Representations]):
        no_references (Union[Unset, int]):  Example: 15.
        no_citations (Union[Unset, int]):  Example: 101.
        h_index_sum (Union[Unset, int]):  Example: 5.
        h_index_avg (Union[Unset, float]):  Example: 5.0.
        twitter_popularity_score (Union[Unset, int]):  Example: 5.
        github_score (Union[Unset, int]):  Example: 500.
        duplicates (Union[Unset, List['Hit']]):
        tweets (Union[Unset, List['Tweet']]):
        github_repos (Union[Unset, List['GitHubRepo']]):
        resources (Union[Unset, List['ResourcesItem']]):
        status (Union[Unset, PrivateDocStatus]):
        status_codes (Union[Unset, List[PrivateDocStatusCode]]):
        status_message (Union[Unset, None, str]):  Example: Something went wrong!.
        get_bibtex_id (Union[Unset, str]):  Example: CO_00002.
        get_similar_docs_id (Union[Unset, str]):  Example: CO_00002.
        get_cites_id (Union[Unset, str]):  Example: CO_00002.
        get_refs_id (Union[Unset, str]):  Example: CO_00002.
        share_uri (Union[Unset, str]):  Example: https://search.zeta-
            alpha.com?doc_ids=0303662dc5bd3fed964fb9ef04bf22c88b0bc9ca.
    """

    field_id: str
    highlight: str
    document_type: DocumentTypeString
    score: float
    uid: str
    metadata: "HitMetadata"
    organize_doc_id: str
    guid: Optional[str]
    uri: Optional[str]
    highlight_tokens: Union[Unset, List[str]] = UNSET
    representations: Union[Unset, "Representations"] = UNSET
    no_references: Union[Unset, int] = UNSET
    no_citations: Union[Unset, int] = UNSET
    h_index_sum: Union[Unset, int] = UNSET
    h_index_avg: Union[Unset, float] = UNSET
    twitter_popularity_score: Union[Unset, int] = UNSET
    github_score: Union[Unset, int] = UNSET
    duplicates: Union[Unset, List["Hit"]] = UNSET
    tweets: Union[Unset, List["Tweet"]] = UNSET
    github_repos: Union[Unset, List["GitHubRepo"]] = UNSET
    resources: Union[Unset, List["ResourcesItem"]] = UNSET
    status: Union[Unset, PrivateDocStatus] = UNSET
    status_codes: Union[Unset, List[PrivateDocStatusCode]] = UNSET
    status_message: Union[Unset, None, str] = UNSET
    get_bibtex_id: Union[Unset, str] = UNSET
    get_similar_docs_id: Union[Unset, str] = UNSET
    get_cites_id: Union[Unset, str] = UNSET
    get_refs_id: Union[Unset, str] = UNSET
    share_uri: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_id = self.field_id
        highlight = self.highlight
        document_type = self.document_type.value

        score = self.score
        uid = self.uid
        metadata = self.metadata.to_dict()

        organize_doc_id = self.organize_doc_id
        highlight_tokens: Union[Unset, List[str]] = UNSET
        if not isinstance(self.highlight_tokens, Unset):
            highlight_tokens = self.highlight_tokens

        guid = self.guid
        uri = self.uri
        representations: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.representations, Unset):
            representations = self.representations.to_dict()

        no_references = self.no_references
        no_citations = self.no_citations
        h_index_sum = self.h_index_sum
        h_index_avg = self.h_index_avg
        twitter_popularity_score = self.twitter_popularity_score
        github_score = self.github_score
        duplicates: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.duplicates, Unset):
            duplicates = []
            for duplicates_item_data in self.duplicates:
                duplicates_item = duplicates_item_data.to_dict()

                duplicates.append(duplicates_item)

        tweets: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.tweets, Unset):
            tweets = []
            for tweets_item_data in self.tweets:
                tweets_item = tweets_item_data.to_dict()

                tweets.append(tweets_item)

        github_repos: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.github_repos, Unset):
            github_repos = []
            for github_repos_item_data in self.github_repos:
                github_repos_item = github_repos_item_data.to_dict()

                github_repos.append(github_repos_item)

        resources: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.resources, Unset):
            resources = []
            for componentsschemas_resources_item_data in self.resources:
                componentsschemas_resources_item = (
                    componentsschemas_resources_item_data.to_dict()
                )

                resources.append(componentsschemas_resources_item)

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        status_codes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.status_codes, Unset):
            status_codes = []
            for status_codes_item_data in self.status_codes:
                status_codes_item = status_codes_item_data.value

                status_codes.append(status_codes_item)

        status_message = self.status_message
        get_bibtex_id = self.get_bibtex_id
        get_similar_docs_id = self.get_similar_docs_id
        get_cites_id = self.get_cites_id
        get_refs_id = self.get_refs_id
        share_uri = self.share_uri

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "_id": field_id,
                "highlight": highlight,
                "document_type": document_type,
                "score": score,
                "uid": uid,
                "metadata": metadata,
                "organize_doc_id": organize_doc_id,
                "guid": guid,
                "uri": uri,
            }
        )
        if highlight_tokens is not UNSET:
            field_dict["highlight_tokens"] = highlight_tokens
        if representations is not UNSET:
            field_dict["representations"] = representations
        if no_references is not UNSET:
            field_dict["no_references"] = no_references
        if no_citations is not UNSET:
            field_dict["no_citations"] = no_citations
        if h_index_sum is not UNSET:
            field_dict["h_index_sum"] = h_index_sum
        if h_index_avg is not UNSET:
            field_dict["h_index_avg"] = h_index_avg
        if twitter_popularity_score is not UNSET:
            field_dict["twitter_popularity_score"] = twitter_popularity_score
        if github_score is not UNSET:
            field_dict["github_score"] = github_score
        if duplicates is not UNSET:
            field_dict["duplicates"] = duplicates
        if tweets is not UNSET:
            field_dict["tweets"] = tweets
        if github_repos is not UNSET:
            field_dict["github_repos"] = github_repos
        if resources is not UNSET:
            field_dict["resources"] = resources
        if status is not UNSET:
            field_dict["status"] = status
        if status_codes is not UNSET:
            field_dict["status_codes"] = status_codes
        if status_message is not UNSET:
            field_dict["status_message"] = status_message
        if get_bibtex_id is not UNSET:
            field_dict["get_bibtex_id"] = get_bibtex_id
        if get_similar_docs_id is not UNSET:
            field_dict["get_similar_docs_id"] = get_similar_docs_id
        if get_cites_id is not UNSET:
            field_dict["get_cites_id"] = get_cites_id
        if get_refs_id is not UNSET:
            field_dict["get_refs_id"] = get_refs_id
        if share_uri is not UNSET:
            field_dict["share_uri"] = share_uri

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.git_hub_repo import GitHubRepo
        from ..models.hit_metadata import HitMetadata
        from ..models.representations import Representations
        from ..models.resources_item import ResourcesItem
        from ..models.tweet import Tweet

        d = src_dict.copy()
        field_id = d.pop("_id")

        highlight = d.pop("highlight")

        document_type = DocumentTypeString(d.pop("document_type"))

        score = d.pop("score")

        uid = d.pop("uid")

        metadata = HitMetadata.from_dict(d.pop("metadata"))

        organize_doc_id = d.pop("organize_doc_id")

        highlight_tokens = cast(List[str], d.pop("highlight_tokens", UNSET))

        guid = d.pop("guid")

        uri = d.pop("uri")

        _representations = d.pop("representations", UNSET)
        representations: Union[Unset, Representations]
        if isinstance(_representations, Unset):
            representations = UNSET
        else:
            representations = Representations.from_dict(_representations)

        no_references = d.pop("no_references", UNSET)

        no_citations = d.pop("no_citations", UNSET)

        h_index_sum = d.pop("h_index_sum", UNSET)

        h_index_avg = d.pop("h_index_avg", UNSET)

        twitter_popularity_score = d.pop("twitter_popularity_score", UNSET)

        github_score = d.pop("github_score", UNSET)

        duplicates = []
        _duplicates = d.pop("duplicates", UNSET)
        for duplicates_item_data in _duplicates or []:
            duplicates_item = Hit.from_dict(duplicates_item_data)

            duplicates.append(duplicates_item)

        tweets = []
        _tweets = d.pop("tweets", UNSET)
        for tweets_item_data in _tweets or []:
            tweets_item = Tweet.from_dict(tweets_item_data)

            tweets.append(tweets_item)

        github_repos = []
        _github_repos = d.pop("github_repos", UNSET)
        for github_repos_item_data in _github_repos or []:
            github_repos_item = GitHubRepo.from_dict(github_repos_item_data)

            github_repos.append(github_repos_item)

        resources = []
        _resources = d.pop("resources", UNSET)
        for componentsschemas_resources_item_data in _resources or []:
            componentsschemas_resources_item = ResourcesItem.from_dict(
                componentsschemas_resources_item_data
            )

            resources.append(componentsschemas_resources_item)

        _status = d.pop("status", UNSET)
        status: Union[Unset, PrivateDocStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = PrivateDocStatus(_status)

        status_codes = []
        _status_codes = d.pop("status_codes", UNSET)
        for status_codes_item_data in _status_codes or []:
            status_codes_item = PrivateDocStatusCode(status_codes_item_data)

            status_codes.append(status_codes_item)

        status_message = d.pop("status_message", UNSET)

        get_bibtex_id = d.pop("get_bibtex_id", UNSET)

        get_similar_docs_id = d.pop("get_similar_docs_id", UNSET)

        get_cites_id = d.pop("get_cites_id", UNSET)

        get_refs_id = d.pop("get_refs_id", UNSET)

        share_uri = d.pop("share_uri", UNSET)

        hit = cls(
            field_id=field_id,
            highlight=highlight,
            document_type=document_type,
            score=score,
            uid=uid,
            metadata=metadata,
            organize_doc_id=organize_doc_id,
            highlight_tokens=highlight_tokens,
            guid=guid,
            uri=uri,
            representations=representations,
            no_references=no_references,
            no_citations=no_citations,
            h_index_sum=h_index_sum,
            h_index_avg=h_index_avg,
            twitter_popularity_score=twitter_popularity_score,
            github_score=github_score,
            duplicates=duplicates,
            tweets=tweets,
            github_repos=github_repos,
            resources=resources,
            status=status,
            status_codes=status_codes,
            status_message=status_message,
            get_bibtex_id=get_bibtex_id,
            get_similar_docs_id=get_similar_docs_id,
            get_cites_id=get_cites_id,
            get_refs_id=get_refs_id,
            share_uri=share_uri,
        )

        hit.additional_properties = d
        return hit

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
