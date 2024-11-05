from flaskapp import db


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)  # integer primary key will be autoincremented by default
    login = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(255), nullable=False)
    def __repr__(self) -> str:
        return f"User(user_id {self.user_id!r}, name={self.name!r}, surname={self.surname!r})"

class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option4 = db.Column(db.String(255), nullable=False)
    option5 = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)

    def __repr__(self) -> str:
        return f"Question(id={self.id!r}, question={self.question!r})"

# В этом месте вы также можете добавить код для инициализации базы данных, если это необходимо.
