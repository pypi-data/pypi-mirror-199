from urllib.parse import urlparse

import cqwu


class Oauth:
    async def oauth(
        self: "cqwu.Client",
        url: str,
        host: str = None,
    ):
        """
        使用 统一身份认证平台 登录子系统，并且保存 cookie
        """
        host = host or urlparse(url).hostname
        html = await self.request.get(url, follow_redirects=True)
        return None if html.url.host != host else html
