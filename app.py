from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Temporary student data
students = []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add_student", methods=["POST"])
def add_student():

    name = request.form["name"]
    enrollment = request.form["enrollment"]
    semester = request.form["semester"]
    sgpa = float(request.form["sgpa"])

    # Get uploaded marksheet
    marksheet = request.files["marksheet"]

    filename = ""

    if marksheet and marksheet.filename != "":
        filename = marksheet.filename

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        marksheet.save(filepath)

    # Add student
    student = {
        "name": name,
        "enrollment": enrollment,
        "semester": semester,
        "sgpa": sgpa,
        "marksheet": filename
    }

    students.append(student)

    return redirect(url_for("leaderboard"))


@app.route("/leaderboard")
def leaderboard():

    # Sort by SGPA highest to lowest
    sorted_students = sorted(
        students,
        key=lambda x: x["sgpa"],
        reverse=True
    )

    # Add rank
    for index, student in enumerate(sorted_students):
        student["rank"] = index + 1

    return render_template(
        "leaderboard.html",
        students=sorted_students
    )


if __name__ == "__main__":
    app.run(debug=True)