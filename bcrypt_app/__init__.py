from flask import Flask

app = Flask( __name__ )
app.secret_key = "shh this is a secret key"