"""
this module is he to started to run the app



from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)"""

# run.py
# Importa directamente la instancia 'app' de tu __init__.py después de crearla
# NOTA: Esto asume que tu app/__init__.py ya tiene la estructura con create_app y registra los blueprints
from app import create_app

# Crea la instancia de la aplicación directamente aquí
# No la asignes a una variable 'app' global que pueda causar ambigüedades
_app_instance = create_app()

if __name__ == '__main__':
    # Ejecuta directamente la instancia creada
    _app_instance.run(host='0.0.0.0', port=5000, debug=True)