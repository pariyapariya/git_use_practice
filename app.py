# import necessary libraries
import pandas as pd

import pymysql
#from sqlalchemy import create_engine

from config import remote_db_endpoint, remote_db_port, remote_db_user, remote_db_pwd, remote_db_name

pymysql.install_as_MySQLdb()

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from sqlalchemy import func, create_engine

app = Flask(__name__)

engine = create_engine(f"mysql://{remote_db_user}:{remote_db_pwd}@{remote_db_endpoint}/{remote_db_name}")

# create route that renders index.html template
@app.route("/")
def home():    
    return render_template("index.html")

# Query the database and send the jsonified results
# @app.route("/send", methods=["GET", "POST"])
# def send():
#     conn = engine.connect()

#     if request.method == "POST":
#         name = request.form["petName"]
#         pet_type = request.form["petType"]
#         age = request.form["petAge"]

#         pets_df = pd.DataFrame({
#             'name': [name],
#             'type': [pet_type],
#             'age': [age]
#         })

#         pets_df.to_sql('pets', con=conn, if_exists='append', index=False)

#         return redirect("/", code=302)

#     conn.close()

    # return render_template("form.html")

@app.route("/api/sba_loan_detail")
def sba_startup():
    conn = engine.connect()
    
    query = '''
        SELECT 
            *
        FROM
            sba_loan_detail 
        Limit 10000    
    ''' 

    sba_df = pd.read_sql(query, con=conn)

    sba_json = sba_df.to_json(orient='records')

    conn.close()

    return sba_json

# @app.route("/api/pals")
# def pals():
#     conn = engine.connect()
    
#     query = '''
#         SELECT 
#             *
#         FROM
#             pets
#     ''' 

#     pets_df = pd.read_sql(query, con=conn)

#     pets_json = pets_df.to_json(orient='records')

#     conn.close()

#     return pets_json

if __name__ == "__main__":
    app.run(debug=True)