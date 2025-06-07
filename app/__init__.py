from flask import Flask
from .modules.marcas.marcas_routes import marca_bp
from .modules.proveedores.proveedores_routes import proveedor_bp
from .modules.categorias.categorias_routes import categoria_bp
from .modules.articulos.articulos_routes import articulo_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(marca_bp)
    app.register_blueprint(proveedor_bp)
    app.register_blueprint(articulo_bp)
    app.register_blueprint(categoria_bp)

    # Ruta de prueba
    @app.route('/')
    def home():
        return "<h1>segunda app en flask</h1>"

    return app