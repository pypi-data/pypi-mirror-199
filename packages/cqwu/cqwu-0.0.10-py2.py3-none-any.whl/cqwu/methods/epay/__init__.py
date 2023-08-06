from .gen_pay_qrcode import GenPayQrcode
from .get_balance import GetBalance
from .get_pay_bill import GetPayBill


class EPay(
    GenPayQrcode,
    GetBalance,
    GetPayBill,
):
    pass
