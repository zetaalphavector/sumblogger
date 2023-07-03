# flake8: noqa
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..models.tweet_tweet_type import TweetTweetType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Tweet")


@attr.s(auto_attribs=True)
class Tweet:
    """
    Attributes:
        tweet_user_profile_url (str):  Example: https://twitter.com/Twitter.
        tweet_user_name (str):  Example: Twitter.
        tweet_text (str):  Example: who should we follow today?.
        tweet_url (str):  Example: https://twitter.com/Twitter/status/1364606837534978052?s=20.
        tweet_timestamp (str):  Example: 2021-03-02T19:40:02.577424.
        tweet_user_profile_picture_url (Optional[str]):  Example:
            https://pbs.twimg.com/profile_images/1354479643882004483/Btnfm47p_400x400.jpg.
        tweet_type (Union[Unset, TweetTweetType]):  Example: tweet.
    """

    tweet_user_profile_url: str
    tweet_user_name: str
    tweet_text: str
    tweet_url: str
    tweet_timestamp: str
    tweet_user_profile_picture_url: Optional[str]
    tweet_type: Union[Unset, TweetTweetType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tweet_user_profile_url = self.tweet_user_profile_url
        tweet_user_name = self.tweet_user_name
        tweet_text = self.tweet_text
        tweet_url = self.tweet_url
        tweet_timestamp = self.tweet_timestamp
        tweet_user_profile_picture_url = self.tweet_user_profile_picture_url
        tweet_type: Union[Unset, str] = UNSET
        if not isinstance(self.tweet_type, Unset):
            tweet_type = self.tweet_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tweet_user_profile_url": tweet_user_profile_url,
                "tweet_user_name": tweet_user_name,
                "tweet_text": tweet_text,
                "tweet_url": tweet_url,
                "tweet_timestamp": tweet_timestamp,
                "tweet_user_profile_picture_url": tweet_user_profile_picture_url,
            }
        )
        if tweet_type is not UNSET:
            field_dict["tweet_type"] = tweet_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tweet_user_profile_url = d.pop("tweet_user_profile_url")

        tweet_user_name = d.pop("tweet_user_name")

        tweet_text = d.pop("tweet_text")

        tweet_url = d.pop("tweet_url")

        tweet_timestamp = d.pop("tweet_timestamp")

        tweet_user_profile_picture_url = d.pop("tweet_user_profile_picture_url")

        _tweet_type = d.pop("tweet_type", UNSET)
        tweet_type: Union[Unset, TweetTweetType]
        if isinstance(_tweet_type, Unset):
            tweet_type = UNSET
        else:
            tweet_type = TweetTweetType(_tweet_type)

        tweet = cls(
            tweet_user_profile_url=tweet_user_profile_url,
            tweet_user_name=tweet_user_name,
            tweet_text=tweet_text,
            tweet_url=tweet_url,
            tweet_timestamp=tweet_timestamp,
            tweet_user_profile_picture_url=tweet_user_profile_picture_url,
            tweet_type=tweet_type,
        )

        tweet.additional_properties = d
        return tweet

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
