from flask import Flask,render_template,request,redirect
import mysql.connector

app=Flask(__name__)

import os

db=mysql.connector.connect(
host=os.getenv("DB_HOST"),
user=os.getenv("DB_USER"),
password=os.getenv("DB_PASSWORD"),
database=os.getenv("DB_NAME")
)

cursor=db.cursor()


@app.route("/register")
def register():

    return render_template(
    "register.html"
    )


@app.route("/register_user",methods=["POST"])
def register_user():

    username=request.form["username"]

    email=request.form["email"]

    password=request.form["password"]

    role=request.form["role"]


    if role=="admin":

        approved="Pending"

    else:

        approved="Yes"


    try:

        cursor.execute("""

        INSERT INTO users
        (username,email,password,role,approved)

        VALUES

        (%s,%s,%s,%s,%s)

        """,

        (
        username,
        email,
        password,
        role,
        approved
        ))

        db.commit()

        return """

        <script>

        alert("Registration Success")

        window.location='/login'

        </script>

        """

    except Exception as e:

        print(e)

        return """

        <script>

        alert("User already exists")

        window.location='/register'

        </script>

        """


if __name__=="__main__":

    app.run(
    debug=True,
    port=5001
    )