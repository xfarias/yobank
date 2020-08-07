from flask_restful import Resource
from flask import Blueprint, request, jsonify
from app.auth.models import User
from werkzeug.security import check_password_hash, generate_password_hash
from app.api.options import user_exists, verify_credentials, generate_status, update_account, update_debt
api = Blueprint('api', __name__, url_prefix='/api')


# Register username and pw to db
class Register(Resource):
    # Class Based API uses classes for defines an endpoint, which are served for especifics methods
    def post(self):
        # get data from json request
        data = request.get_json()

        # spliting the data from request
        username = data['username']
        password = data['password']  # clear data
        # checking if the collect data exists
        print(user_exists(username))
        if user_exists(username):
            error = {
                'status': 301,
                'msg': 'Invalid Credentials'
            }
            return jsonify(error)
        # user checked , time to hash the password
        hashpass = generate_password_hash(password, method='sha256')
        own = 0.0
        debt = 0.0
        # username and passw already done, is time do add to db
        user = User(username=username, password=hashpass, own=own, debt=debt)
        user.save()

        # data stored in db, confirmation return

        success = {
            'status': 200,
            'msg': "Success! You have Signup to yoBank!"
        }

        return jsonify(success)


class Add(Resource):
    # Add money to your account
    def post(self):
        data = request.get_json()

        username = data['username']
        password = data['password']
        money = data['amount']

        ret, error = verify_credentials(username, password)

        if error:
            return jsonify(ret)

        if money <= 0:
            return jsonify(generate_status(304, 'The money entered must be greater thar 0'))

        # users cash
        cash = User.objects(username=username).first()

        # add the remaining money to user
        update_account(username, cash['own'] + money)

        return jsonify(generate_status(200, "Amount added successfully to account"))


class Transfer(Resource):
    def post(self):
        # get data from user request
        data = request.get_json()

        # spliting the request data into variables
        username = data['username']
        password = data['password']
        to = data['to']
        money = data['amount']

        # verify the credentials
        ret, error = verify_credentials(username, password)

        if error:
            return jsonify(ret)

        # the user have money?
        cash = User.objects.get_or_404(username=username)
        # cash = User.find_one({"username": username})["own"]

        # is the cash a negative value?
        if cash.own <= 0:
            return jsonify(generate_status(303, "You are out of money, please Add Cash or take a loan"))
        # is the amount entered is negative?
        if money <= 0:
            return jsonify(generate_status(304, "The money amount entered must be greater than 0"))
        # the user that will recieve the money exists?
        if not user_exists(to):
            return jsonify(generate_status(301, "Recieved username is invalid"))

        # checking the balance of

        cash_to = User.objects.get_or_404(username=to)

        print(cash_to.own)
        # updating those accounts
        update_account(to, cash_to.own + money)
        update_account(username, cash.own - money)

        return jsonify(generate_status(200, "Amount added successfully to account"))


class Balance(Resource):
    def post(self):

        data = request.get_json()

        username = data['username']
        password = data['password']

        ret, error = verify_credentials(username, password)

        if error:
            return jsonify(ret)
        # get the balance - own,debt by username.

        balance = User.objects.get_or_404(username=username)
        '''
        MongoDB Raw Queryset
          balance = users.find({
            "username": username
        }, {
            "password": 0,
            "_id": 0
        })[0]
        '''
        b = {
            'username': balance.username,
            'own': balance.own,
            'debt': balance.debt
        }

        return jsonify(b)


class TakeLoan(Resource):
    def post(self):
        data = request.get_json()

        username = data["username"]
        password = data["password"]
        money = data["amount"]

        ret, error = verify_credentials(username, password)

        if error:
            return jsonify(ret)
        user = User.objects.get_or_404(username=username)

        cash = user.own
        debt = user.debt

        update_account(username, cash+money)
        update_debt(username, debt+money)

        return jsonify(generate_status(200, "Loan Added to Your Account "))


class PayLoan(Resource):
    def post(self):
        data = request.get_json()

        username = data["username"]
        password = data["password"]
        money = data["amount"]

        ret, error = verify_credentials(username, password)
        if error:
            return jsonify(ret)

        cash = User.objects.get_or_404(username=username)
        #cash = users.find_one({"username": username})["own"]

        if cash.own < money:
            return jsonify(generate_status(303, "Not Enough Cash in your account"))

        debt = cash.debt
        update_account(username, cash.own - money)
        update_debt(username, debt - money)

        return jsonify(generate_status(200, "Loan Paid"))

