from flask import Blueprint, request, jsonify
from services.scrapper_bot import ScrapperBot

scrap_bp = Blueprint('scrap', __name__, url_prefix='/scrap')

@scrap_bp.route('', methods=['POST'])
def create_scrap():
    # Inicializar con valores personalizados si lo deseas
    bot = ScrapperBot(make="seat", model="ibiza", year_from="2020", year_to="2024")
    bot.run()
    return "Scrapeado", 201

@scrap_bp.route('', methods=['DELETE'])
def delete_scrap():
    # Logic for handling DELETE request
    ##return jsonify({"Scrap borradod"}), 200
    return "Scrapeado borrado", 200