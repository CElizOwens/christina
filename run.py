from app import app
from views import views   # Will say import is unused; is used at runtime

if __name__ == "__main__":
    app.run(debug=True)
