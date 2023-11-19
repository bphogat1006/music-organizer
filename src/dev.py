from dotenv import load_dotenv
load_dotenv()

from server import app
app.run('0.0.0.0', 3000, debug=True)
# app.run('0.0.0.0', 3000)
