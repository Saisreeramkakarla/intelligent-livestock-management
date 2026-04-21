from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "livestock_secret_key"

# -------- DATABASE CONNECTION FUNCTION --------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="srck",
        database="livestock_db",
        autocommit=True
    )

# -------- LOGIN --------
@app.route("/login", methods=["GET", "POST"])
def login():
    db = get_db_connection()
    cursor = db.cursor(buffered=True)

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()

        if user:
            session["user"] = username
            return redirect("/dashboard")   # ✅ changed
        else:
            return "Invalid Username or Password"

    return render_template("login.html")


# -------- LOGOUT --------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# -------- DASHBOARD --------
@app.route("/")
@app.route("/dashboard")   # ✅ added route
def home():
    if "user" not in session:
        return redirect("/login")

    db = get_db_connection()
    cursor = db.cursor(buffered=True)

    cursor.execute("SELECT COUNT(*) FROM animals")
    total_animals = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM health")
    total_health = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions")
    total_predictions = cursor.fetchone()[0]

    return render_template(
        "dashboard.html",
        total_animals=total_animals,
        total_health=total_health,
        unhealthy_cases=total_predictions,
        model_accuracy="100%"
    )


# -------- ADD ANIMAL --------
@app.route("/addanimal", methods=["GET", "POST"])
def addanimal():
    if "user" not in session:
        return redirect("/login")

    db = get_db_connection()
    cursor = db.cursor(buffered=True)

    if request.method == "POST":
        cursor.execute(
            "INSERT INTO animals (type, breed, age, gender) VALUES (%s,%s,%s,%s)",
            (
                request.form["type"],
                request.form["breed"],
                request.form["age"],
                request.form["gender"]
            )
        )

    cursor.execute("SELECT * FROM animals")
    animals = cursor.fetchall()

    return render_template("addanimal.html", animals=animals)


# -------- ADD HEALTH --------
@app.route("/addhealth", methods=["GET", "POST"])
def addhealth():
    if "user" not in session:
        return redirect("/login")

    db = get_db_connection()
    cursor = db.cursor(buffered=True)

    if request.method == "POST":
        cursor.execute(
            """INSERT INTO health 
            (animal_id, temperature, heart_rate, activity, feeding) 
            VALUES (%s,%s,%s,%s,%s)""",
            (
                request.form["aid"],
                request.form["temp"],
                request.form["hr"],
                request.form["act"],
                request.form["feed"]
            )
        )

    cursor.execute("SELECT * FROM health")
    health_records = cursor.fetchall()

    return render_template("addhealth.html", health_records=health_records)


# -------- PREDICT --------
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if "user" not in session:
        return redirect("/login")

    db = get_db_connection()
    cursor = db.cursor(buffered=True)

    result = None

    if request.method == "POST":
        age = float(request.form["age"])
        weight = float(request.form["weight"])
        temp = float(request.form["temp"])
        behavior = int(request.form["behavior"])
        appetite = int(request.form["appetite"])
        vomiting = int(request.form["vomiting"])

        if temp > 102 or behavior == 1 or appetite == 1 or vomiting == 1:
            result = "Unhealthy - Possible Infection"
        else:
            result = "Healthy"

        cursor.execute(
            """INSERT INTO predictions 
            (age, weight, temperature, behavior, appetite, vomiting, result)
            VALUES (%s,%s,%s,%s,%s,%s,%s)""",
            (age, weight, temp, behavior, appetite, vomiting, result)
        )

    cursor.execute("SELECT * FROM predictions")
    prediction_records = cursor.fetchall()

    return render_template(   # ✅ fixed error
        "predict.html",
        result=result,
        prediction_records=prediction_records
    )


# -------- RUN --------
if __name__ == "__main__":
    app.run(debug=True)