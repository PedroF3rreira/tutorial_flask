import sqlite3
import click # decorador para linha de comando

from flask import current_app, g # utilizado para disponibilidade global de objetos


def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
				current_app.config['DATABASE'],
				detect_types=sqlite3.PARSE_DECLTYPES
			)
		g.db.row_factory = sqlite3.Row

	return g.db


def close_db(e=None):
	db = g.pop('db', None)

	if db is not None:
		db.close()


def init_db():
	db = get_db()

	with current_app.open_resource('schema.sql') as f:
		db.executescript(f.read().decode('utf-8'))


@click.command('init-db')
def init_db_command():
	"""Limpando dados existentes e criando tabelas"""
	init_db()
	click.echo('Inicializando banco de dados')


def init_app(app):
	# quando aplicativo for desmontado
	app.teardown_appcontext(close_db)
	# adiciona script ao app cli
	app.cli.add_command(init_db_command)