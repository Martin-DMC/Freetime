from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    "sirve la pagina principal index.html"
    return render_template('index.html')

@main_bp.route('/login')
def login():
    """Sirve la página de inicio de sesión (login.html)."""
    return render_template('login.html')

@main_bp.route('/places')
def place_page():
    """Sirve la página de detalles del lugar (place.html)."""
    return render_template('place.html')

@main_bp.route('/profile')
def profile():
    """Sirve la página del perfil personal (profile.html)."""
    return render_template('profile.html')

@main_bp.route('/addPlace')
def addPlaces():
    """Sirve la página para añadir places (add.places.html)."""
    return render_template('add-places.html')
