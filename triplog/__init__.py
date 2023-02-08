from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = '722d24131ebca2d827a6b6c6ee973b77'


from triplog import routes
