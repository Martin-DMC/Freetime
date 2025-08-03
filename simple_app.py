from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "¡Hola desde una app simple!"

if __name__ == '__main__':
    app.run(debug=True, port=5001) # Usa un puerto diferente para evitar conflictos