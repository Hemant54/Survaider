import dash
import dash_core_components as dcc
import dash_html_components as html
import sqlite3
import pandas as pd 
import numpy as np
from sqlalchemy import create_engine
engine = create_engine('sqlite:///adult.db', echo=False)
df=engine.execute("SELECT * FROM adult").fetchall()
df=pd.DataFrame(np.array(df))
df=df.drop([0], axis=1)
df= df.rename(index=str, columns={1:"age",2:"workclass",3:"fnlwgt",4:"education",5:"education-num",6:"marital-status",7:"occupation",8:"relationship",9:"race",10:"sex",11:"capital-gain",12:"capital-loss",13:"hours-per-week",14:"native-country",15:"class"})
count=pd.crosstab(index=df["sex"], columns="count")
count.columns=["no"]
count.index=["Female", "Male"]
male_count=count["no"][1]
female_count=count["no"][0]
relation=pd.crosstab(index=df["relationship"], columns="count")
relation.columns=["no"]
relation.index=["Husband", "Not-in-family", "Other-relative", "Own-child", "Unmarried", "Wife"]
husband=relation["no"][0]
not_in_family=relation["no"][1]
other_relative=relation["no"][2]
own_child=relation["no"][3]
unmarried=relation["no"][4]
wife=relation["no"][5]
app = dash.Dash()
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
		
               
            
    )
df=df.filter(items=['sex', 'race', 'relationship' ])


app.layout = html.Div(children=[
    html.H1(children='Hello Surevaider'),

    html.Div(children='''
        Bar Graphs web app using Dash Framework and Python 
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': ['male'], 'y': [male_count], 'type': 'bar', 'name': 'Male'},
				{'x': ['female'], 'y': [female_count], 'type': 'bar', 'name': u'Female'},
                
            ],
            'layout': {
                'title': 'Male and Female Graph'
            }
        }
    ),
	dcc.Graph(
        id='example-graph1',
        figure={
            'data': [
                {'x': ['Husband'], 'y': [husband], 'type': 'bar', 'name': 'Husband'},
				{'x': ['Not-in-family'], 'y': [not_in_family], 'type': 'bar', 'name': 'Not-in-family'},
				{'x': ['Other-relative'], 'y': [other_relative], 'type': 'bar', 'name': 'Other-relative'},
				{'x': ['Own-child'], 'y': [own_child], 'type': 'bar', 'name': 'Own-child'},
				{'x': ['Unmarried'], 'y': [unmarried], 'type': 'bar', 'name': 'Unmarried'},
				{'x': ['Wife'], 'y': [wife], 'type': 'bar', 'name': 'Wife'},
                
            ],
            'layout': {
                'title': 'Relationship Graph'
            }
        }
    ),
	
	generate_table(df)
			

])



if __name__ == '__main__':
    app.run_server(debug=True)