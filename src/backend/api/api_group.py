import json

from flask import Blueprint, request, Response
from flask_cors import CORS

import backend.service.group.group as service
from backend.schema.dto.group import GroupCategoryDTO

app_group = Blueprint('app_group', __name__, url_prefix="/group")
CORS(app_group)


@app_group.route("/monthly", methods=['POST'])
def group():
    body = request.json
    res = service.get_group_of_accounts(service.QueryGroupOfAccounts(accounts=body['accounts']))
    json_objects = [g.to_json() for g in res]
    return Response(
        response=f"[{','.join(json_objects)}]",
        mimetype="application/json",
        status=200,
    )


@app_group.route("/detail", methods=['POST'])
def details():
    body = request.json
    res = service.get_detail_of_group(service.QueryGroupDetails(accounts=body['accounts'], period=body['period']))
    return Response(
        response=res.to_json(),
        mimetype="application/json",
        status=200,
    )


@app_group.route("/category", methods=['POST'])
def category():
    body = request.json
    out: list[GroupCategoryDTO] = service.get_group_category(
        service.QueryGroupCategory(
            accounts=body['accounts'],
            month=body['month'].replace('/', '-'),
            expense=False,
            group_last=6
        )
    )
    out_json = ",".join([x.to_json() for x in out])

    in_: list[GroupCategoryDTO] = service.get_group_category(
        service.QueryGroupCategory(
            accounts=body['accounts'],
            month=body['month'].replace('/', '-'),
            expense=True,
            group_last=6
        )
    )
    in_json = ",".join([x.to_json() for x in in_])

    res = '{"in": [' + in_json + '], "out": [' + out_json + ']}'
    return Response(
        response=res,
        mimetype="application/json",
        status=200,
    )