from sqlalchemy import create_engine
from flask import Flask, jsonify
from sqlFactory import SQLFactory

#################################################
# Database Setup
#################################################
sqlFactory = SQLFactory()


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/invoices"
        f"/api/v1.0/invoice_items"
        f"/api/v1.0/invoice_full/<INVOICE_ID>"
    )

#################################################
# Flask Routes FOR QUERIES
#################################################

@app.route("/api/v1.0/invoices")
def invoices():
    data = sqlFactory.getAllInvoices()
    return jsonify({"ok": True, "data": data})

@app.route("/api/v1.0/invoice_items")
def invoice_items():
    data = sqlFactory.getAllInvoiceItems()
    return jsonify({"ok": True, "data": data})

@app.route("/api/v1.0/invoice_full/<invoice_id>")
def invoice_full(invoice_id):
    data = sqlFactory.getInvoiceForInvoiceID(invoice_id)
    return jsonify({"ok": True, "data": data})

if __name__ == '__main__':
    app.run(debug=True)