from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os



app = Flask(__name__)
app.secret_key = 'secretkey'  # CHANGE in production

# Database (PostgreSQL via .env)
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



# Email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mssk6304445254@gmail.com'  # your email
app.config['MAIL_PASSWORD'] = 'fyya ojbg qppt kjps'        # app password

mail = Mail(app)
s = URLSafeTimedSerializer(app.secret_key)

# User Model
class User(db.Model):
    __tablename__ = 'users'  # <-- this fixes naming issue
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    verified = db.Column(db.Boolean, default=False)



# Routes
@app.route('/')
def index():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        if User.query.filter_by(username=username).first():
            return 'Username already exists.'
        if User.query.filter_by(email=email).first():
            return 'Email already exists.'

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        token = s.dumps(email, salt='email-confirm')
        link = url_for('confirm_email', token=token, _external=True)

        msg = Message('Confirm Your Email', sender='mssk6304445254@gmail.com', recipients=[email])
        msg.body = f'Click the link to verify your email: {link}'
        mail.send(msg)

        return 'A confirmation link has been sent to your email.'
    return render_template('register.html')

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except:
        return 'The confirmation link is invalid or has expired.'

    user = User.query.filter_by(email=email).first()
    if user:
        user.verified = True
        db.session.commit()
        return '✅ Your email has been verified. <a href="/login">Login</a>'
    return 'User not found.'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            if not user.verified:
                return '❌ Please verify your email before logging in.'
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        return '❌ Invalid credentials.'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

# 🆕 Forgot Password Flow
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = s.dumps(email, salt='reset-password')
            link = url_for('reset_password', token=token, _external=True)

            msg = Message('Password Reset Link', sender='mssk6304445254@gmail.com', recipients=[email])
            msg.body = f'Click here to reset your password: {link}'
            mail.send(msg)

            return 'Password reset link sent to your email.'
        return 'Email not found.'
    return render_template('forgot.html')

@app.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='reset-password', max_age=3600)
    except (SignatureExpired, BadSignature):
        return 'This password reset link is invalid or expired.'

    if request.method == 'POST':
        user = User.query.filter_by(email=email).first()
        if user:
            new_password = request.form['password']
            user.password = generate_password_hash(new_password)
            db.session.commit()
            return '✅ Your password has been updated. <a href="/login">Login</a>'
        return 'User not found.'
    return render_template('reset.html')

if __name__ == "__main__":
    
    with app.app_context():
        db.create_all()

    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)




