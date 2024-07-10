from flask import render_template, redirect
from forms import RegisterUser, AddProduct, AddProductCategory, LoginUser, SliderForm
from extensions import app, db
from models import Product, ProductCategory, User
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/", methods=["POST", "GET"])
def home_page():
    form = SliderForm()
    promo = Product.query.filter_by(promo="promo").limit(2).all()
    slider_value = None
    if form.validate_on_submit():
        print(123)
        min_price = 0
        max_price = form.slider.data
        print(max_price)
        products = Product.query.filter(Product.price >= min_price, Product.price <= max_price).all()
    else:
        products = Product.query.all()
    return render_template('index.html', form=form, slider_value=slider_value, categories=ProductCategory.query.all(), products = products,
                           promos=promo)



@app.route("/login", methods=["POST", "GET"])
def log_in():
    form = LoginUser()
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        else:
            print(form.errors)
    return render_template("signin.html", form=form, categories=ProductCategory.query.all())


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterUser()
    if form.validate_on_submit():
        new_user = User(email=form.email.data,
                        password=form.password.data,
                        nickname=form.nickname.data,
                        birthday=form.birthday.data,
                        full_name=form.full_name.data,
                        role="user")

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect("/")
    else:
        print(form.errors)
    return render_template("signup.html", form=form, categories=ProductCategory.query.all())


@app.route("/logout", methods=["POST", "GET"])
def logout():
    logout_user()
    return redirect("/")


@app.route("/add_product", methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.role != "admin":
        return redirect("/")
    form = AddProduct()
    if form.validate_on_submit():
        new_product = Product(name=form.name.data,
                              image_url=form.image_url.data,
                              price=form.price.data,
                              text=form.text.data,
                              promo=form.promo.data,
                              category_id=form.category_id.data)
        db.session.add(new_product)
        db.session.commit()
        return redirect("/")
    return render_template("add_product.html", form=form, categories=ProductCategory.query.all())


@app.route("/add_category", methods=['GET', 'POST'])
@login_required
def add_category():
    form = AddProductCategory()
    if form.validate_on_submit():
        new_category = ProductCategory(name=form.category_name.data,
                                       id=form.id.data)
        db.session.add(new_category)
        db.session.commit()
        return redirect("/")
    else:
        print(form.errors)
    return render_template("add_category.html", form=form, categories=ProductCategory.query.all())


@app.route("/product/<int:id>")
def product(id):
    product = Product.query.get(id)
    return render_template("product.html", product=product, categories=ProductCategory.query.all())


@app.route("/promo", methods=['GET', 'POST'])
def promo():
    form = SliderForm()
    promo = Product.query.filter_by(promo="promo").all()
    slider_value = None
    if form.validate_on_submit():
        print(123)
        min_price = 0
        max_price = form.slider.data
        print(max_price)
        products = Product.query.filter(Product.price >= min_price, Product.price <= max_price).all()
    else:
        products = Product.query.all()
    return render_template("promo.html",form = form,  slider_value=slider_value, categories=ProductCategory.query.all(), products = products,
                           promos=promo)


@app.route("/products/<int:category_id>", methods=['GET', 'POST'])
@app.route("/products", methods=['GET', 'POST'])
def products(category_id):
    form = SliderForm()
    if form.validate_on_submit():
        min_price = 0
        max_price = form.slider.data
        products = Product.query.filter(
            Product.category_id == category_id,
            Product.price >= min_price,
            Product.price <= max_price
        ).all()
    else:
        products = Product.query.filter_by(category_id=category_id).all()
    return render_template("products.html", products=products, categories=ProductCategory.query.all(), form=form)


@app.route("/search/<string:name>")
def search(name):
    products = Product.query.filter(Product.name.ilike(f"%{name}%")).all()
    return render_template("products.html", products=products)

@app.route("/edit_product/<int:id>", methods=["POST", "GET"])
@login_required
def edit_product(id):
    product = Product.query.get(id)
    if not product:
        return render_template("404.html", id=id)

    form = AddProduct(name=product.name, text=product.text, price=product.price, image_url=product.image_url, promo=product.promo,
                           category_id=product.category_id)

    if form.validate_on_submit():
        product.promo = form.promo.data
        product.name = form.name.data
        product.text = form.text.data
        product.price = form.price.data
        product.image_url = form.image_url.data
        product.category_id = form.category_id.data

        db.session.commit()
        return redirect("/")
    else:
        print(form.errors)

    return render_template("edit_product.html", form=form, categories=ProductCategory.query.all())

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/delete_product/<int:id>", methods=["DELETE", "GET"])
@login_required
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return render_template("404.html", id=id)
    db.session.delete(product)
    db.session.commit()
    return redirect("/")