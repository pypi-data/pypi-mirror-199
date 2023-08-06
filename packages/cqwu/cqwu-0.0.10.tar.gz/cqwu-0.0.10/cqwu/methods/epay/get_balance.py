from typing import Optional
from bs4 import BeautifulSoup

import cqwu
from cqwu.errors.auth import CookieError


class GetBalance:
    async def get_balance(
        self: "cqwu.Client",
    ) -> Optional[str]:
        """
        获取校园卡余额

        Returns:
            str: 余额
        """
        url = "http://218.194.176.214:8382/epay/thirdapp/balance"
        html = await self.oauth(url)
        if not html:
            raise CookieError()
        if html.url != url:
            raise CookieError()
        soup = BeautifulSoup(html.text, "lxml")
        try:
            return soup.find_all("div", "weui-cell__ft")[2].next
        except (ValueError, TypeError, KeyError, IndexError):
            return ""
