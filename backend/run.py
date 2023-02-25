from os import getenv
from dotenv import load_dotenv
from app import soketio, app

load_dotenv()

if __name__ == '__main__':
    soketio.run(app,
        host=getenv('host'),
        port=int(getenv('port')),
        debug=False,
        allow_unsafe_werkzeug=True
    )