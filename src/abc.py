from typing import List, Optional


class Messageable:
    def send(self, content: str, *args, **kwargs):
        raise NotImplementedError


class User(Messageable):
    first_name: str
    last_name: Optional[str]

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    def get_dnd(self) -> bool:
        raise NotImplementedError

    def set_dnd(self, dnd: bool):
        raise NotImplementedError

    def get_language(self) -> str:
        raise NotImplementedError

    def set_language(self, language: str):
        raise NotImplementedError

    def get_holiday_mode(self) -> bool:
        raise NotImplementedError

    def set_holiday_mode(self, mode: bool) -> None:
        raise NotImplementedError

    def get_subscriptions(self) -> List[str]:
        raise NotImplementedError

    def set_subscriptions(self, departments: List[str]) -> None:
        raise NotImplementedError

    def add_subscription(self, department: str) -> bool:
        raise NotImplementedError

    def remove_subscription(self, department: str) -> bool:
        raise NotImplementedError


class Backend:
    def run(self):
        raise NotImplementedError

    def get_admin(self) -> User:
        raise NotImplementedError

    def get_user(self, id: int) -> User:
        raise NotImplementedError

    def get_me(self) -> User:
        """ Returns the bot user. """
        raise NotImplementedError
