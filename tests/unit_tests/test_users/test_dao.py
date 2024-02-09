import pytest

from dao import UsersDAO

"""pytest --envfile .test.env tests/unit_tests/test_users/test_dao.py -s -v"""


@pytest.mark.parametrize(
    "email, is_exist",
    [
        ("test@test.com", True),
        ("artem@example.com", True),
        (".....", False),
    ],
)
async def test_find_user_by_id(email, is_exist):
    user = await UsersDAO.find_one_or_none(email=email)

    if is_exist:
        assert user
        assert user["email"] == email
    else:
        assert not user
