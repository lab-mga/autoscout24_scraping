from flask import Blueprint, request, jsonify

scrap_bp = Blueprint('scrap', __name__, url_prefix='/scrap')

@scrap_bp.route('', methods=['POST'])
def create_scrap():
    # Logic for handling POST request
    ##eturn jsonify({"Scrap hecho"}), 201
    return "Scrapeado", 201

@scrap_bp.route('', methods=['DELETE'])
def delete_scrap():
    # Logic for handling DELETE request
    ##return jsonify({"Scrap borradod"}), 200
    return "Scrapeado borrado", 200