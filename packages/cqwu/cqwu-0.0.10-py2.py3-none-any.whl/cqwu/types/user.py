class User:
    def __init__(
        self,
        username: int,
        password: str = None,
        name: str = None,
        sex: str = None,
        age: int = None,
        grade: int = None,
        institute: str = None,
        specialty: str = None,
        now_class: str = None,
        join_year: int = None,
        birthday: str = None,
        sfz: str = None,
        level: str = None,
        home: str = None,
    ):
        """
        一个用户

        :param username: 学号
        :param password: 密码
        :param name: 姓名
        :param sex: 性别
        :param age: 年龄
        :param grade: 年级
        :param institute: 学院
        :param specialty: 专业
        :param now_class: 班级
        :param join_year: 入学年份
        :param birthday: 出生日期
        :param sfz: 身份证号
        :param level: 培养层次
        :param home: 户籍地址
        """
        self.username = username
        self.password = password
        self.name = name
        self.sex = sex
        self.age = age
        self.grade = grade
        self.institute = institute
        self.specialty = specialty
        self.now_class = now_class
        self.join_year = join_year
        self.birthday = birthday
        self.sfz = sfz
        self.level = level
        self.home = home
