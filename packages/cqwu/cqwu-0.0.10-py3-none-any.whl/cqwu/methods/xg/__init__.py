import cqwu

from .get_cp import GetCP
from .get_public_cp import GetPublicCP
from .get_score import GetScore
from ...errors import CookieError


class XG(
    GetCP,
    GetPublicCP,
    GetScore,
):
    async def oauth_xg(
        self: "cqwu.Client",
    ):
        url = "http://xg.cqwu.edu.cn/xsfw/sys/zhcptybbapp/*default/index.do#/cjcx"
        html = await self.oauth(url)
        if not html:
            raise CookieError()
        if html.url != url:
            raise CookieError()
        url = "http://xg.cqwu.edu.cn/xsfw/sys/swpubapp/indexmenu/getAppConfig.do"
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,hu;q=0.5',
            'Connection': 'keep-alive',
            'Referer': 'http://xg.cqwu.edu.cn/xsfw/sys/zhcptybbapp/*default/index.do',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51',
        }
        params = {
            'appId': '5275772372599202',
            'appName': 'zhcptybbapp',
            'v': '021534151969418724',
        }
        await self.request.get(url, headers=headers, params=params)
