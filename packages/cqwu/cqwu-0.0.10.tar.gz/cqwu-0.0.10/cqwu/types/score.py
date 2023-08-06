from pydantic import BaseModel


class Score(BaseModel):
    """ 成绩类 """
    KCMC: str
    XF: float
    ZCJ: float
    JD: str
    XN: str
    XN_DISPLAY: str
    XQ: str
    XQ_DISPLAY: str

    @property
    def name(self) -> str:
        """ 课程名称 """
        return self.KCMC

    @property
    def credit(self) -> float:
        """ 学分 """
        return self.XF

    @property
    def score(self) -> float:
        """ 成绩 """
        return self.ZCJ

    @property
    def grade_point(self) -> float:
        """ 绩点 """
        return float(self.JD)

    @property
    def year(self) -> int:
        """ 学年 """
        return int(self.XN)

    @property
    def semester(self) -> int:
        """ 学期 """
        return int(self.XQ)
