# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response,jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()
    if earthquake:
        body = {'id': earthquake.id,
                'magnitude': earthquake.magnitude,
                'location': earthquake.location,
                'year': earthquake.year
        }
        status = 200
    else:
        body = {'message':  f'Earthquake {id} not found.'}
        status = 404
        
    return make_response(body, status)

# @app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
# def get_earthquakes_by_magnitude(magnitude):
#     matching_quakes = Earthquake.query.filter_by(magnitude>=magnitude).all()
#     response_data = {
#         "count": len(matching_quakes),
#         "quakes": [quake.to_dict() for quake in matching_quakes]  # Assuming to_dict() method is defined in your model
#     }
#     return make_response(jsonify(response_data), 200)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def matching_minimum_magnitude(magnitude):
    earthquakes = []
    for earthquake in Earthquake.query.filter(Earthquake.magnitude >= magnitude).all():
        earthquakes.append(earthquake.to_dict())
    body = {
        'count':len(earthquakes),
        'quakes': earthquakes
    }  
    status = 200 
    return make_response(body, status)     

if __name__ == '__main__':
    app.run(port=5555, debug=True)
