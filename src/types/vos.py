from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from src.types.conference_blog import ConferenceInfo


class Terminology(BaseModel):
    cluster: str
    clusters: str
    item: str
    items: str
    link: str
    links: str
    link_strength: str
    total_link_strength: str
    title: str
    abstract: str
    authors: str


class Templates(BaseModel):
    item_description: str


class Styles(BaseModel):
    description_heading: str


class Parameters(BaseModel):
    item_size_variation: float
    largest_component: bool
    attraction: float
    repulsion: float
    max_n_links: Optional[int] = None


class Weights(BaseModel):
    Influence: float
    Relevance: float
    Popularity: float
    Citations: float


class Link(BaseModel):
    source_id: str
    target_id: str
    strength: float


class Summary(BaseModel):
    keywords: Optional[List[str]] = None
    topic: Optional[str] = None
    long_summary: Optional[str] = None
    tldr_summary: str


class Item(BaseModel):
    id: str
    heading: Optional[str] = None
    title: str
    authors: Optional[str] = None
    label: str
    abstract: str
    uri: Optional[str] = None
    img_url: Optional[str] = None
    x: float
    y: float
    cluster: int
    weights: Weights
    type: Optional[str] = None
    normalized_w: Optional[Weights] = None
    impact_score: Optional[float] = None
    summary: Optional[Summary] = None


class Cluster(BaseModel):
    cluster: int
    label: Optional[str] = None
    summary: Optional[Summary] = None


class VosNetwork(BaseModel):
    items: List[Item]
    links: List[Link]
    clusters: Optional[List[Cluster]] = None
    blog_title: Optional[str] = None
    blog_intro: Optional[str] = None
    blog_conclusion: Optional[str] = None


class ClusterColor(BaseModel):
    cluster: int
    color: str


class ColorSchemes(BaseModel):
    cluster_colors: List[ClusterColor]


class VosConfig(BaseModel):
    terminology: Terminology
    color_schemes: Optional[ColorSchemes] = None
    templates: Templates
    styles: Styles
    parameters: Parameters

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        kwargs.pop("exclude_none", None)
        return super().dict(*args, exclude_none=True, **kwargs)


class VosClusteredDocuments(BaseModel):
    config: VosConfig
    network: VosNetwork


class VosConferenceClusteredDocuments(VosClusteredDocuments):
    conference_info: ConferenceInfo
