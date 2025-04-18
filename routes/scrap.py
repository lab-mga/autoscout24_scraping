from flask import Blueprint, request, jsonify
from services.scrapper_bot import ScrapperBot
from schemas.scrapper_schema import ScrapperBotSchema  # Nuevo import
from pydantic import ValidationError  # Nuevo import

scrap_bp = Blueprint('scrap', __name__, url_prefix='/scrap')

@scrap_bp.route('', methods=['POST'])
def create_scrap():
    try:
        data = request.get_json()
        schema = ScrapperBotSchema(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    ScrapperBot.run(
        make=schema.make,
        model=schema.model,
        version=schema.version,
        year_from=schema.year_from,
        year_to=schema.year_to,
        power_from=schema.power_from,
        power_to=schema.power_to,
        powertype=schema.powertype,
        num_pages=schema.num_pages,
        zipr=schema.zipr
    )
    return "Scrapeado", 201

@scrap_bp.route('', methods=['DELETE'])
def delete_scrap():
    # Logic for handling DELETE request
    ##return jsonify({"Scrap borradod"}), 200
    return "Scrapeado borrado", 200