import logging

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker

from domain.user import User
from output.database.database_base import Base, engine


class UserData(Base, User):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(50))

    def create_user(self):
        try:
            with sessionmaker(bind=engine)() as session:
                session.add(self)
                session.commit()
                logging.info("User added")
        except Exception as e:
            logging.error(e)

    @staticmethod
    def get_user_by_id(id_user):
        try:
            with sessionmaker(bind=engine)() as session:
                return session.query(UserData).filter(UserData.id == id_user).first()
        except Exception as e:
            logging.error(e)

    @staticmethod
    def get_user_by_name(name_user):
        try:
            with sessionmaker(bind=engine)() as session:
                return session.query(UserData).filter(UserData.username == name_user).first()
        except Exception as e:
            logging.error(e)

    @staticmethod
    def user_exists(username, password):
        try:
            with sessionmaker(bind=engine)() as session:
                return session.query(UserData).filter(UserData.username == username).filter(
                    UserData.password == password).first()
        except Exception as e:
            logging.error(e)


if __name__ == "__main__":
    user = UserData(username="admin", password="admin")
    # user.create_user()
    # print(user.get_user_by_name("bacari the boss"))

    if UserData.user_exists("admin", "admin"):
        print("yes")
    else:
        print("no")
