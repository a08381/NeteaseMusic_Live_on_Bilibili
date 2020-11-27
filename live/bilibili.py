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
        return self.name


class Users:

    def __init__(self):
        self.users = {}

    def dumps(self) -> list:
        u = []
        for (k, v) in self.users:
            u.append(v.__dict__)
        return u
    
    @classmethod
    def loads(cls, ul: list):
        users = Users()
        for ud in ul:
            u = User(0)
            u.__dict__.update(ud)
            users[int(ud["uid"])] = u
        return users

    def load(self, ul: list):
        self.users.clear()
        for ud in ul:
            u = User(0)
            u.__dict__.update(ud)
            self.users[int(ud["uid"])] = u
        return self

    def __getitem__(self, key) -> User:
        if type(key) == int:
            item = self.users.get(key)
            if not item:
                item = User(key)
                self.users[key] = item
            return item

    def __setitem__(self, key, value) -> None:
        if type(key) == int and type(value) == User:
            self.users[key] = value

    def __iter__(self):
        return self.users


users = Users()
