import webbrowser
import threading
import time
from app import app, fetch_prices

def run_flask():
    threading.Thread(target=fetch_prices, daemon=True).start()
    app.run(debug=False, port=5050, host="0.0.0.0")

threading.Thread(target=run_flask).start()

time.sleep(2)
webbrowser.open("http://127.0.0.1:5050")
