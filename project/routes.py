from cffi.backend_ctypes import long
from flask import request, jsonify, url_for, render_template, flash, make_response

from . import app, db, bcrypt, models
from project.models import User, AdditionalInfo, Profession, Card
import jwt
import datetime
from project.tokens import login_token_required, generate_confirmation_token, confirm_token
from project.send_email import send_email
from .check_functions import check_username, check_email
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


@app.route('/is_current_user_exist', methods=['GET'])
@jwt_required()
def is_current_user_exist():
    gotten_token = get_jwt_identity()
    current_user = User.query.filter_by(id=gotten_token).first()
    if current_user:
        return jsonify({"id": current_user.id, "username": current_user.username, "email": current_user.email, "password": current_user.password,
                        "rating": current_user.rating, "isFreelancer": current_user.isExecutor, "confirmed": current_user.confirmed,
                        "additionalInfo": current_user.additionalInfo, "profession": current_user.profession})
    else:
        return jsonify({"id": None, "username": "", "email": "", "password": "", "rating": float(0), "isFreelancer": False,
                        "confirmed": False, "additionalInfo": AdditionalInfo(description="", city="", country="", typeOfWork=""),
                        "profession": Profession(description="", specialization="")})


@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form["email"]
    password = request.form["password"]
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        token_login = create_access_token(identity=user.id)
        return jsonify({"id": user.id, "username": user.username, "email": user.email, "password": user.password, "rating": float(0), "isFreelancer": False,
                    "token": token_login, "confirmed": user.confirmed, "additionalInfo": user.additionalInfo, "profession": user.profession})
    return jsonify({"error": "Login or password doesn't correct"})


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    db.create_all()
    user_id = request.form["user_id"]
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    crypt_pass = bcrypt.generate_password_hash(password).decode('utf-8')

    if check_username(username):
        return jsonify({"error": "This username already used"})

    if check_email(email):
        return jsonify({"error": "This email already used"})

    additional = AdditionalInfo(city="", country="", description="", typeOfWork="")
    profession = Profession(specialization="", description="", tags=[])
    user = User(id=user_id, username=username, email=email, password=crypt_pass, rating=float(0), isExecutor=False,
                       additionalInfo=additional, profession=profession)
    db.session.add(user)
    db.session.commit()

    token_login = create_access_token(identity=user.id)

    print(token_login)
    # confirm with email
    confirmation_token = generate_confirmation_token(user.email)
    confirm_url = url_for('confirm_email', token=confirmation_token, _external=True)
    html = render_template('confirm_email.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(user.email, subject, html)

    return jsonify({"id": user.id, "username": user.username, "email": user.email, "password": user.password, "rating": float(0), "isFreelancer": False,
                    "token": token_login, "confirmed": user.confirmed, "additionalInfo": user.additionalInfo, "profession": user.profession})


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return render_template('confirm_finish.html')


@app.route('/get_name/<user_id>')
def get_name(user_id):
    user = User.query.filter_by(id=user_id).first()
    try:
        return jsonify({"username": user.username, "rating": user.rating, "isFreelancer": user.isExecutor, "email": user.email})
    except AttributeError:
        return jsonify({"username": "", "rating": float(0), "isFreelancer": False, "email": ""})


@app.route('/get_profession/<user_id>')
def get_profession(user_id):
    user = User.query.filter_by(id=user_id).first()
    try:
        return jsonify(user.profession)
    except AttributeError:
        return jsonify(Profession(description="", specialization="", tags=[]))


@app.route('/get_additional_info/<user_id>')
def get_additional_info(user_id):
    user = User.query.filter_by(id=user_id).first()
    try:
        return jsonify(user.additionalInfo)
    except AttributeError:
        return jsonify(AdditionalInfo(description="", city="", country="", typeOfWork=""))


@app.route('/get_users_cards/<user_id>')
def get_users_cards(user_id):
    user = User.query.filter_by(id=user_id).first()
    try:
        return jsonify(user.cards)
    except AttributeError:
        return jsonify(Card())


@app.route('/add_new_card', methods=["GET", "POST"])
def add_new_card():
    user_id = request.form["id"]
    card_id = request.form["cardId"]
    title = request.form["title"]
    description = request.form["description"]
    date = request.form["date"]
    create_time = request.form.get("createTime", type=long)
    cost = request.form.get("cost", type=int)
    active = request.form.get("active", type=lambda v: v.lower() == 'true')
    agreement = request.form.get("agreement", type=lambda v: v.lower() == 'true')

    user = User.query.filter_by(id=user_id).first()
    user.cards.append(Card(id=card_id, title=title, description=description, date=date, createTime=create_time,
                           cost=cost, active=active, agreement=agreement))
    db.session.commit()
    return jsonify({"message": "success"})


@app.route('/change_card', methods=["GET", "POST"])
def change_card():
    user_id = request.form["id"]
    card_id = request.form["cardId"]
    title = request.form["title"]
    description = request.form["description"]
    date = request.form["date"]
    cost = request.form.get("cost", type=int)
    active = request.form.get("active", type=lambda v: v.lower() == 'true')
    agreement = request.form.get("agreement", type=lambda v: v.lower() == 'true')

    user = User.query.filter_by(id=user_id).first()
    for card in user.cards:
        if card.id == card_id:
            card.title = title
            card.description = description
            card.date = date
            card.cost = cost
            card.active = active
            card.agreement = agreement

    db.session.commit()
    return jsonify({"message": "success"})


@app.route('/get_all_cards', methods=["GET", "POST"])
def get_all_cards():
    users = User.query.all()
    users_cards = []
    for user in users:
        if user.isExecutor:
            users_cards.append(user.cards)
    return jsonify(users_cards)


@app.route('/set_name', methods=["GET", "POST"])
def set_name():
    user_id = request.form["id"]
    name = request.form["username"]

    user = User.query.filter_by(id=user_id).first()
    user.username = name
    db.session.commit()
    return jsonify({"message": "success"})


@app.route('/set_profession', methods=["GET", "POST"])
def set_profession():
    user_id = request.form["id"]
    description = request.form["description"]
    specialization = request.form["specialization"]
    tags = request.form.getlist("tags")

    user = User.query.filter_by(id=user_id).first()
    user.profession.description = description
    user.profession.specialization = specialization
    user.profession.tags = tags
    db.session.commit()
    return jsonify({"message": "success"})


@app.route('/set_additional_info', methods=["GET", "POST"])
def set_additional_info():
    user_id = request.form["id"]
    description = request.form["description"]
    country = request.form["country"]
    city = request.form["city"]
    type_of_work = request.form["typeOfWork"]

    user = User.query.filter_by(id=user_id).first()
    user.additionalInfo.description = description
    user.additionalInfo.country = country
    user.additionalInfo.city = city
    user.additionalInfo.typeOfWork = type_of_work
    db.session.commit()
    return jsonify({"message": "success"})


@app.route('/set_is_freelancer_state', methods=["GET", "POST"])
def set_is_freelancer_state():
    user_id = request.form["id"]
    state = request.form.get("isFreelancer", type=lambda v: v.lower() == 'true')
    user = User.query.filter_by(id=user_id).first()
    user.isExecutor = state
    db.session.commit()
    return jsonify({"message": "success"})


@app.route('/get_all_freelancers', methods=["GET"])
def get_all_freelancers():
    users = User.query.all()
    users_list = []
    for user in users:
        if user.isExecutor:
            users_list.append(user)
    return jsonify(users_list)


@app.route('/get_card_user/<user_id>', methods=["GET"])
def get_card_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return jsonify(user)

