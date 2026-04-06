import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base


def _get_test_database_url() -> str | None:
    return os.getenv("DATABASE_URL")


@pytest.fixture(scope="session")
def test_engine():
    database_url = _get_test_database_url()
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not set; integration tests require a real database. "
            "Set DATABASE_URL to a Postgres connection string."
        )

    engine = create_engine(database_url)

    import app.models.user  # noqa: F401

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(test_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
        session.close()
