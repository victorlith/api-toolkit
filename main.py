from flask import Flask
from flask_cors import CORS
from views.exoplanet_view import exoplanet_bp
from views.user_view import user_bp

app = Flask(__name__)
CORS(app)


app.register_blueprint(exoplanet_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')


if __name__ == '__main__':
    from waitress import serve
    print('Servidor iniciado...')
    serve(app, host="0.0.0.0", port=80)
    #app.run(host='0.0.0.0', port=80, debug=True)