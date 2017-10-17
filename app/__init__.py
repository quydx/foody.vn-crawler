
#@
from flask import Flask 
fapp = Flask(__name__)
import config
fapp.config.from_object(config)
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(fapp)
from app import views

