from sqlalchemy import Column, Integer, String, Float
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy(app)
ma = Marshmallow(app)


# database models
class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Report(db.Model):
    __tablename__ = "report"
    report_id = Column(Integer, primary_key=True)
    report_name = Column(String)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "email", "password")


class ReportSchema(ma.Schema):
    class Meta:
        fields = (
            "report_id",
            "report_name",
        )


user_schema = UserSchema()
users_schema = UserSchema(many=True)

report_schema = ReportSchema()
reports_schema = ReportSchema(many=True)
