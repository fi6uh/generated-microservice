from flask import Flask, render_template
import requests

app = Flask(__name__)

# Route that makes a request to the middleware and displays the response
@app.route('/')
def index():
    middleware_url = 'http://172.18.0.5:5150/api/data'
    
    try:
        response = requests.get(middleware_url)
        data = response.json()
        return render_template('index.html', data=data)
    except requests.RequestException as e:
        return f"Error connecting to middleware: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
