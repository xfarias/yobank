from app.api.view import Register, Add, Transfer, Balance, TakeLoan, PayLoan
from flask_restful import Api
from app import app

api = Api(app)

api.add_resource(Register, '/api/register')
api.add_resource(Add, '/api/add')
api.add_resource(Transfer, '/api/transfer')
api.add_resource(Balance, '/api/balance')
api.add_resource(TakeLoan, '/api/takeloan')
api.add_resource(PayLoan, '/api/payloan')
