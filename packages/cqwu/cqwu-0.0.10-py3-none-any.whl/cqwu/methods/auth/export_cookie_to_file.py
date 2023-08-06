import cqwu
from cqwu.errors.auth import CookieError


class ExportCookieToFile:
    async def export_cookie_to_file(
        self: "cqwu.Client",
    ):
        """
        导出 cookie 到文件
        """
        if not self.cookies:
            raise CookieError()

        data = "".join(f"{key}={value};" for key, value in self.cookies.items())
        with open(self.cookie_file_path, "w") as f:
            f.write(data)
