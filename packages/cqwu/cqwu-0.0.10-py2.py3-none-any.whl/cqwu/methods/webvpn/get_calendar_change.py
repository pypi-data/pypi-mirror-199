import cqwu
from cqwu.errors import CookieError


def get_in_middle(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0]


class GetCalendarChange:
    async def get_calendar_change(
        self: "cqwu.Client",
        xue_nian: int = None,
        xue_qi: int = None,
    ) -> str:
        """ 获取课程表 """
        xue_nian = xue_nian or self.xue_nian
        xue_qi = xue_qi or self.xue_qi
        jw_html = await self.request.get(
            f"{self.web_ehall_path}/appShow?appId=5299144291521305", follow_redirects=True
        )
        if "教学管理服务平台" not in jw_html.text:
            raise CookieError
        jw_host = self.get_web_vpn_host(jw_html.url, https=True)
        jw_url = f"{jw_host}/cqwljw/student/jxap.jxaptzxx_rpt.jsp"
        jw_sg_url = f"{jw_host}/cqwljw/STU_DynamicInitDataAction.do"
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Origin': 'https://clientvpn.cqwu.edu.cn',
            'Referer': f'{jw_host}/cqwljw/student/jxap.jxaptzxx.html?menucode=S20302',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41',
            'content-type': 'application/x-www-form-urlencoded',
            'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        params = {
            "classPath": "C73E288D0DEA8D7F772BBD7F8FDC7E66F44C9E3992261989ECBAC5A3D722B306C6354658E0F25121E24CED075326C19885F263F369E5CD668E2EEE7CFB7EB5788F202FC6FD7DB0C96FB6995C1DD96ADE84BE3E72CFFBE9EC74FA044498BD2D21EA0439F9DC625F0EF61B7159924C542D577F814848F27128"
        }
        res = await self.request.post(jw_sg_url, params=params, headers=headers, timeout=60, follow_redirects=True)
        data = {
            'xh': get_in_middle(res.text, '<xh>', '</xh>'),
            'xn': str(xue_nian),
            'xq': str(xue_qi),
            'xnxq': f'{xue_nian},{xue_qi}',
            'menucode_current': 'S20302',
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://clientvpn.cqwu.edu.cn',
            'Referer': f'{jw_host}/cqwljw/student/jxap.jxaptzxx.html?menucode=S20302',
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
        jw_html = await self.request.post(jw_url, data=data, headers=headers, timeout=60, follow_redirects=True)
        jw_html = jw_html.text.replace("""<script type="text/javascript" src="//clientvpn.cqwu.edu.cn/webvpn/bundle.debug.js" charset="utf-8"></script>""", "")
        jw_html = jw_html.replace("""<script language='javascript' type='text/javascript' src='../js/Print.js'></script>""", "")
        return jw_html.replace("<title></title>", '<meta charset="UTF-8">')
