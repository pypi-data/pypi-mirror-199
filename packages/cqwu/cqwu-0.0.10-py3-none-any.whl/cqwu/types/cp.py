from typing import List

from pydantic import BaseModel


class CP(BaseModel):
    id: int
    name: str
    xue_nian: str
    xue_qi: str
    score: float
    class_rank: int
    class_member: int
    grade_rank: int
    grade_member: int
    dysz: float
    zysz: float
    cxsz: float
    wtsz: float
    zysz_class_rank: int
    zysz_grade_rank: int


class PublicCPRaw(BaseModel):
    XH: str
    XM: str
    DWDM_DISPLAY: str
    ZYDM_DISPLAY: str
    BJDM_DISPLAY: str
    ZCJ: float
    BJPM: int
    ZYNJPM: int
    FS1: float
    FS10: float
    FS11: float
    FS12: float
    DYYSCJ: str
    WTYSCJ: str
    CXYSCJ: str

    @property
    def id(self) -> int:
        """ 学号 """
        return int(self.XH)

    @property
    def name(self) -> str:
        """ 姓名 """
        return self.XM

    @property
    def yuan_xi(self) -> str:
        """ 院系 """
        return self.DWDM_DISPLAY

    @property
    def zhuan_ye(self) -> str:
        """ 专业 """
        return self.ZYDM_DISPLAY

    @property
    def class_name(self) -> str:
        """ 班级 """
        return self.BJDM_DISPLAY

    @property
    def total_score(self) -> float:
        """ 总成绩 """
        return float(self.ZCJ)

    @property
    def class_rank(self) -> int:
        """ 班级排名 """
        return int(self.BJPM)

    @property
    def grade_rank(self) -> int:
        """ 专业年级排名 """
        return int(self.ZYNJPM)

    @property
    def dysz(self) -> float:
        """ 德育素质分 """
        return float(self.FS1)

    @property
    def zysz(self) -> float:
        """ 智育素质测评 """
        return float(self.FS10)

    @property
    def cxsz(self) -> float:
        """ 创新素质测评 """
        return float(self.FS11)

    @property
    def wtsz(self) -> float:
        """ 文体素质 """
        return float(self.FS12)

    @property
    def dysz_raw(self) -> float:
        """ 德育原始成绩 """
        return float(self.DYYSCJ)

    @property
    def wtsz_raw(self) -> float:
        """ 文体原始成绩 """
        return float(self.WTYSCJ)

    @property
    def cxsz_raw(self) -> float:
        """ 创新原始成绩 """
        return float(self.CXYSCJ)


class CPGS(BaseModel):
    totalSize: int
    pageNumber: int
    pageSize: int
    rows: List[PublicCPRaw]
