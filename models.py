from extensions import db, app, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    text = db.Column(db.String)
    promo = db.Column(db.String)
    image_url = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey("product_category.id"))
    category = db.relationship("ProductCategory", back_populates="products")

class ProductCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    products = db.relationship("Product", back_populates="category")

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    nickname = db.Column(db.String)
    full_name = db.Column(db.String)
    birthday = db.Column(db.Date)
    role = db.Column(db.String)

    def __init__(self, email, password, nickname, full_name, birthday, role="user"):
        self.email = email
        self.password = generate_password_hash(password)
        self.nickname = nickname
        self.full_name = full_name
        self.birthday = birthday
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Parse the birthday string to a datetime object
        birthday = datetime.strptime("01-02-2000", "%d-%m-%Y").date()
        admin = User(email="vaxo_niga@gmail.com",
                     password="vaxushti123",
                     nickname="vaxo16",
                     birthday=birthday,  # Use the parsed date object
                     full_name="vaxtangi",
                     role="admin")
        db.session.add(admin)
        db.session.commit()
    app.run(debug=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)