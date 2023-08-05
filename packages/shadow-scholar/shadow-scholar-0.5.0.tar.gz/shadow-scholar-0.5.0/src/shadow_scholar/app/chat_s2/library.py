import logging
import os
import re
from dataclasses import dataclass, field
from time import time
from typing import Dict, Iterable, List, Optional, Union, cast

import requests

API_FIELDS = [
    "title",
    "abstract",
    "venue",
    "fieldsOfStudy",
    "authors",
    "isOpenAccess",
    "year",
    "corpusId",
]

S2_API_KEY = os.environ.get("S2_API_KEY", "")


LOGGER = logging.getLogger(__name__)


def get_s2_metadata(
    papers: Union["Paper", Iterable["Paper"]],
    s2_api_key: str = S2_API_KEY,
):
    start = time()

    url = (
        "https://api.semanticscholar.org/graph/v1/paper/batch?"
        f"fields={','.join(API_FIELDS)}"
    )
    header = {"x-api-key": s2_api_key}

    papers = [papers] if isinstance(papers, Paper) else papers
    missing = [p for p in papers if p.missing]

    if not missing:
        # nothing new to fetch metadata for
        return

    data = {"ids": [p.id for p in missing]}
    response = requests.post(url, headers=header, json=data)
    results = response.json()

    delta = time() - start
    LOGGER.warn(f"S2 Metadata :: {delta:.2f}s :: {len(results)} items.")

    for paper, paper_metadata in zip(missing, results):
        if paper_metadata:
            try:
                paper.metadata.update(cast(dict, paper_metadata))
            except Exception as e:
                LOGGER.error(f"Failed to update metadata for {paper.id}: {e}")
                continue


@dataclass
class Paper:
    id: str
    metadata: dict = field(default_factory=dict)
    score: float = -1.0
    short_id: Optional[int] = None

    def __str__(self) -> str:
        return f"Paper({self.id})"

    @classmethod
    def id_from_s2_url(cls, url: str) -> Union[str, None]:
        is_valid_url = re.match(
            r"https://(www.)?semanticscholar.org/paper.*?/([a-f0-9]+)", url
        )
        if not is_valid_url:
            return None

        sha1 = is_valid_url.group(2)
        return sha1

    @classmethod
    def id_from_arxiv_url(cls, url: str) -> Union[str, None]:
        is_valid_url = re.match(r"https://(www.)?arxiv.org/abs/(.+)", url)
        if not is_valid_url:
            return None

        arxiv_id = is_valid_url.group(2)
        return f"arxiv:{arxiv_id}"

    @classmethod
    def from_url(cls, url: str, **attrs) -> Optional["Paper"]:
        id_ = cls.id_from_s2_url(url) or cls.id_from_arxiv_url(url)
        return cls(id_, **attrs) if id_ else None

    @property
    def missing(self) -> bool:
        return len(self.metadata) == 0

    @property
    def authors(self) -> List[str]:
        return [author["name"] for author in self.metadata.get("authors", [])]

    @property
    def url(self) -> str:
        return f"https://api.semanticscholar.org/{self.id}"

    @property
    def year(self) -> Union[int, None]:
        if (year := self.metadata.get("year")) is not None:
            year = int(year)
        return year

    @property
    def title(self) -> str:
        return self.metadata.get("title", "")

    @property
    def abstract(self) -> str:
        return self.metadata.get("abstract", "")

    @property
    def is_open_access(self) -> bool:
        return self.metadata.get("isOpenAccess", False)

    @property
    def venue(self) -> str:
        return self.metadata.get("venue", "")

    @property
    def corpus_id(self) -> str:
        return self.metadata.get("corpusId", "")

    def _truncate(self, text: str, cols: int = 70) -> str:
        if len(text) > (cols - 3):
            return text[:cols] + "..."
        return text

    def html_format_paper(self) -> str:
        title = (
            f'<p><a href="{self.url}" target="_blank">'
            f"<b>{self._truncate(self.title)}</b></a> ({self.year})</p>"
        )
        authors = f'<p><i>{self._truncate(", ".join(self.authors))}</i></p>'
        abstract = f'<p>{self._truncate(self.abstract or "")}</p>'
        return "\n".join([title, authors, abstract])

    def html_format_id(self) -> str:
        short_id = (
            f'<span class="span-major">[{self.short_id}]</span>'
            if self.short_id
            else ""
        )

        span_class = "span-minor" if short_id else "span-minor"
        title_id = (
            f'<span class="{span_class}">'
            f'<a href="{self.url}" target="_blank">{self.corpus_id}</a>'
            "</span>"
        )
        score = f"<i>{self.score:.2f}</i>"
        return (
            '<div id="id-score-table-container">'
            f"<p>{short_id}</p><p>{title_id}</p>"
            f'<p id="score-para">{score}</p>'
            "</div>"
        )


@dataclass
class Stack:
    papers: Dict[str, Paper] = field(default_factory=dict)
    s2_api_key: str = S2_API_KEY

    def append(self, paper: Paper):
        if paper.id not in self.papers:
            self.papers[paper.id] = paper
            paper.short_id = len(self.papers)
        elif paper.score > self.papers[paper.id].score:
            self.papers[paper.id].score = paper.score

    def extend(self, papers: Iterable[Paper]):
        for paper in papers:
            self.append(paper)

    def fetch(self):
        get_s2_metadata(self.papers.values(), s2_api_key=self.s2_api_key)
        for p in list(self.papers.keys()):
            if self.papers[p].missing:
                self.papers.pop(p)

    @property
    def sorted(self) -> List[Paper]:
        return sorted(self.papers.values(), key=lambda p: -p.score)

    def __len__(self):
        return len(self.papers)

    def __getitem__(self, key):
        return self.papers[key]

    def __iter__(self):
        return iter(self.papers)

    def __str__(self) -> str:
        return (
            f"Stack_{len(self.papers)}(\n"
            + "\n".join(f"\t{paper}," for paper in self.papers)
            + "\n)"
        )

    def table(self) -> List[List[str]]:
        if len(self) == 0:
            # we need to return something otherwise UI will break
            return [["", ""]]

        return [
            [p.html_format_id(), p.html_format_paper()] for p in self.sorted
        ]
