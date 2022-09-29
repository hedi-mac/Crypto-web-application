from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from flask import Blueprint, request
from flask.json import jsonify
import validators
from src.database import Cryptocurrency, db
from flasgger import swag_from

cryptocurrencies = Blueprint("cryptocurrencies", __name__, url_prefix="/api/v1/cryptocurrencies")


@cryptocurrencies.route('/', methods=['POST', 'GET'])
def handle_cryptocurrencies():
    if request.method == 'POST':
        name = request.get_json().get('name', '')
        abbreviation = request.get_json().get('abbreviation', '')
        if Cryptocurrency.query.filter_by(name=name).first():
            return jsonify({
                'error': 'Name already exists'
            }), HTTP_409_CONFLICT
        if Cryptocurrency.query.filter_by(abbreviation=abbreviation).first():
            return jsonify({
                'error': 'Abbreviation already exists'
            }), HTTP_409_CONFLICT
        cryptocurrency = Cryptocurrency(name=name, abbreviation=abbreviation)
        db.session.add(cryptocurrency)
        db.session.commit()
        return jsonify({
            'id': cryptocurrency.id,
            'name': cryptocurrency.name,
            'abbreviation': cryptocurrency.abbreviation
        }), HTTP_201_CREATED
    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        cryptocurrencies = Cryptocurrency.query.paginate(page=page, per_page=per_page)
        data = []
        for cryptocurrency in cryptocurrencies.items:
            data.append({
                'id': cryptocurrency.id,
                'name': cryptocurrency.name,
                'abbreviation': cryptocurrency.abbreviation
            })
        meta = {
            "page": cryptocurrencies.page,
            'pages': cryptocurrencies.pages,
            'total_count': cryptocurrencies.total,
            'prev_page': cryptocurrencies.prev_num,
            'next_page': cryptocurrencies.next_num,
            'has_next': cryptocurrencies.has_next,
            'has_prev': cryptocurrencies.has_prev,

        }
        return jsonify({'data': data, "meta": meta}), HTTP_200_OK


