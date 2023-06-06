from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

#postgresql://myuser:1234@fastapi_postgres_1:5432/fastapi_database
SQLALCHEMY_DATABASE_URL = 'mariadb+pymysql://root:Snex2022@127.0.0.1:3306/bp_team' # URL db


engine = create_engine(SQLALCHEMY_DATABASE_URL)


Base = declarative_base()