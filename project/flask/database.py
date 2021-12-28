from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from settings import db_name, db_pass, db_user, sql_instance_connection_name

driver_name = "mysql+pymysql"

engine = create_engine(
    driver_name
    + "://"
    + f"{db_user}:{db_pass}@/{db_name}"
    + f"?unix_socket=cloudsql/{sql_instance_connection_name}"
)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import schemas  # noqa

    Base.metadata.create_all(bind=engine)
