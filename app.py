from flask import Flask, render_template
from routes.item_routes import item_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Registro dos blueprints
    app.register_blueprint(item_bp)

    # Rota para a página principal
    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
