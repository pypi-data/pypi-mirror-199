import time

import cqwu
from cqwu.errors.auth import NeedCaptchaError


class CheckCaptcha:
    async def check_captcha(
        self: "cqwu.Client",
        username: int = None,
        show_qrcode: bool = True,
    ):
        """ 检查是否需要验证码 """
        username = username or self.username
        params = {
            "username": username,
            "pwdEncrypt2": "pwdEncryptSalt",
            "_": str(round(time.time() * 1000))
        }
        url = f"{self.auth_host}/authserver/needCaptcha.html"
        captcha_html = await self.request.get(url, params=params, follow_redirects=False)
        if captcha_html.text == 'true':
            params = {
                "ts": str(round(time.time()))
            }
            captcha_url = f"{self.auth_host}/authserver/captcha.html"
            res = await self.request.get(captcha_url, params=params, follow_redirects=False)
            if not show_qrcode:
                raise NeedCaptchaError(res.content)
            with open("captcha.jpg", mode="wb") as f:
                f.write(res.content)
            print("验证码已保存在当前目录下的 captcha.jpg 文件中。")
            return self.get_input("验证码")
        return False
