from app import app
from flask import jsonify, request
from services import team_service

@app.route('/', methods=["POST"])
@cross_origin(origin='*')
def Index():
    return jsonify(team_service.sort_teams(request)), 200
