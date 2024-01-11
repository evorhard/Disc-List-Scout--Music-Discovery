from flask import Flask

# Local imports
from config import APP_SECRET
from views import views_blueprint

app = Flask(__name__)
app.secret_key = APP_SECRET
app.register_blueprint(views_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
