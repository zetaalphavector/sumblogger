from enum import Enum


class TweetTweetType(str, Enum):
    TWEET = "tweet"
    QUOTED = "quoted"
    RETWEET = "retweet"

    def __str__(self) -> str:
        return str(self.value)
