# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 17:03:05 2021

@author: AH05350
"""

#from flask import Flask, render_template, request
import pandas as pd
from apriori import apriori

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    if(request.method=='POST'):
        df = pd.read_csv(request.files.get('csvfile'), header=None, sep=',')
        records = []
        for i in range(len(df)):
            records.append([str(df.values[i,j]) for j in range(len(df.columns))])
        association_rules = apriori(records, min_support=float(request.form["min_support"]),\
                                    min_confidence=float(request.form["min_confidence"]), \
                                        min_lift=float(request.form["min_lift"]), min_length=int(request.form["min_length"]))
        association_results = list(association_rules)
        df_results = pd.DataFrame(columns = ['Rule', 'Support', 'Confidence', 'Lift'])
        for item in association_results:
            items = [x for x in item[0]]
            df_results.loc[len(df_results)] = [items, str(item[1]), str(item[2][0][2]), str(item[2][0][3])]
        return render_template('home.html',  tables=[df_results.to_html(classes = 'str')], titles=df_results.columns.values)
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=False)
