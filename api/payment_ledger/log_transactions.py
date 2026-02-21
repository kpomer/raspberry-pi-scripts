# api/payment_ledger/log_transactions.py
import sqlite3
import os
from flask import Blueprint, jsonify, request

# Flask Blueprint Setup
payment_ledger_bp = Blueprint('payment_ledger', __name__)

# Creates the DB file in the same folder as this script
DB_PATH = os.path.join(os.path.dirname(__file__), 'payment_ledger.db')