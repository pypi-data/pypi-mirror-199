import os
import re
import urllib.parse
from dataclasses import dataclass, field
from time import time
from typing import Dict, Iterable, List, NamedTuple, Set, Tuple, Union, cast

import requests

from .library import S2_API_KEY, Paper

S2_SEARCH_ENDPOINT = "https://api.semanticscholar.org/graph/v1/paper/search/"
GOOGLE_SEARCH_API_KEY = os.environ.get("GOOGLE_SEARCH_API_KEY", "")


class BaseSearchEndpoint:
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key

    def encode(self, text: str) -> str:
        text = re.sub(r"^\-\s*", "", text)
        text = re.sub(r"[\"\']+", "", text)
        text = re.sub(r"(^\s+|\s+$)", "", text)
        return text

    def __call__(self, query: str, max_results: int = 1000) -> List[Paper]:
        raise NotImplementedError()


class S2SearchEndpoint(BaseSearchEndpoint):
    def __init__(
        self,
        endpoint: str = S2_SEARCH_ENDPOINT,
        api_key: str = S2_API_KEY,
    ):
        super().__init__(endpoint=endpoint, api_key=api_key)

    def encode(self, text: str) -> str:
        text = super().encode(text)
        return text.replace(" ", "+")

    def __call__(self, query: str, max_results: int = 1000) -> List[Paper]:
        start = time()
        query = self.encode(query)
        url = f"{self.endpoint}?query={query}"
        headers = {"x-api-key": self.api_key}
        data = requests.get(url, headers=headers).json()
        filtered = [
            Paper(p["paperId"], score=1 / i)
            for i, p in enumerate(data["data"], start=1)
        ][:max_results]
        delta = time() - start

        print(f"S2 Search :: {delta:.2f}s :: {len(filtered)} results.")

        return filtered


class GoogleSearchEndpoint(BaseSearchEndpoint):
    def __init__(
        self,
        endpoint: str = "https://www.googleapis.com/customsearch/v1",
        api_key: str = GOOGLE_SEARCH_API_KEY,
        cx: str = "602714345f3a24773",
        max_results: int = 1000,
    ):
        super().__init__(endpoint=endpoint, api_key=api_key)
        self.cx = cx

    def encode(self, text: str) -> str:
        text = super().encode(text)
        return urllib.parse.quote(text)

    def __call__(self, query: str, max_results: int = 1000) -> List[Paper]:
        start = time()
        query = self.encode(query)
        url = (
            f"https://www.googleapis.com/customsearch/v1/siterestrict?"
            f"&key={self.api_key}"
            f"&cx={self.cx}"
            f"&q={query}"
        )
        response = requests.get(url).json()
        papers = [
            Paper.from_url(url=r["link"], score=1 / i)
            for i, r in enumerate(cast(list, response["items"]), start=1)
        ]
        filtered = [p for p in papers if p is not None][:max_results]
        delta = time() - start
        print(f"Google Search :: {delta:.2f}s :: {len(filtered)} results.")

        return filtered


class Query(NamedTuple):
    user_query: Union[str, None]
    system_query: Union[str, None]

    def __bool__(self):
        return self.text != ""

    @property
    def text(self) -> str:
        return self.user_query or self.system_query or ""


@dataclass
class Queries:
    queries: Dict[str, Query] = field(default_factory=dict)
    used: Set[str] = field(default_factory=set)

    def add(self, queries: List[Tuple[Union[str, None], Union[str, None]]]):
        for query in queries:
            query = Query(*query)
            if not query:
                continue
            self.queries[query.text] = query

    def use(self) -> Iterable[str]:
        for query in self.queries:
            if query not in self.used:
                self.used.add(query)
                yield query

    def list(self) -> List[Tuple[Union[str, None], Union[str, None]]]:
        return list(self.queries.values())
