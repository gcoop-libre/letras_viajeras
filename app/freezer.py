from flask_frozen import Freezer
from app import app

FREEZER_DEFAULT_MIMETYPE='text/html'

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
