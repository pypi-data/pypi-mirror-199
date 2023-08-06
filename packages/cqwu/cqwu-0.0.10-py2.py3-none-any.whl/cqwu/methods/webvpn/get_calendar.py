import base64
from typing import Tuple, List, Union

from bs4 import BeautifulSoup

import cqwu
from cqwu.errors import CookieError
from cqwu.types.calendar import AiCourse


class GetCalendar:
    async def get_calendar(
        self: "cqwu.Client",
        xue_nian: int = None,
        xue_qi: int = None,
        use_model: bool = False,
    ) -> Union[str, List[AiCourse]]:
        """ 获取课程表 """
        xue_nian = xue_nian or self.xue_nian
        xue_qi = xue_qi or self.xue_qi
        jw_html = await self.request.get(
            f"{self.web_ehall_path}/appShow?appId=5299144291521305", follow_redirects=True
        )
        if "教学管理服务平台" not in jw_html.text:
            raise CookieError
        jw_host = self.get_web_vpn_host(jw_html.url)
        jw_url = f"{jw_host}/cqwljw/student/wsxk.xskcb10319.jsp"
        params = {
            "params": base64.b64encode(f"xn={xue_nian}&xq={xue_qi}".encode()).decode(),
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Referer': f'{jw_host}/cqwljw/student/xkjg.wdkb.jsp?menucode=S20301',
            'Sec-Fetch-Dest': 'iframe',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41',
            'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        jw_html = await self.request.get(jw_url, params=params, headers=headers, timeout=60, follow_redirects=True)
        jw_html = jw_html.text.replace("""<script type="text/javascript" src="//clientvpn.cqwu.edu.cn/webvpn/bundle.debug.js" charset="utf-8"></script>""", "")
        return (
            parse_courses(jw_html)
            if use_model
            else jw_html.replace("<title></title>", '<meta charset="UTF-8">')
        )


def parse_courses(jw_html: str) -> List[AiCourse]:
    courses = []
    courses_keys = []
    soup = BeautifulSoup(jw_html, "lxml")
    trs = [i for i in soup.find_all("tr") if i.find("td", {"class": "td"})][:9]
    for tr in trs:
        tds = tr.find_all("td", {"class": "td"})
        for index, td in enumerate(tds):
            divs = td.find_all("div")
            for div in divs:
                class_property = str(div).split("<br/>")
                if len(class_property) != 4:
                    continue
                try:
                    weeks, start_num, sections = parse_weeks_and_sections(
                        BeautifulSoup(class_property[2], "lxml").text.strip()
                    )
                except Exception:
                    continue
                item = AiCourse(
                    name=BeautifulSoup(class_property[0], "lxml").text.strip(),
                    teacher=BeautifulSoup(class_property[1], "lxml").text.strip(),
                    position=BeautifulSoup(class_property[3], "lxml").text.strip(),
                    weeks=weeks,
                    day=index + 1,
                    start_num=start_num,
                    sections=sections,
                )
                if item.key not in courses_keys:
                    courses_keys.append(item.key)
                    courses.append(item)
    return courses


def parse_weeks_and_sections(text: str) -> Tuple[List[int], int, int]:
    # text: 17[1-4],1-18 单 [傍晚1]
    weeks_list, start_num, sections = [], 0, 0
    for week1 in text.split("[")[0].split(","):
        if "-" in week1:
            dan, shuang = "单" in week1, "双" in week1
            week1 = week1.replace("单", "").replace("双", "")
            for week in range(int(week1.split("-")[0]), int(week1.split("-")[1]) + 1):
                if dan:
                    if week % 2 != 0:
                        weeks_list.append(week)
                elif shuang:
                    if week % 2 == 0:
                        weeks_list.append(week)
                else:
                    weeks_list.append(week)
        else:
            weeks_list.append(int(week1))

    section_range = text.split("[")[1].replace("]", "")
    if section_range.startswith("傍晚"):
        start_num = 9
        sections = 1
    elif "-" in section_range:
        start_num = int(section_range.split("-")[0])
        end = int(section_range.split("-")[1])
        sections = end - start_num + 1
    else:
        start_num = int(section_range)
        sections = 1
    return weeks_list, start_num, sections
