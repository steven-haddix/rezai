from typing import Annotated, Any, AsyncIterator, Optional

from fastapi import Depends
from langchain.tools import tool
from langchain_anthropic import ChatAnthropic
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.graph import CompiledGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent
from pydantic.v1 import BaseModel, SecretStr

from rezai.db.dao.restaurant_dao import RestaurantDAO
from rezai.db.models.restaurant_model import Restaurant
from rezai.services.valueserp.service import ValueSerpService
from rezai.services.youcom.service import YouComService
from rezai.settings import settings

memory = MemorySaver()


class State(BaseModel):
    messages: Annotated[list[Any], add_messages]
    tool_results: dict[str, Any] = {}


def create_restaurant_agent(
    valueserp_service: ValueSerpService,
    youcom_service: YouComService,
    restaurant_dao: RestaurantDAO,
) -> CompiledGraph:
    """
    Creates and returns a compiled graph for a restaurant agent.

    This function sets up a restaurant agent with various tools for searching restaurants,
    getting restaurant details, performing web searches, and interacting with a restaurant database.
    It uses the provided services to implement these tools and creates a ReactAgent using LangChain.

    :param valueserp_service: A service for performing restaurant searches and retrieving place details.
    :type valueserp_service: ValueSerpService
    :param youcom_service: A service for performing web searches.
    :type youcom_service: YouComService
    :param restaurant_dao: A data access object for interacting with the restaurant database.
    :type restaurant_dao: RestaurantDAO
    :return: A compiled graph representing the restaurant agent, ready to be executed.
    :rtype: CompiledGraph

    The function defines several tool functions within its scope:
    - search_restaurants: Searches for restaurants based on a query and location.
    - get_restaurant_details: Retrieves detailed information about a specific restaurant.
    - web_search: Performs a general web search.
    - lookup_restaurants: Searches for restaurants in the database.
    - save_restaurant: Saves a new restaurant to the database.

    These tools are then combined with a language model to create a ReactAgent, which is
    returned as a compiled graph.

    Note:
    The actual implementation of the tools and the creation of the ReactAgent are defined
    within this function but are not shown in this docstring.
    """

    @tool
    async def search_restaurants(query: str, location: str) -> Any:
        """
        Search for restaurants based on a given query and location.

        :param query: The search query for restaurants.
        :param location: The location or area to search for restaurants.

        :return: Returns the search results containing restaurant information.
        """
        return await valueserp_service.search_places(query, location)

    @tool
    def get_restaurant_details(data_cid: str) -> Any:
        """
        Get the details of a restaurant based on the data CID.

        :param data_cid: The data CID of the restaurant.

        :return: The details of the restaurant.
        """
        return valueserp_service.get_place_details(data_cid)

    @tool
    def web_search(query: str) -> Any:
        """
        Search the web for information based on a given query.

        :param query: The search query for web search.

        :return: The search results containing web search information.
        """
        return youcom_service.get_ai_snippets_for_query(query)

    @tool
    async def lookup_restaurants(**kwargs: Any) -> list[Restaurant]:
        """
        Lookup restaurants based on the given keyword arguments.

        :param kwargs: The keyword arguments to filter restaurants.
        :return: The search results containing restaurant information.
        """
        return await restaurant_dao.filter(**kwargs)

    @tool
    async def save_restaurant(
        title: str,
        type: str,  # noqa: WPS125
        category: str,
        website: Optional[str] = None,
        description: Optional[str] = None,
        address: Optional[str] = None,
        phone: Optional[str] = None,
        rating: Optional[float] = None,
        reviews: Optional[int] = None,
        unclaimed: Optional[bool] = None,
        hours: Optional[str] = None,
        opening_hours: Optional[str] = None,
        people_also_search_for: Optional[str] = None,
        menu: Optional[str] = None,
        reservations: Optional[str] = None,
        order: Optional[str] = None,
        order_food: Optional[str] = None,
    ) -> None:
        """
        Save a restaurant to the database.

        :param title: The title of the restaurant.
        :param type: The type of the restaurant.
        :param category: The category of the restaurant.
        :param website: The website of the restaurant.
        :param description: The description of the restaurant.
        :param address: The address of the restaurant.
        :param phone: The phone number of the restaurant.
        :param rating: The rating of the restaurant.
        :param reviews: The number of reviews of the restaurant.
        :param unclaimed: Whether the restaurant is unclaimed.
        :param hours: The hours of the restaurant.
        :param opening_hours: The opening hours of the restaurant.
        :param people_also_search_for: The related searches for the restaurant.
        :param menu: The menu of the restaurant.
        :param reservations: The reservation information of the restaurant.
        :param order: The order information of the restaurant.
        :param order_food: The order food information of the restaurant.
        """
        restaurant = Restaurant(
            title=title,
            type=type,
            category=category,
            website=website,
            description=description,
            address=address,
            phone=phone,
            rating=rating,
            reviews=reviews,
            unclaimed=unclaimed,
            hours=hours,
            opening_hours=opening_hours,
            people_also_search_for=people_also_search_for,
            menu=menu,
            reservations=reservations,
            order=order,
            order_food=order_food,
        )
        await restaurant_dao.create_restaurant(restaurant)

    llm = ChatAnthropic(
        model_name="claude-3-haiku-20240307",
        api_key=(
            SecretStr(settings.anthropic_api_key)
            if settings.anthropic_api_key
            else None
        ),
        timeout=None,
        max_retries=3,
        temperature=0.5,
        base_url=None,
        stop=None,
    )

    tools = [
        search_restaurants,
        get_restaurant_details,
        web_search,
        lookup_restaurants,
        save_restaurant,
    ]

    system_prompt = """
        You are an AI restaurant concierge assistant. Your role is to help users find restaurants,
        provide information about specific restaurants, and manage a database of restaurant information. You will be
        given a set of tools to accomplish these tasks.
        If a user hasn't given you a location, always ask instead of seaching with no location reference.
    """

    react_agent = create_react_agent(
        llm,
        tools=tools,  # type: ignore
        checkpointer=memory,
        messages_modifier=system_prompt,
    )

    return react_agent


class RestaurantAgentContainer:
    def __init__(
        self,
        valueserp_service: ValueSerpService,
        youcom_service: YouComService,
        restaurant_dao: RestaurantDAO,
    ) -> None:
        self.graph = self.create_graph(
            valueserp_service,
            youcom_service,
            restaurant_dao,
        )

    @staticmethod
    def create_graph(
        valueserp_service: ValueSerpService,
        youcom_service: YouComService,
        restaurant_dao: RestaurantDAO,
    ) -> CompiledGraph:
        return create_restaurant_agent(
            valueserp_service,
            youcom_service,
            restaurant_dao,
        )

    def run_graph(
        self,
        input_data: dict[str, Any],
        config: RunnableConfig,
        **kwargs: Any,
    ) -> AsyncIterator[dict[str, Any] | Any]:
        return self.graph.astream(input_data, config=config, **kwargs)


def get_restaurant_agent_container(
    valueserp_service: ValueSerpService = Depends(),
    youcom_service: YouComService = Depends(),
    restaurant_dao: RestaurantDAO = Depends(),
) -> RestaurantAgentContainer:
    """
    Dependency to get the restaurant agent container.

    :param valueserp_service: The ValueSerp service.
    :param youcom_service: The YouCom service.
    :param restaurant_dao: The restaurant DAO.
    :return: The restaurant agent container.
    """
    return RestaurantAgentContainer(
        valueserp_service=valueserp_service,
        youcom_service=youcom_service,
        restaurant_dao=restaurant_dao,
    )
