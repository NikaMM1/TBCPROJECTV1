from ext import app 
from routes import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
if __name__ == '__main__':
    app.run(debug=True)
