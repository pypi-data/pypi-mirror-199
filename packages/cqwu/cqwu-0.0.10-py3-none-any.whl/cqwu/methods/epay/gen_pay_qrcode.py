from io import BytesIO

import qrcode
from bs4 import BeautifulSoup

import cqwu
from cqwu.errors.auth import CookieError
from cqwu.errors.epay import EPayQrCodeError


class GenPayQrcode:
    async def gen_pay_qrcode(
        self: "cqwu.Client",
        show_qrcode: bool = True,
    ) -> None:
        """
        生成支付二维码
        """
        url = "http://218.194.176.214:8382/epay/thirdconsume/qrcode"
        html = await self.oauth(url)
        if not html:
            raise CookieError()
        if html.url != url:
            raise CookieError()
        soup = BeautifulSoup(html.text, "lxml")
        try:
            data = soup.find("input", attrs={"id": "myText"})["value"]
        except (ValueError, TypeError, KeyError, IndexError):
            return
        qr = qrcode.QRCode()
        qr.add_data(data)
        img = qrcode.make(data)
        if not show_qrcode:
            img_bytes = BytesIO()
            img.save(img_bytes)
            img_bytes.seek(0)
            raise EPayQrCodeError(img_bytes.getvalue())
        qr.print_ascii(invert=True)
        img.save("qrcode.png")
        print("生成支付码到 qrcode.png 成功，请打开该文件查看")
