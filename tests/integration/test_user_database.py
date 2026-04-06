import pytest
from sqlalchemy.exc import IntegrityError

from app.models.user import User


def test_user_created_at_is_set(db_session):
    user = User.create(username="alice", email="alice@example.com", password="Password123")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    assert user.created_at is not None


def test_username_must_be_unique(db_session):
    db_session.add(User.create(username="alice", email="alice1@example.com", password="Password123"))
    db_session.commit()

    db_session.add(User.create(username="alice", email="alice2@example.com", password="Password123"))
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_email_must_be_unique(db_session):
    db_session.add(User.create(username="alice1", email="alice@example.com", password="Password123"))
    db_session.commit()

    db_session.add(User.create(username="alice2", email="alice@example.com", password="Password123"))
    with pytest.raises(IntegrityError):
        db_session.commit()
