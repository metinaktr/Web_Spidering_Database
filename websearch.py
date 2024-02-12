import pyodbc 
from flask import Flask, render_template,request
import pickle
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from PIL import Image
from datetime import datetime
from pathlib import Path
import sys

app = Flask(__name__, template_folder="./static/")

@app.route('/')
def home():
    return render_template('websearch.html')  
 
@app.route("/websearch", methods=['GET','POST']) 
def websearch():
    #get query  from the request
   
    if request.method=='POST':
        query=request.form['query']

    if query=="":
        return render_template('websearch.html')  
  #connect to the Mssql database      
    conn_str = (
        r'DRIVER={SQL Server};'
        r'SERVER=(local)\SQLEXPRESS;'
        r'DATABASE=search_data;'
        r'Trusted_Connection=yes;'
        
    )
    conn = pyodbc.connect(conn_str)
    
    c=conn.cursor()
   #search for websites that match the query in their cleaned_content
    c.execute("select url, title from pages_cw where  CONVERT(varchar, cleaned_content) LIKE ? ORDER BY pagerank DESC",('%' + query +'%',))
    urls=c.fetchall()

    conn.close()



    return render_template('results.html', urls=urls, query=query)

if __name__=='__main__':
    app.run(debug=True)
    
  
    
    

