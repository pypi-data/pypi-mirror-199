from .base import CQWUEhallError


class AuthError(CQWUEhallError):
    pass


class UsernameOrPasswordError(AuthError):
    """ 用户名或密码错误 """


class CookieError(AuthError):
    """ Cookie 失效 """


class NeedCaptchaError(AuthError):
    """ 需要验证码才能登录 """
    def __init__(self, captcha: bytes):
        self.captcha = captcha
