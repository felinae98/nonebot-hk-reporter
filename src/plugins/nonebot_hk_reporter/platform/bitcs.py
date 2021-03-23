from ..post import Post
from ..types import *
from .platform import PlatformNoTarget

import httpx
from bs4 import BeautifulSoup as bs


class BitCS(PlatformNoTarget):

    categories = {}
    enable_tag = False
    platform_name = 'bitcs'

    @staticmethod
    async def get_account_name(_) -> str:
        return '北理工计算机学院'

    async def get_sub_list(self) -> list[RawPost]:
        async with httpx.AsyncClient() as client:
            res = await client.get('https://cs.bit.edu.cn/')
        soup = bs(res.text, 'html.parser')
        a_tags = soup.find(class_='rt02').find('ul').find_all('a')
        return [{
                'url': 'https://cs.bit.edu.cn/' + a['href'],
                'title': a.text.strip()
                } for a in a_tags]

    def get_id(self, post: RawPost) -> Any:
        return post['url']

    def get_date(self, _) -> None:
        return None

    async def parse(self, raw_post: RawPost) -> Post:
        return Post(
                    'bitcs', raw_post['title'], url=raw_post['url'], target_name='北理计算机',
                    override_use_pic=False
                )

