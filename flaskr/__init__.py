import os
from . import db
from . import auth
from . import blog

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


	db.init_app(app)
	app.register_blueprint(auth.bp)
	app.register_blueprint(blog.bp)
	app.add_url_rule('/', endpoint='index')

	return app