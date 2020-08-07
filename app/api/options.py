
from app.auth.models import User
from werkzeug.security import check_password_hash


# Defines if user exists
def user_exists(username):
    existing_user = User.objects(username=username).first()
    if existing_user:
        return True
    else:
        return False


# auxiliar methods which will help us to handle with users requests
def verify_pw(username, password):
    # check if user exists
    if not user_exists(username):
        return False

    check_user = User.objects(username=username).first()
    if check_password_hash(check_user['password'], password):
        return True
    else:
        return False


# generic message to output status
def generate_status(status, msg):
    st = {
        'status': status,
        'msg': msg
    }
    return st


# check if the credentials presented are legitible
def verify_credentials(username, password):
    # the user exists?
    if not user_exists(username):
        return generate_status(301, "Invalid Username"), True

    # checking the valid of passw
    correct_pw = verify_pw(username, password)
    if not correct_pw:
        return generate_status(302, "Incorrect Password"), True

    return None, False


def update_account(username, balance):
    User.objects(username=username).update(set__own=balance)
    '''
    MongoDB Raw updating
    User.update_one({
        "username": username
    }, {
        "$set": {
            "own": balance
        }
    })
    '''


def update_debt(username, balance):
    User.objects(username=username).update(set__debt=balance)


def get_cash(username):
    '''
    MongoDB Raw get_cash
    cash = users.find_one({
        'username': username
    }, {
        '_id': 0
    })
    '''
    cash = User.objects.get_or_404(username=username)

    return cash.own