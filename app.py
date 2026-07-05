from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "employee.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        department TEXT,
        salary INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return "Employee Management API is Running"

@app.route("/employees", methods=["GET"])
def get_employees():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()

    employees = []

    for row in rows:
        employees.append({
            "id": row[0],
            "name": row[1],
            "department": row[2],
            "salary": row[3]
        })

    conn.close()

    return jsonify(employees)

@app.route("/employees", methods=["POST"])
def add_employee():

    data = request.json

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO employees(name,department,salary) VALUES(?,?,?)",
        (data["name"], data["department"], data["salary"])
    )

    conn.commit()
    conn.close()

    return jsonify({"message":"Employee Added Successfully"})

@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM employees WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message":"Employee Deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)