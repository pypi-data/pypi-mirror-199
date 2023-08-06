from .auth import Auth
from .epay import EPay
from .users import Users
from .webvpn import WebVPN
from .xg import XG


class Methods(
    Auth,
    EPay,
    Users,
    WebVPN,
    XG,
):
    pass
