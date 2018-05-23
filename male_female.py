import sqlite3
import pandas as pd 
import numpy as np
from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template
from sqlalchemy import create_engine
engine = create_engine('sqlite:///adult.db', echo=False)
df=engine.execute("SELECT * FROM adult").fetchall()
df=pd.DataFrame(np.array(df))
df=df.drop([0], axis=1)
df= df.rename(index=str, columns={1:"age",2:"workclass",3:"fnlwgt",4:"education",5:"education-num",6:"marital-status",7:"occupation",8:"relationship",9:"race",10:"sex",11:"capital-gain",12:"capital-loss",13:"hours-per-week",14:"native-country",15:"class"})
print(df.head())
count=pd.crosstab(index=df["sex"], columns="count")
count.columns=["no"]
count.index=["Male", "Female"]
app = Flask(__name__)
@app.route("/")
def pie():
    labels = count.index 
    values = [count["no"][1], count["no"][0] ]
    colors = [ "#F7464A", "#46BFBD"  ]
    return render_template('pie.html', set=zip(values, labels, colors))

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)