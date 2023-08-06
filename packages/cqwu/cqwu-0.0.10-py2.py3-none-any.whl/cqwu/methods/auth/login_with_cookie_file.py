from os.path import exists

import cqwu
from cqwu.errors.auth import CookieError


class LoginWithCookieFile:
    async def login_with_cookie_file(
        self: "cqwu.Client",
    ):
        """
        使用 cookie 文本文件登录
        """
        if not exists(self.cookie_file_path):
            raise CookieError()

        try:
            with open(self.cookie_file_path, "r") as f:
                self.cookie = f.read()  # noqa
            await self.login_with_cookie()
        except Exception as e:
            raise CookieError() from e
