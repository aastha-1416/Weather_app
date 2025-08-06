from flask import Flask, render_template, request, redirect, session, jsonify
import pymysql
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Connect to MySQL
conn = pymysql.connect(host='localhost', user='root', password='Annielove_14app', db='weatherdb')
cursor = conn.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    
    if user:
        session['user'] = username
        return redirect('/dashboard')  # ✅ Redirect to dashboard on success
    else:
        return render_template('index.html', error='Invalid username or password')  # ❌ Stay on login page


@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html')
    return redirect('/')

@app.route('/weather')
def weather():
    try:
        api_key = 'your_actual_openweathermap_api_key'
        city = 'Canberra,au'
        # url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        url = f'https://api.openweathermap.org/data/2.5/weather?q=Canberra,au&appid={api_key}&units=metric'

        response = requests.get(url).json()
        data = {
            'temp': response['main']['temp'],
            'description': response['weather'][0]['description']
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch weather data'}), 500

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
