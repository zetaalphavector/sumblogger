# flake8: noqa
from typing import Any, Dict, List, Optional, Type, TypeVar

import attr

T = TypeVar("T", bound="GitHubRepo")


@attr.s(auto_attribs=True)
class GitHubRepo:
    """
    Attributes:
        stars (int): A number of stars for the repository. Example: 500.
        forks (int): A number of forks of the repository. Example: 1000.
        gh_url (str): An URL of the repository. Example: https://github.com/tensorflow/tensorflow.
        mentioned_in_paper (bool): Whether the repository is mentioned in the paper (is official).
        name (str): A name of the repository.
        owner (str): An owner of the repository.
        description (Optional[str]): Description of the repository.
    """

    stars: int
    forks: int
    gh_url: str
    mentioned_in_paper: bool
    name: str
    owner: str
    description: Optional[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        stars = self.stars
        forks = self.forks
        gh_url = self.gh_url
        mentioned_in_paper = self.mentioned_in_paper
        name = self.name
        owner = self.owner
        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "stars": stars,
                "forks": forks,
                "gh_url": gh_url,
                "mentioned_in_paper": mentioned_in_paper,
                "name": name,
                "owner": owner,
                "description": description,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        stars = d.pop("stars")

        forks = d.pop("forks")

        gh_url = d.pop("gh_url")

        mentioned_in_paper = d.pop("mentioned_in_paper")

        name = d.pop("name")

        owner = d.pop("owner")

        description = d.pop("description")

        git_hub_repo = cls(
            stars=stars,
            forks=forks,
            gh_url=gh_url,
            mentioned_in_paper=mentioned_in_paper,
            name=name,
            owner=owner,
            description=description,
        )

        git_hub_repo.additional_properties = d
        return git_hub_repo

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
