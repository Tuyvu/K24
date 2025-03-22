from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()

# # Database Config
# DATABASE_URL = "mysql+pymysql://root:example@user_db:3306/user_db"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # Model
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100))
#     email = Column(String(100), unique=True)

# Base.metadata.create_all(bind=engine)

# # Schema
# class UserSchema(BaseModel):
#     name: str
#     email: str

# API
@app.get("/")
def home_user():
 return {"message": "Đã truy cập thành công!"}
# @app.post("/users/")
# def create_user(user: UserSchema):
#     db = SessionLocal()
#     db_user = User(name=user.name, email=user.email)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     db.close()
#     return db_user

# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     db = SessionLocal()
#     user = db.query(User).filter(User.id == user_id).first()
#     db.close()
#     if user:
#         return user
#     return {"error": "User not found"}