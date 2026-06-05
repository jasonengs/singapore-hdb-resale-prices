import os

from dashboard.app import app

if __name__ == "__main__":
    # app = create_app()
    # app.run(debug=False)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
