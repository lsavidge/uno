import os

from flask import Flask
from flask import g, render_template
from flask.ext.restful import Api, reqparse, Resource

from utils.sql import connect_db, query_db
from utils.words import load_words

# Flask configuration
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uno.db')
DEBUG = False

# Set up flask
app = Flask(__name__)
app.config.from_object(__name__)

# Set up flask-restful
api = Api(app)


# Set up database connection for each request
@app.before_request
def before_request():
    g.db = connect_db(app.config['DATABASE'])


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


# URL routing
# TODO: move these to static if no server-side templating added
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/journal', methods=['GET'])
def view_journal():
    return render_template('journal.html')


# Flask-restful classes
class Entries(Resource):
    """
    An entry point for journal entries
    """
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('max', type=int, help='Max number of entries to get')
        query_string = 'select * from entries order by datetime(added_on) desc'
        args = parser.parse_args(strict=True)
        if args['max']:
            query_string += ' limit %d' % args['max']
        entries = query_db(query_string)
        return entries

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('entry', type=str, required=True,
                            help='[required] One-word entry to add to this journal')
        args = parser.parse_args(strict=True)
        g.db.execute('insert into entries (word) values (:word)', {'word': args['entry']})
        g.db.commit()

api.add_resource(Entries, '/entries')


class Words(Resource):
    """
    An entry point for journal words available as entries
    """
    def get(self):
        # TODO: move to static if nothing added here
        words = load_words()
        return words

api.add_resource(Words, '/words')

if __name__ == '__main__':
    app.run()
