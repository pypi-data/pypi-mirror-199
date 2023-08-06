import asyncio
from typing import Coroutine, Optional
from httpx import AsyncClient, Cookies

from cqwu.methods import Methods
from cqwu.types import User


class Client(Methods):
    """CQWU main client."""

    def __init__(
        self,
        username: int = None,
        password: str = None,
        cookie: str = None,
        cookie_file_path: str = "cookie.txt",
        timeout: int = 10,
    ):
        self.username = username
        self.password = password
        self.cookie = cookie
        self.cookie_file_path = cookie_file_path
        self.host = "http://ehall.cqwu.edu.cn"
        self.auth_host = "http://authserver.cqwu.edu.cn"
        self.web_ehall_path = ""
        self.cookies = Cookies()
        self.request = AsyncClient(timeout=timeout)
        self.loop = asyncio.get_event_loop()
        self.me: Optional[User] = None
        self._use_password_login = False
        self.xue_nian = 2022  # 学年
        self.xue_qi = 1  # 学期 0 为第一学期， 1 为第二学期

    @staticmethod
    def get_input(word: str = "", is_int: bool = False):
        while True:
            value = input(f"请输入{word}：")
            if not value:
                continue
            if is_int:
                try:
                    value = int(value)
                except ValueError:
                    continue
            confirm = (input(f'确认是 "{value}" 吗？(y/N): ')).lower()
            if confirm == "y":
                break
        return value

    def sync(self, coroutine: Coroutine):
        """
        同步执行异步函数

        Args:
            coroutine (Coroutine): 异步函数

        Returns:
            该异步函数的返回值
        """
        return self.loop.run_until_complete(coroutine)
