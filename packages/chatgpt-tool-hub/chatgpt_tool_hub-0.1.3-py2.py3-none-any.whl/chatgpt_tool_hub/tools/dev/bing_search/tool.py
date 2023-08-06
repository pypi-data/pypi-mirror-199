"""Tool for the Bing search API."""

from tools.base_tool import BaseTool
from tools.dev.utilities import BingSearchAPIWrapper


class BingSearchRun(BaseTool):
    """Tool that adds the capability to query the Bing search API."""

    name = "Bing Search"
    description = (
        "A wrapper around Bing Search. "
        "Useful for when you need to answer questions about current events. "
        "Input should be a search query."
    )
    api_wrapper: BingSearchAPIWrapper

    def _run(self, query: str) -> str:
        """Use the tool."""
        return self.api_wrapper.run(query)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("BingSearchRun does not support async")
