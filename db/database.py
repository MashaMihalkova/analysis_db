from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://osm:geoserver@10.0.1.64:5432/db_etl_pm_pmc"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:34uzisup@localhost:5432/db_test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
