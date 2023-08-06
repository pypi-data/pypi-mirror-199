import cqwu
from cqwu.errors.auth import CookieError
from cqwu.types.epay import PayBillPage


class GetPayBill:
    async def get_pay_bill(
        self: "cqwu.Client",
        page_number: int = 1,
    ) -> PayBillPage:
        """
        获取校园卡消费账单

        Returns:
            PayBillPage: 消费账单
        """
        url = "http://218.194.176.214:8382/epay/thirdapp/bill"
        html = await self.oauth(url)
        if not html:
            raise CookieError()
        if html.url != url:
            raise CookieError()
        data = await self.request.post(
            "http://218.194.176.214:8382/epay/thirdapp/loadbill.json",
            data={"pageno": page_number}
        )
        return PayBillPage(**data.json())
