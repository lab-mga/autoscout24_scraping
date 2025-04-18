from flask import Blueprint, request, jsonify
from Analysis.oportunidades import OportunidadesAnalyzer  # Importa la clase
from models.resultado_oportunidades import AnalisisCocheModel  # Importa el modelo

analyze_bp = Blueprint('analyze', __name__, url_prefix='/analyze')

@analyze_bp.route('', methods=['POST'])
def analyze_post():
    # Borra todos los registros antes de analizar
    AnalisisCocheModel.eliminar_todos()
    # Ejecuta la lógica de analizar_oportunidades
    OportunidadesAnalyzer.analizar_oportunidades()
    resultados = AnalisisCocheModel.obtener_todos()
    return jsonify({
        "message": "POST recibido y análisis ejecutado",
        "resultados": resultados
    }), 201

@analyze_bp.route('', methods=['DELETE'])
def analyze_delete():
    return jsonify({"message": "DELETE recibido"}), 200





