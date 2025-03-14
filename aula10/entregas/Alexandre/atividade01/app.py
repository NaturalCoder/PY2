from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def rota_p():
    return ""

@app.route('/hello/<user>')
def user(user=""):
    return render_template('index.html', nome=user)

if __name__ =='__main__':
    app.run(debug=True)