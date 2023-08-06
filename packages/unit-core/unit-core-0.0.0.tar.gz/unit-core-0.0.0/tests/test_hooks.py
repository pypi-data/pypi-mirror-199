from main import BaseService


def test_start_hook():

    class UserService(BaseService):
        def get_user(self, user_id: int) -> str:
            return f"User {user_id}"

    service = UserService()

    assert service.get_user(1) == "User 1"
