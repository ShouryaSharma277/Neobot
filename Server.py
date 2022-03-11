from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "<h2>Winter is alive idiots</h1>"

def run():
  app.run(host="0.0.0.0", port=8080)

def runServer():
  t = Thread(target=run)
  t.start()
