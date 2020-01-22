from app import app, db
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegistrationForm, AddingClients
from flask_login import current_user, login_user, logout_user
from app.models import User, Client
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
import datetime



@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == "POST":
        data = request.get_json()

        user_to_change = current_user.clients.filter_by(id=int(data['user_id'])).first()
        user_to_change.invoice_status = 'Generated'
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('index.html', title='Homepage')


@login_required
@app.route('/gen-invoice', methods=['POST', 'GET'])
def invoice():
    global client_invoice
    if request.method == "POST":
        data = request.get_json()

        client_invoice = current_user.clients.filter_by(id=int(data['user_id'])).first()

    today = datetime.date.today()
    due_date = today + datetime.timedelta(days=14)
    return render_template('generated_invoice.html', title='Invoice', client_invoice=client_invoice,
                           today=today, due_date=due_date)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    form_registration = RegistrationForm()
    if form_registration.validate_on_submit():
        new_user = User(company_name=form_registration.company_name.data, email=form_registration.email.data)
        new_user.set_password(form_registration.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form, form_registration=form_registration)


@app.route('/user/<id>/<company_name>')
@login_required
def user(id, company_name):
    user = User.query.filter_by(id=id).first_or_404()

    return render_template('user.html', user=user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/add_client', methods=['GET', 'POST'])
@login_required
def add_client():
    form = AddingClients()
    if form.validate_on_submit():
        client = Client(client_name=form.name.data, client_company=form.company.data, client_email=form.email.data,
                        invoice_amount=form.invoice.data, service_description=form.service_desc.data,
                        user_id=current_user.id)

        db.session.add(client)
        db.session.commit()
        flash('Awesome, we will send the bill to that bitch soon!')
        return redirect(url_for('index'))
    return render_template('addClient.html', title='Add Client', form=form)
