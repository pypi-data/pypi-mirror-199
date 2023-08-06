import re


class BCInfo(object):
    def __init__(
        self, pan: str = "", pan_sn: str = "", track2: str = "", ic55: str = ""
    ):
        super(BCInfo, self).__init__()
        self.pan = pan  # 主账号
        self.pan_sn = pan_sn  # 主账号序列号
        self.track2 = track2  # 二磁
        self.ic55 = ic55  # 55 域

    @property
    def pin_pan(self) -> str:
        r = re.sub(r"\D", "", self.pan)
        t = ""
        if len(r) <= 12:
            t = r
        else:
            t = r[-13:-1]

        return t.encode().rjust(16, b"\x00").hex()

    def __repr__(self) -> str:
        return "pan: %s, pan sn: %s, pin pan: %s, track2: %s, ic55: %s" % (
            self.pan,
            self.pan_sn,
            self.pin_pan,
            self.track2,
            self.ic55,
        )
