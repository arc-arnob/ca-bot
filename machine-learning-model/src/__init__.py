from flask import Flask
import os
from dotenv import load_dotenv
import sys
from .config.dev_config import DevConfig

# loading environment variables
load_dotenv()

# declaring flask application
app = Flask(__name__)

# calling the dev configuration
config = DevConfig()

# making our application to use dev env
app.env = config.ENV