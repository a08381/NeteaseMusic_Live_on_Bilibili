from bilibili_api import user


class User:

    def __init__(self, uid: int):
        self.uid = uid
        self.reward = 0

    @property
    def name(self) -> str:
        info = user.get_user_info(self.uid)
        return info["name"]

    def __eq__(self, value):
        if type(value) == User:
            return self.uid == value.uid
        elif type(value) == int:
            return self.uid == value

    def __iadd__(self, value):
        self.reward += value

    def __isub__(self, value):
        self.reward -= value

    def __str__(self):
        return self.get_name()
