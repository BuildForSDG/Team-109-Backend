import os

from SDG_Backend.__init__ import create_app

#def run():
config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

    
if __name__ == '__main__':
    app.run(debug=True)