from flask import Flask
import random, logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/health')
def health():
    return {"status": "ok"}

@app.route('/process')
def process():
    if random.random() < 0.3:
        logging.error("Processing failure: simulated exception")
        return {"status": "error", "message": "processing failed"}, 500
    logging.info("Processing succeeded")
    return {"status": "processed"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)