from os import getenv
from dotenv import load_dotenv
from app import soketio, app

load_dotenv()

if __name__ == '__main__':
    soketio.run(app,
        host=getenv('host'),
        port=getenv('port'),
        debug=getenv('debug'),
        allow_unsafe_werkzeug=True
    )