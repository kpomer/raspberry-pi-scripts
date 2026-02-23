# api/payment_ledger/log_transactions.py
import sqlite3
import os
import uuid
import json
import datetime
from flask import Blueprint, jsonify, request

# Flask Blueprint Setup
payment_ledger_bp = Blueprint('payment_ledger', __name__)

def processPaymentLog(requestJson):
    # Structure data for INSERT statement)
    try:
        dataToInsert = [
            (
                str(uuid.uuid4()), 
                item['user'], 
                item['merchant'], 
                item['paymentMethod'], 
                item['transactionAmount'], 
                item['lat'], 
                item['long'], 
                item['transactionDateTime'], 
                datetime.datetime.now().astimezone().isoformat(timespec='seconds')
            ) 
            for item in requestJson
        ]
    except (KeyError, TypeError) as e:
        return {"success": False, "data": None, "error": f"Invalid data format: Missing key {e}"}
    except Exception as e:
        return {"success": False, "data": None, "error": "Internal processing error"}
    

    DB_PATH = os.path.join(os.path.dirname(__file__), 'payment_ledger.db')
    initialize_db(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.executemany(
            """INSERT INTO transactionLog
                (id, user, merchant, paymentMethod, transactionAmount, latitude, longitude, transactionDateTime, syncDateTime) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
            dataToInsert
        )
        
        conn.commit()
        return {"success": True, "data": {"count": len(dataToInsert)}, "error": None}
        
    except sqlite3.Error as e:
        conn.rollback()
        return {"success": False, "data": None, "error": f"Database Error: {str(e)}"}
    finally:
        conn.close()


def initialize_db(db_path):

    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactionLog (
                id TEXT PRIMARY KEY,
                user TEXT NOT NULL,
                merchant TEXT NOT NULL,
                paymentMethod TEXT NOT NULL,
                transactionAmount TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                transactionDateTime TEXT NOT NULL,
                syncDateTime TEXT NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()

@payment_ledger_bp.route('/', methods=['POST'])
def get_payment_ledger_api():
    # ----- Root function called from API ---#
    try:
        requestJson = request.get_json()
        result = processPaymentLog(requestJson)
        status_code = 201 if result['success'] else 500
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"success": False, "data": None, "error": f"Internal Error: {str(e)}"}), 500


if __name__ == "__main__":
    # ----- LOCAL TESTING ---#
    SAMPLE_REQUEST = os.path.join(os.path.dirname(__file__), 'sample_payment_ledger_request.json')

    if not (os.path.exists(SAMPLE_REQUEST)):
        raise Exception(f"No sample file exists at path: {SAMPLE_REQUEST}")

    with open(SAMPLE_REQUEST) as sampleRequest:
        requestJson = json.load(sampleRequest)

    result = processPaymentLog(requestJson)
    status_code = 201 if result['success'] else 500
    print(f"status_code: {status_code}")
    print(result)
