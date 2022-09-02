class Messageable:
    def send(self, content: str, *args, **kwargs):
        raise NotImplementedError


class User(Messageable):
    def get_dnd(self) -> bool:
        raise NotImplementedError

    def set_dnd(self, dnd: bool):
        raise NotImplementedError

    def get_language(self) -> str:
        raise NotImplementedError

    def set_language(self, language: str):
        raise NotImplementedError


class Backend:
    def run(self):
        raise NotImplementedError

    def get_user(self, id: int) -> User:
        raise NotImplementedError
