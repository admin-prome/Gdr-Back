from source.jiraModule.utils.conexion import db
from flask import Blueprint, jsonify, request
from source.jiraModule.components.HigherAmount.model_postHigherAmount import QuotaAmountOneMillion


post_higherAmount_bp = Blueprint("HigherAmount", __name__)

@post_higherAmount_bp.route('/HigherAmount', methods=['POST'])
def post_higher_amount():
    try:
        data = request.get_json()

        new_quota_amount = QuotaAmountOneMillion(
            dni=data['dni'],
            opportunity=data['opportunity'],
            executive=data['executive'],
            quotaValue=data['quotaValue'],
            amount=data['amount'],
            notified=data.get('notified', False)  # Si 'notified' no está presente, establece el valor predeterminado en False
        )

        db.session.add(new_quota_amount)
        db.session.commit()

        return jsonify({'message': 'Datos insertados correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500