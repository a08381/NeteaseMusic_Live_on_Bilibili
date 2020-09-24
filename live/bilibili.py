from bilibili_api import user


class User:

    def __init__(self, uid: int):
        self.uid = uid

    def get_name(self) -> str:
        info = user.get_user_info(self.uid)
        return info["name"]

    def __eq__(self, value):
        if type(value) == User:
            return self.uid == value.uid
        elif type(value) == int:
            return self.uid == value

    def __str__(self):
        return self.get_name()
