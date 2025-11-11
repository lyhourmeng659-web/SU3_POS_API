from flask import request
from sqlalchemy import text
from app import app, db


# daily
@app.get("/report/sales/daily")
def report_daily():
    sql = text("""
        SELECT DATE(i.created_at) as date, SUM(d.total) as total_sales
        FROM invoice_details d
        JOIN invoices i ON d.invoice_id = i.id
        GROUP BY DATE(i.created_at)
        ORDER BY DATE(i.created_at) DESC
    """)
    result = db.session.execute(sql).fetchall()
    return [dict(row._mapping) for row in result], 200


# weekly
@app.get("/report/sales/weekly")
def report_weekly():
    sql = text("""
        SELECT strftime('%Y-%W', i.created_at)
        as week, SUM(d.total) as total_sales
        FROM invoice_details d
        JOIN invoices i ON d.invoice_id = i.id
        GROUP BY strftime('%Y-%W', i.created_at)
        ORDER BY week DESC
    """)
    result = db.session.execute(sql).fetchall()
    return [dict(row._mapping) for row in result], 200


# monthly
@app.get("/report/sales/monthly")
def report_monthly():
    sql = text("""
        SELECT strftime('%Y-%m', i.created_at) as month, SUM(d.total) as total_sales
        FROM invoice_details d
        JOIN invoices i ON d.invoice_id = i.id
        GROUP BY month
        ORDER BY month DESC
    """)
    result = db.session.execute(sql).fetchall()
    return [dict(row._mapping) for row in result], 200


# sale by criteria
@app.get("/report/sales/by")
def report_by():
    # Get query parameter safely and normalize it
    sale_by = request.args.get("type", "").strip().lower()

    # Validate
    if not sale_by:
        return {"error": "Missing 'type' parameter. Use ?type=product or ?type=category"}, 400

    # Query by Product
    if sale_by == "product":
        sql = text("""
            SELECT 
                p.name AS product_name, 
                SUM(d.qty) AS total_qty, 
                SUM(d.total) AS total_sales
            FROM invoice_details d
            JOIN products p ON d.product_id = p.id
            GROUP BY p.id
            ORDER BY total_sales DESC
        """)

    # Query by Category
    elif sale_by == "category":
        sql = text("""
            SELECT 
                c.name AS category_name, 
                SUM(d.qty) AS total_qty, 
                SUM(d.total) AS total_sales
            FROM invoice_details d
            JOIN products p ON d.product_id = p.id
            JOIN categories c ON p.category_id = c.id
            GROUP BY c.id
            ORDER BY total_sales DESC
        """)

    # Unsupported type
    else:
        return {"error": f"Unsupported type '{sale_by}'. Allowed: product, category"}, 400

    # Execute and return result
    result = db.session.execute(sql).fetchall()
    data = [dict(row._mapping) for row in result]
    return {"type": sale_by, "count": len(data), "data": data}, 200
