import cqwu
from cqwu.errors.auth import CookieError


class LoginWithCookie:
    async def login_with_cookie(
        self: "cqwu.Client",
        cookie: str = None,
    ):
        """
        使用 cookie 登录
        """
        cookie = cookie or self.cookie
        if not cookie:
            raise CookieError()
        self.cookie = cookie  # noqa
        try:
            data = self.cookie.split(";")
            for cookie in data:
                if not cookie:
                    continue
                key, value = cookie.split("=")
                self.cookies.set(key, value)
                self.request.cookies.set(key, value)
            self.me = await self.get_me()  # noqa
        except Exception as e:
            raise CookieError() from e
