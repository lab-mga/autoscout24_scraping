from flask import Blueprint, request, jsonify
from Analysis.oportunidades import OportunidadesAnalyzer  # Importa la clase
from models.resultado_oportunidades import AnalisisCocheModel  # Importa el modelo
##Imports para validar payload
from schemas import analyze_schema
from schemas.analyze_schema import AnalyzeSchema
from pydantic import ValidationError
##

analyze_bp = Blueprint('analyze', __name__, url_prefix='/analyze')

@analyze_bp.route('', methods=['POST'])
def analyze_post():

    #valida entrada
    try:
        data = request.get_json()
        schema = AnalyzeSchema(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    # Borra todos los registros antes de analizar
    if schema.delete_analysis: 
        AnalisisCocheModel.eliminar_todos()

    # Ejecuta la lógica de analizar_oportunidades
    OportunidadesAnalyzer.analizar_oportunidades(target_price=schema.target_price)

    #Respuesta
    resultados = AnalisisCocheModel.obtener_todos()
    return jsonify({
        "message": "POST recibido y análisis ejecutado",
        "resultados": resultados
    }), 201

@analyze_bp.route('', methods=['DELETE'])
def analyze_delete():
    return jsonify({"message": "DELETE recibido"}), 200





