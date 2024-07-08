from routes import *
from ext  import app
import os

app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
if __name__ == '__main__':
    app.run(debug=True)
