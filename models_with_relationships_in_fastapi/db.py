from sqlmodel import create_engine,SQLModel,Session,select
sqlite_db_name = 'data.db'
sqlite_url = f"sqlite:///{sqlite_db_name}"
engine = create_engine(sqlite_url, echo=True,connect_args={"check_same_thread": False})

def create_db_and_tables(is_create=True,is_drop=False):
    if is_drop:
        SQLModel.metadata.drop_all(engine)
    if is_create:
        SQLModel.metadata.create_all(engine)
    assert engine is not None, "engine is None"
    with engine.begin() as conn:
        conn.exec_driver_sql("PRAGMA foreign_keys=ON")
        result = conn.exec_driver_sql("PRAGMA foreign_keys")
        if result and result.fetchone() == (1,):
            print("sqlite 外键已开启")
        else:
            print("sqlite 外键未开启")

def close_engine():
    if engine:
        engine.dispose()
def get_session():
    assert engine is not None, "engine is None"
    with Session(engine) as session:
        yield session

