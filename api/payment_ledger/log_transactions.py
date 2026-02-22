# api/payment_ledger/log_transactions.py
import sqlite3
import os
import uuid
import json
from flask import Blueprint, jsonify, request

# Flask Blueprint Setup
payment_ledger_bp = Blueprint('payment_ledger', __name__)


def processPaymentLog(requestJson):
    # Creates the DB file in the same folder as this script
    DB_PATH = os.path.join(os.path.dirname(__file__), 'payment_ledger.db')

    # uniqueId = str(uuid.uuid4())

    # print(DB_PATH)
    # print(uniqueId)

    # TODO Insert into payment_ledger.db using Sqlite.  Make a single call to allow for "all or nothing" functionality when handling errors

    return 0 # Success!

@payment_ledger_bp.route('/')
def get_payment_ledger_api():
    # ----- Root function called from API ---#
    requestJson = request.get_json()
    #print(requestJson)
    
    status = processPaymentLog(requestJson)
    print(f"Status: {status}")


if __name__ == "__main__":
    # ----- LOCAL TESTING ---#
    SAMPLE_REQUEST = os.path.join(os.path.dirname(__file__), 'sample_payment_ledger_request.json')

    if not (os.path.exists(SAMPLE_REQUEST)):
        raise Exception(f"No sample file exists at path: {SAMPLE_REQUEST}")

    with open(SAMPLE_REQUEST) as sampleRequest:
        requestJson = json.load(sampleRequest)
    #print(requestJson)

    status = processPaymentLog(requestJson)
    print(f"Status: {status}")