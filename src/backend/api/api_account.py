from flask import Blueprint, request, Response
from flask_cors import CORS

from backend.service.domain.accocunt import get_account_list, QueryAccounts

app_account = Blueprint('app_account', __name__, url_prefix="/account")
CORS(app_account)


@app_account.route("/all", methods=['POST'])
def group():
    body = request.json
    order = body['orderBy']
    res = get_account_list(QueryAccounts(order_by=order))
    json_objects = [g.to_json() for g in res]
    return Response(
        response=f"[{','.join(json_objects)}]",
        mimetype="application/json",
        status=200,
    )



