# rezai/web/api/valueserp/views.py
from fastapi import APIRouter, Depends

from rezai.services.valueserp.service import ValueSerpService
from rezai.web.api.valueserp.schema import (
    PlaceDetailsRequest,
    PlaceDetailsResponse,
    SearchPlacesRequest,
    SearchPlacesResponse,
)

router = APIRouter()


@router.post("/search_places", response_model=SearchPlacesResponse)
async def search_places(
    request: SearchPlacesRequest,
    valueserp_service: ValueSerpService = Depends(),
) -> SearchPlacesResponse:
    """
    Search for places using the Valueserp API.

    This endpoint will return a list of places based on the query and location provided.

    :param request: SearchPlacesRequest
    :param valueserp_service: ValueSerpService = Depends()

    :return: SearchPlacesResponse
    """
    search_results = await valueserp_service.search_places(
        request.query,
        request.location,
    )
    return SearchPlacesResponse(places_results=search_results)


@router.post("/place_details", response_model=PlaceDetailsResponse)
async def get_place_details(
    request: PlaceDetailsRequest,
    valueserp_service: ValueSerpService = Depends(),
) -> PlaceDetailsResponse:
    """
    Get place details using the Valueserp API.

    This endpoint will return the details of a place based on the data_cid provided.

    :param request: PlaceDetailsRequest
    :param valueserp_service: ValueSerpService = Depends()

    :return: PlaceDetailsResponse
    """
    place_details = await valueserp_service.get_place_details(request.data_cid)
    return PlaceDetailsResponse(place_details=place_details)
