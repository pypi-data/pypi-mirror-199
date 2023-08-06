import cqwu


class LoginWebVPN:
    async def login_web_vpn(
        self: "cqwu.Client",
    ):
        """
        登录 WebVPN
        """
        if not self._use_password_login:
            return
        url = "https://webvpn.cqwu.edu.cn"
        ehall_html = await self.request.get(url, follow_redirects=True)
        self.web_ehall_path = self.get_web_vpn_host(ehall_html.url)  # noqa
        await self.oauth("http://authserver.cqwu.edu.cn/authserver/login?service=https://clientvpn.cqwu.edu.cn/enlink/api/client/callback/cas")
        auth_html = await self.request.get(
            f"{self.web_ehall_path}/login", follow_redirects=True
        )
        if web_auth_path := self.get_web_vpn_host(auth_html.url):
            await self.login_with_password(auth_host=web_auth_path)
