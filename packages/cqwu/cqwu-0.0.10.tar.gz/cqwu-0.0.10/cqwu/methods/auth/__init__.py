from .check_captcha import CheckCaptcha
from .export_cookie_to_file import ExportCookieToFile
from .login import Login
from .login_with_cookie import LoginWithCookie
from .login_with_cookie_file import LoginWithCookieFile
from .login_with_password import LoginWithPassword
from .oauth import Oauth


class Auth(
    CheckCaptcha,
    ExportCookieToFile,
    Login,
    LoginWithCookie,
    LoginWithCookieFile,
    LoginWithPassword,
    Oauth
):
    pass
