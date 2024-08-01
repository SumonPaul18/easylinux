from flask import Flask, render_template, request, flash, redirect, url_for
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')  # Replace with a strong secret key

from app import routes
