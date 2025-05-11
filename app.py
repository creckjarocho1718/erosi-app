from flask import Flask, send_from_directory, redirect

app = Flask(__name__, static_folder=None)

@app.route('/')
def root():
    return redirect('/login')

# LOGIN
@app.route('/login')
@app.route('/login/')
def login_index():
    return send_from_directory('login', 'index.html')

@app.route('/login/<path:filename>')
def login_files(filename):
    return send_from_directory('login', filename)

# TESTS 1–5
for i in range(1, 6):
    exec(f"""
@app.route('/test{i}')
@app.route('/test{i}/')
def test{i}_index():
    return send_from_directory('test{i}', 'index.html')

@app.route('/test{i}/<path:filename>')
def test{i}_files(filename):
    return send_from_directory('test{i}', filename)
""")

if __name__ == '__main__':
    app.run(debug=True)
