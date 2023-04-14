import os
from . import db
from . import auth

from flask import Flask

def create_app(test_config=None):
	# Cria e configura o aplicativo
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
			SECRET_KEY='dev',
			DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
		)

	if test_config is None:
		# carrega uma instancia da configuração, se ela existir, quando não estiver em teste
		app.config.from_pyfile('config.py', silent=True)
	else:
		# carrega a configuração de teste se ele for passada
		app.config.from_mapping(test_config)


	# assegura que arquivos existam
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass


	@app.route('/')
	def hello():
		return "Hello factore app"

	db.init_app(app)
	app.register_blueprint(auth.bp)

	return app