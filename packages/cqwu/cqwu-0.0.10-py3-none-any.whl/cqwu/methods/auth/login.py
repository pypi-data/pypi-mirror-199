import contextlib
from os.path import exists

import cqwu
from cqwu.errors.auth import CookieError


class Login:
    async def login(
        self: "cqwu.Client",
    ):
        """ 登录 """
        with contextlib.suppress(CookieError):
            if self.cookie:
                await self.login_with_cookie()
            elif exists(self.cookie_file_path):
                await self.login_with_cookie_file()
            return
        if self.username and self.password:
            await self.login_with_password()
        else:
            raise CookieError()
