from typing import List

import cqwu
from cqwu.errors import CookieError
from cqwu.types.cp import CPGS, PublicCPRaw


class GetPublicCP:
    async def get_public_cp(
        self: "cqwu.Client",
        page_size: int = 999,
        page_number: int = 1,
        total: bool = True,
    ) -> List[PublicCPRaw]:
        """ 获取综合测评公示结果 """
        await self.oauth_xg()

        async def get_public_cp_raw(page_size_: int, page_number_: int) -> CPGS:
            url = "http://xg.cqwu.edu.cn/xsfw/sys/zhcptybbapp/modules/cpgs/cpgs_cpgsbg.do"
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,hu;q=0.5',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'http://xg.cqwu.edu.cn',
                'Referer': 'http://xg.cqwu.edu.cn/xsfw/sys/zhcptybbapp/*default/index.do',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51',
                'X-Requested-With': 'XMLHttpRequest',
            }
            data = {
                'querySetting': '[]',
                'pageSize': str(page_size_),
                'pageNumber': str(page_number_),
            }
            html = await self.request.post(url, headers=headers, data=data)
            if html.status_code != 200:
                raise CookieError()
            html_data = html.json()
            html_raw_data = html_data.get("datas", {}).get("cpgs_cpgsbg", {})
            return (
                CPGS(**html_raw_data)
                if html_raw_data
                else CPGS(
                    totalSize=0,
                    pageNumber=page_number_,
                    pageSize=page_size_,
                    rows=[],
                )
            )

        return_datas: List[PublicCPRaw] = []
        if total:
            page_size = 999
            page_number = 1
            while True:
                html_raw_datas = await get_public_cp_raw(page_size, page_number)
                if len(html_raw_datas.rows) == 0:
                    break
                return_datas.extend(html_raw_datas.rows)
                if html_raw_datas.totalSize == 0:
                    break
                elif html_raw_datas.pageNumber * html_raw_datas.pageSize >= html_raw_datas.totalSize:
                    break
                else:
                    page_number += 1
        else:
            html_raw_datas = await get_public_cp_raw(page_size, page_number)
            if len(html_raw_datas.rows) != 0:
                return_datas.extend(html_raw_datas.rows)
        return return_datas
