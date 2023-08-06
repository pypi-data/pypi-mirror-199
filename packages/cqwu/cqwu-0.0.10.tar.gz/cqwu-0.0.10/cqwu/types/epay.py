from typing import List

from pydantic import BaseModel


class PayBill(BaseModel):
    id: str
    amount: float
    tradename: str
    shopname: str
    paytime: int
    status: int


class PayBillPage(BaseModel):
    pageno: int
    totalpage: int
    retcode: int
    retmsg: str
    dtls: List[PayBill]
