from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db_config = {
    "host": "mysql",        # service name in docker network
    "user": "root",
    "password": "rootpass",
    "database": "namesdb"
}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        name = request.form.get("name")
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM people WHERE name = %s", (name,))
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()

            result = "Present" if count > 0 else "Absent"
        except Exception as e:
            result = f"Error: {e}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
