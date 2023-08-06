from io import BytesIO

import openpyxl

import cqwu
from cqwu.errors import CookieError
from cqwu.types.cp import CP


class GetCP:
    async def get_cp(
        self: "cqwu.Client",
        year: int = None,
        semester: int = None,
    ) -> CP:
        """ 获取综合测评结果 """
        xue_nian = year or self.xue_nian
        xue_qi = semester or self.xue_qi
        await self.oauth_xg()
        url = "http://xg.cqwu.edu.cn/xsfw/sys/emapcomponent/imexport/export.do"
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
            'app': 'zhcptybbapp',
            'contextPath': 'http://xg.cqwu.edu.cn/xsfw',
            'module': 'modules',
            'page': 'cpjgcx',
            'action': 'cpjgcxbgdz',
            'containerId': 'cpjg_grid',
            'CPXN': str(xue_nian),
            'CPXQ': str(xue_qi),
            'filename': '综合测评结果',
            'colnames': 'XH,XM,CPXN,CPXQ,DWDM,DZ_ZYFX,BJDM,ZCJ,BJPM,BJRS,ZYNJPM,ZYNJRS,FS1,FS10,FS11,FS12,'
                        'XZNJ,DZ_BJPM,DZ_ZYPM',
        }
        html = await self.request.post(url, headers=headers, data=data)
        if html.status_code != 200:
            raise CookieError()
        html_data = html.json()
        url = f"http://xg.cqwu.edu.cn/xsfw/sys/emapcomponent/file/getAttachmentFile/{html_data['attachment']}.do"
        xlsx_file = await self.request.get(url, headers=headers)
        wb = openpyxl.load_workbook(filename=BytesIO(xlsx_file.content))
        ws = wb.active
        wz = ws[2]
        return CP(
            id=int(wz[0].value),
            name=wz[1].value,
            xue_nian=wz[2].value,
            xue_qi=wz[3].value,
            score=float(wz[7].value),
            class_rank=int(wz[8].value),
            class_member=int(wz[9].value),
            grade_rank=int(wz[10].value),
            grade_member=int(wz[11].value),
            dysz=float(wz[12].value),
            zysz=float(wz[13].value),
            cxsz=float(wz[14].value),
            wtsz=float(wz[15].value),
            zysz_class_rank=int(wz[17].value),
            zysz_grade_rank=int(wz[18].value),
        )
