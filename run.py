from app import app
from routes import routes   # Will say import is unused; is used at runtime

if __name__ == "__main__":
    app.run(debug=True)
