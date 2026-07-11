from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "employee.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS employees(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def index():

    conn = get_connection()
    employees = conn.execute("SELECT * FROM employees").fetchall()
    conn.close()

    return render_template("index.html", employees=employees)


@app.route("/add", methods=["POST"])
def add_employee():

    name = request.form["name"]
    department = request.form["department"]
    salary = request.form["salary"]

    conn = get_connection()

    conn.execute(
        "INSERT INTO employees(name, department, salary) VALUES (?, ?, ?)",
        (name, department, salary)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/delete/<int:id>")
def delete_employee(id):

    conn = get_connection()

    conn.execute(
        "DELETE FROM employees WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_employee(id):

    conn = get_connection()

    if request.method == "POST":

        name = request.form["name"]
        department = request.form["department"]
        salary = request.form["salary"]

        conn.execute(
            """
            UPDATE employees
            SET name=?,
                department=?,
                salary=?
            WHERE id=?
            """,
            (name, department, salary, id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    employee = conn.execute(
        "SELECT * FROM employees WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        "edit_employee.html",
        employee=employee
    )


if __name__ == "__main__":
    app.run(debug=True)
