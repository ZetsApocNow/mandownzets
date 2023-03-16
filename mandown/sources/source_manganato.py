"""
Source file for readmanganato.com
"""
# pylint: disable=invalid-name

import re

import requests
from bs4 import BeautifulSoup

from ..base import BaseChapter, BaseMetadata
from .base_source import BaseSource


class MangaNatoSource(BaseSource):
    name = "MangaNato"
    domains = [
        "https://manganato.com",
        "https://readmanganato.com",
        "https://chapmanganato.com",
    ]
    headers = {"Referer": "https://readmanganato.com/"}

    def __init__(self, url: str) -> None:
        super().__init__(url)
        self.id = self.url_to_id(url)
        self._scripts: str | None = None

    def fetch_metadata(self) -> BaseMetadata:
        soup = BeautifulSoup(self._get_scripts(), "lxml")
        title: str = soup.h1.next_element
        authors_genres = soup.select("td > a.a-h")
        authors: list[str] = []
        genres: list[str] = []
        for el in authors_genres:
            if el["href"].startswith("https://manganato.com/author"):
                authors.append(el.next_element)
            elif el["href"].startswith("https://manganato.com/genre"):
                genres.append(el.next_element)

        cover_img = next(iter(soup.select("span.info-image > img.img-loading")))
        cover_art: str = cover_img["src"]

        description = soup.select_one(
            "#panel-story-info-description > h3"
        ).nextSibling.text.strip()

        return BaseMetadata(title, authors, self.url, genres, description, cover_art)

    def fetch_chapter_list(self) -> list[BaseChapter]:
        soup = BeautifulSoup(self._get_scripts(), "lxml")
        chapters = [
            BaseChapter(c.next_element, c["href"])
            for c in soup.select("a.chapter-name")
        ]
        chapters.reverse()
        return chapters

    def fetch_chapter_image_list(self, chapter: BaseChapter) -> list[str]:
        soup = BeautifulSoup(requests.get(chapter.url).text, "lxml")
        images = []
        for i in soup.find_all("img"):
            if not i["src"].startswith("https://readmanganato.com"):
                images.append(i["src"])
        return images

    def _get_scripts(self) -> str:
        if self._scripts:
            return self._scripts

        self._scripts = requests.get(self.url).text
        return self._scripts

    @classmethod
    def url_to_id(cls, url: str) -> str:
        *_, last_item = filter(None, url.split("/"))
        return last_item

    @staticmethod
    def check_url(url: str) -> bool:
        return bool(
            re.match(r"https://readmanganato.com/.*", url)
            or re.match(r"https://chapmanganato.com/.*", url)
        )


def get_class() -> type[BaseSource]:
    return MangaNatoSource
