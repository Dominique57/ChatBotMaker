from pymessenger.bot import Bot
from flask import Flask, request
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

from .app import ACCESS_TOKEN, VERIFY_TOKEN, app, bot
from .db_manager import Session, engine, Base
from .models import User, Server, Channel, Argument
from .flow import handles
from .routes import verify_fb_token


def run():
    app.run()
