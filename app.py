"""Flask app for Cupcakes"""
from flask import Flask, request, render_template,  redirect, flash, session, url_for, jsonify, abort
from models import db, connect_db, Cupcake


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "123"

connect_db(app)

@app.route('/')
def index():
    """Render the homepage"""

    return render_template('index.html')

@app.route('/api/cupcakes')
def get_cupcakes():
    """Get data about all cupcakes"""

    cupcakes = Cupcake.query.all()
    cupcakes_list = []
    for cupcake in cupcakes:
        cupcakes_list.append({'id': cupcake.id,
                              'flavor': cupcake.flavor,
                              'size': cupcake.size,
                              'rating': cupcake.rating,
                              'image': cupcake.image})
    return jsonify(cupcakes=cupcakes_list)


@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """Get data about a single cupcake"""

    cupcake = Cupcake.query.get(cupcake_id)

    if not cupcake:
        abort(404)

    return jsonify(cupcake={'id': cupcake.id,
                            'flavor': cupcake.flavor,
                            'size': cupcake.size,
                            'rating': cupcake.rating,
                            'image': cupcake.image})


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a cupcake"""

    data = request.get_json()

    flavor = data.get('flavor')
    size = data.get('size')
    rating = data.get('rating')
    image = data.get('image', 'https://tinyurl.com/demo-cupcake')

    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake={'id': cupcake.id,
                            'flavor': cupcake.flavor,
                            'size': cupcake.size,
                            'rating': cupcake.rating,
                            'image': cupcake.image})

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update cupcake with given id and return updated cupcake as JSON."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    data = request.json

    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.image = data.get('image', cupcake.image)

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete cupcake with given id and return JSON confirming deletion."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message='Deleted')
