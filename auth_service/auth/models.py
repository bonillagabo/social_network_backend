from auth import db


class User(db.Model):
    __tablename__ = "users_user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def as_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }
