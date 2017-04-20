import os
from statuspage.app import app

HOST = '0.0.0.0'
PORT = os.environ.get('PORT', 5000)

def main():
    app.run(host=HOST, port=PORT)

if __name__ == '__main__':
    main()
