from pydantic import BaseModel


class ConferenceInfo(BaseModel):
    name: str
    website: str
    location: str
    start_date: str
    end_date: str
