from flask import Blueprint, request, Response
from flask_cors import CORS

from backend.service.domain.transactions import QueryTransactions, get_transactions_filtered

app_transaction = Blueprint('app_transaction', __name__, url_prefix="/transaction")
CORS(app_transaction)


@app_transaction.route("/filter", methods=['POST'])
def filter_transaction():
    body = request.json
    in_ = get_transactions_filtered(QueryTransactions(
        accounts=body['accounts'], positive=True, period=body['month']
    ))
    in_json = ",".join([x.to_json() for x in in_])

    out = get_transactions_filtered(QueryTransactions(
        accounts=body['accounts'], positive=False, period=body['month']
    ))
    out_json = ",".join([x.to_json() for x in out])

    res = '{"in": [' + in_json + '], "out": [' + out_json + ']}'
    return Response(
        response=res,
        mimetype="application/json",
        status=200,
    )