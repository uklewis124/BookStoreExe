from flask import Flask, session, redirect, render_template, Blueprint
import pandas as pd
from dash import Dash, html
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import jinja2
from typing import Callable
from flask import current_app as server

def initiate():
    # do this for all blueprints
    server.register_blueprint(INSERT_BLUEPRINT_NAME_HERE)