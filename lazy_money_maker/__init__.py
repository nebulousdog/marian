'''
the Lazy Money Maker Flask application privides routing and RESTful API.
'''

import os

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    send_from_directory,
)

from lazy_money_maker.robinhood import (
    raw_collection,
    rh_dividends,
    rh_positions,
    rh_quote,
    rh_watchlist,
)

from lazy_money_maker.utils.templating import list_routes

def create_app(test_config=None):
    """create app"""

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'lazy_money_maker.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # jinja templates
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    @app.route('/')
    def index(): # pylint: disable=unused-variable
        return render_template('index.html', routes=list_routes(app))

    # NOTE: csv=false evaluates to truthy, only care about existence of `csv`
    #   param atm, but really should clear that up.
    #   expecting only `/positions?csv` or `/positions`.
    @app.route('/positions')
    def positions(): # pylint: disable=unused-variable
        csv = request.args.get('csv') is not None
        return rh_positions(csv)

    @app.route('/collection/<tag>')
    def collection(tag): # pylint: disable=unused-variable
        return raw_collection(tag)

    @app.route('/quote/<symbol>')
    def quote(symbol): # pylint: disable=unused-variable
        return rh_quote(symbol)

    @app.route('/watchlist')
    def watchlist(): # pylint: disable=unused-variable
        return rh_watchlist()

    @app.route('/dividends')
    def dividends(): # pylint: disable=unused-variable
        return rh_dividends()

    @app.route('/login')
    def login(): # pylint: disable=unused-variable
        return render_template('login.html')

    @app.route('/stylesheets/<path:path>')
    def send_stylesheet(path): # pylint: disable=unused-variable
        return send_from_directory('stylesheets', path)

    @app.route('/javascripts/<path:path>')
    def send_js(path): # pylint: disable=unused-variable
        return send_from_directory('javascripts', path)

    return app
