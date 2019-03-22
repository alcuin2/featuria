from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from featuria import app, db, bcrypt
from featuria.forms import RegistrationForm, LoginForm, UpdateForm, AddClientForm, AddFeatureForm1, AddFeatureForm2, \
    AddProductAreaForm, PriorityRangeForm, EditClientForm, EditProductAreaForm, UpdateFeatureForm
from featuria.models import User, Client, Feature, ProductArea, PriorityRange


@app.route("/")
def home():

    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        features = Feature.query.order_by(Feature.date_added.desc()).paginate(page=page, per_page=5)
        if features.total == 0:
            flash("No Feature has been added, use the 'Add Feature' button", 'info')
        return render_template("home.html", datetime=datetime, features=features)
    else:
        return redirect(url_for("login"))


@app.route("/register", methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(fullname=form.fullname.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created successfully, log in!', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('home'))
        else:
            flash("Login unsuccessful, check email or password", "danger")
    return render_template("login.html", title="login", form=form)


@app.route("/logout")
def logout():

    logout_user()
    flash("You have logged out out, see you again", "success")
    return redirect(url_for("login"))


@app.route("/profile", methods=["POST", "GET"])
@login_required
def profile():

    form = UpdateForm()
    if form.validate_on_submit():
        current_user.fullname = form.fullname.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account updated", "success"),
        return redirect(url_for("profile"))
    if request.method == "GET":
        form.fullname.data = current_user.fullname
        form.email.data = current_user.email
    image_pic = url_for("static", filename=f"display_pics/{current_user.profile_pic}")
    return render_template("profile.html", image_pic=image_pic, form=form)


@app.route("/feature/new", methods=["GET", "POST"])
@login_required
def add_feature1():

    form = AddFeatureForm1()
    clients = Client.query.all()
    form.client.choices.append((0, "Select Client"))
    for client in clients:
        form.client.choices.append((client.id, client.name))
    if form.validate_on_submit():
        client_id = form.client.data
        return redirect(url_for('add_feature2', client_id=client_id))
    return render_template("add_feature1.html", form=form, legend="Add New Feature")


@app.route("/feature/new/<int:client_id>", methods=["GET", "POST"])
@login_required
def add_feature2(client_id):

    form = AddFeatureForm2()
    client = Client.query.get_or_404(client_id)
    product_areas = ProductArea.query.all()
    priority_range = PriorityRange.query.get(1)
    for index in range(priority_range.range):
        _feature = Feature.query.filter_by(client_id=client.id).filter_by(priority=index + 1).first()
        if _feature:
            pass
        else:
            form.priority.choices.append((index + 1, index + 1))
    for product_area in product_areas:
        form.product_area.choices.append((product_area.title, product_area.title))
    if form.validate_on_submit():
        feature = Feature(title=form.title.data, description=form.description.data, client_id=client.id,
                          priority=form.priority.data, target_date=form.target_date.data, added_by=current_user.id,
                          product_area=form.product_area.data, date_added=datetime.now())
        db.session.add(feature)
        db.session.commit()
        flash("New Feature Request added.", "success")
        return redirect(url_for("home"))
    return render_template("add_feature2.html", client=client, form=form,
                           legend=f"Add New Feature Request for '{client.name}'")


@app.route("/feature/edit/<int:client_id>/<int:feature_id>", methods=["GET", "POST"])
@login_required
def edit_feature(client_id, feature_id):

    form = UpdateFeatureForm()
    client = Client.query.get_or_404(client_id)
    feature = Feature.query.get_or_404(feature_id)
    product_areas = ProductArea.query.all()
    priority_range = PriorityRange.query.get(1)
    for index in range(priority_range.range):
        _feature = Feature.query.filter_by(client_id=client.id).filter_by(priority=index + 1).first()
        if _feature and _feature is not feature:
            pass
        else:
            form.priority.choices.append((index + 1, index + 1))
    for product_area in product_areas:
        form.product_area.choices.append((product_area.title, product_area.title))
    if form.validate_on_submit():
        print("I'm here")
        feature.title = form.title.data
        feature.description = form.description.data
        feature.priority = form.priority.data
        feature.product_area = form.product_area.data
        feature.target_date = form.target_date.data
        feature.status = form.status.data
        db.session.commit()
        flash("Feature update successful", "success")
        return redirect(url_for("home"))

    form.title.data = feature.title
    form.description.data = feature.description
    form.priority.data = feature.priority
    form.product_area.data = feature.product_area
    date = feature.target_date
    date_obj = datetime.strptime(date, "%Y-%M-%d")
    form.target_date.data = date_obj
    form.status.data = feature.status

    return render_template("edit_feature.html", form=form, date_obj=date_obj,
                           legend=f"Edit {client.name}'s Request", client=client, feature=feature)


@app.route("/feature/<int:feature_id>/delete", methods=["POST"])
@login_required
def delete_feature(feature_id):

    feature = Feature.query.get_or_404(feature_id)
    if feature.creator != current_user:
        abort(403)
    db.session.delete(feature)
    db.session.commit()
    flash(f"{feature.title} deleted successfully", "success")
    return redirect(url_for("home"))


@app.route("/clients", methods=["GET", "POST"])
@login_required
def clients():

    form = AddClientForm()
    if form.validate_on_submit():
        client = Client(name=form.name.data, added_by=current_user.id)
        db.session.add(client)
        db.session.commit()
        flash(f"{client.name} is added", "success")
        return redirect(url_for("clients"))
    clients = Client.query.order_by("id desc")
    clients_count = clients.count()
    return render_template("clients.html", form=form, legend="Clients", clients=clients, clients_count=clients_count)


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():

    priority_range = PriorityRange.query.get(1)
    if priority_range is None:
        priority_range = PriorityRange(range=10)
        db.session.add(priority_range)
        db.session.commit()
    priority_range_form = PriorityRangeForm()
    product_area_form = AddProductAreaForm()
    if product_area_form.validate_on_submit():
        product_area = ProductArea(title=product_area_form.title.data, added_by=current_user.id)
        db.session.add(product_area)
        db.session.commit()
        flash(f"{product_area.title} is added", "success")
        return redirect(url_for("settings"))
    elif request.method == "GET":
        priority_range_form.range.data = priority_range.range

    product_areas = ProductArea.query.order_by("id desc")
    return render_template("settings.html", priority_range_form=priority_range_form,
                           product_area_form=product_area_form, legend="Settings",
                           product_areas=product_areas)


@app.route("/priority-range/update", methods=["POST"])
@login_required
def update_priority_range():

    priority_range = PriorityRange.query.get(1)
    range = request.form['range']
    priority_range_form = PriorityRangeForm(range=range)
    if priority_range_form.validate():
        priority_range.range = priority_range_form.range.data
        db.session.commit()
        flash(f"Priority range updated", "success")
        return redirect(url_for("settings"))
    product_areas = ProductArea.query.order_by("id desc")
    product_area_form = AddProductAreaForm()
    return render_template("settings.html", priority_range_form=priority_range_form,
                           product_area_form=product_area_form, legend="Settings",
                           product_areas=product_areas)


@app.route("/client/<int:client_id>/delete", methods=["POST"])
@login_required
def delete_client(client_id):

    client = Client.query.get_or_404(client_id)
    if client.creator != current_user:
        abort(403)

    features = Feature.query.filter_by(client_id=client.id)
    for feature in features:
        db.session.delete(feature)
    db.session.delete(client)
    db.session.commit()
    flash(f"Client '{client.name}' and {features.count()} feature request(s) deleted successfully", "info")
    return redirect(url_for("clients"))


@app.route("/client/<int:client_id>/edit", methods=["Get", "POST"])
@login_required
def edit_client(client_id):

    client = Client.query.get_or_404(client_id)
    if client.creator != current_user:
        abort(403)
    form = EditClientForm()
    if form.validate_on_submit():
        client.name = form.name.data
        db.session.commit()
        flash(f"Client update successful", "success")
        return redirect(url_for("clients"))
    elif request.method == "GET":
        form.name.data = client.name
    return render_template("edit_client.html", form=form)


@app.route("/settings/product_area/<int:product_area_id>/delete", methods=["POST"])
@login_required
def delete_product_area(product_area_id):

    product_area = ProductArea.query.get_or_404(product_area_id)
    if product_area.creator != current_user:
        abort(403)
    db.session.delete(product_area)
    db.session.commit()
    flash(f"{product_area.title} deleted successfully", "success")
    return redirect("settings")


@app.route("/settings/product_area/<int:product_area_id>/edit", methods=["Get", "POST"])
@login_required
def edit_product_area(product_area_id):

    product_area = ProductArea.query.get_or_404(product_area_id)
    if product_area.creator != current_user:
        abort(403)
    form = EditProductAreaForm()
    if form.validate_on_submit():
        product_area.title = form.title.data
        db.session.commit()
        flash(f"Client update successful", "success")
        return redirect(url_for("settings"))
    elif request.method == "GET":
        form.title.data = product_area.title
    return render_template("edit_product_area.html", form=form)


@app.route("/search")
@login_required
def search():

    query = request.args.get('query')
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        features = Feature.query.filter(Feature.description.contains(query))\
            .order_by(Feature.date_added.desc()).paginate(page=page, per_page=5)
        if features.total > 0:
            flash(f"{features.total} results for '{query}'", 'info')
        else:
            flash(f"No search results for '{query}'", 'danger')
        return render_template("home.html", datetime=datetime, features=features)
    return redirect(url_for("login"))


@app.route("/client/<int:client_id>/features")
@login_required
def client_features(client_id):

    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        client = Client.query.get_or_404(client_id)
        features = Feature.query.filter_by(client_id=client.id)\
            .order_by(Feature.date_added.desc()).paginate(page=page, per_page=5)
        if features.total > 0:
            flash(f"{features.total} results for '{client.name}'", 'info')
        else:
            flash(f"No features for '{client.name}'", 'danger')
        return render_template("home.html", datetime=datetime, features=features)
    return redirect(url_for("login"))


@app.errorhandler(404)
def page_not_found(e):

    return render_template('404.html'), 404


@app.errorhandler(403)
def page_forbidden(e):

    return render_template('403.html'), 403


@app.errorhandler(500)
def page_not_found(e):

    return render_template('500.html'), 500






