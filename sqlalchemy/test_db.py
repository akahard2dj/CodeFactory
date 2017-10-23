from crawler.database.database_engine import DatabaseEngine
from crawler.database.database_engine import Base
from crawler.database.test_table import User

sqlengine = DatabaseEngine(dbdialect='sqlite')
engine = sqlengine.get_engine()
session = sqlengine.get_session()
Base.metadata.create_all(engine)


user_model = User('user', 'name', '1234')
session.add(user_model)
session.commit()
