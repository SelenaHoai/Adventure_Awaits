
from flask_app import app


# This needs to stay at the bottom
if __name__ == "__main__":
    app.run(debug=True, port=8000)
