from typing import Optional, Union
from bs4 import BeautifulSoup

import cqwu
from cqwu import types
from cqwu.errors.auth import CookieError


def get_value_from_soup(soup: BeautifulSoup, attr_id: str) -> Union[type(None), str, int]:
    try:
        data = soup.find("input", attrs={"id": attr_id})["value"]
        try:
            return int(data)
        except ValueError:
            return data
    except (ValueError, TypeError, KeyError):
        return None


class GetMe:
    async def get_me(
        self: "cqwu.Client",
    ) -> Optional["types.User"]:
        """
        获取个人信息

        Returns:
            types.User: 个人信息
        """
        url = "http://218.194.176.8/prizepunishnv/studentInfoManageStudentNV!forwardStudentInfo.action"
        html = await self.oauth(url)
        if not html:
            raise CookieError()
        if html.url != url:
            html = await self.request.get(url)
        if html.url != url:
            raise CookieError()
        soup = BeautifulSoup(html.text, "lxml")
        data = {
            "username": "detail_xh",
            "name": "detail_xm",
            "sex": "detail_xb",
            "age": "detail_nl",
            "grade": "detail_nj",
            "institute": "detail_xy",
            "now_class": "detail_bj",
            "join_year": "detail_rxnj",
            "birthday": "detail_csrq",
            "sfz": "detail_sfzh",
            "level": "detail_pycc",
            "home": "detail_hkszd",
        }
        temp = {key: get_value_from_soup(soup, value) for key, value in data.items()}
        temp["password"] = self.password
        try:
            temp["specialty"] = soup.find_all("input", attrs={"id": "detail_xy"})[1]["value"]
        except (ValueError, TypeError, KeyError, IndexError):
            temp["specialty"] = None
        return types.User(**temp)
