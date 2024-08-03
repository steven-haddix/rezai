# rezai/web/api/valueserp/schema.py
from typing import List

from pydantic import BaseModel


class SearchPlacesRequest(BaseModel):
    query: str
    location: str


class PlaceDetailsRequest(BaseModel):
    data_cid: str


class PlaceResult(BaseModel):
    title: str
    data_cid: str
    address: str
    category: str
    rating: float


class SearchPlacesResponse(BaseModel):
    places_results: List[PlaceResult]


class PlaceDetails(BaseModel):
    data_id: str
    data_cid: str
    title: str
    address: str
    website: str
    rating: float
    reviews: int
    type: str
    category: str
    phone: str


class PlaceDetailsResponse(BaseModel):
    place_details: PlaceDetails
