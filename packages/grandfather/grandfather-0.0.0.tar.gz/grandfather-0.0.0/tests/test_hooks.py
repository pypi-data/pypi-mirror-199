import inspect

from main import UnitCore, Hook, trace


def test_start_hook():

    state = []

    class TraceHook(Hook):
        def __call__(self, *args, **kwargs):
            state.append((self.wrapped_func.__name__, args, kwargs))
            return self.wrapped_func(*args, **kwargs)

    @trace(TraceHook)
    class UserService:
        def get_user(self, user_id: int) -> str:
            return f"User {user_id}"

    service = UserService()

    assert service.get_user(1) == "User 1"

    assert state == ["pre_hook_called", "post_hook_called"]
