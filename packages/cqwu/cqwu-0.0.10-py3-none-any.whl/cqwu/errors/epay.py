from .base import CQWUEhallError


class EPayError(CQWUEhallError):
    pass


class EPayQrCodeError(EPayError):
    def __init__(self, qrcode: bytes):
        self.qrcode = qrcode
