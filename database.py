from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Thông tin kết nối database
DATABASE_URL = "postgresql+psycopg2://postgres:123@postgres_db_container:5432/db_recipe"

# Tạo engine kết nối
engine = create_engine(DATABASE_URL)

# Tạo session để làm việc với database  
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Hàm tạo session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()