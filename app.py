# Name : Surya Narayanan Nadhamuni Suresh
# UTA ID : 1001877873
from flask import Flask,render_template, request,url_for,flash
import mysql.connector as mysql
from geopy.geocoders import Nominatim as nm
from geopy.point import Point
from math import radians, sin, cos,sqrt,atan2
from decimal import Decimal
import time
import datetime

app = Flask(__name__)

app.secret_key = 'random string'

#DB connection details
HOST='utacloud1.reclaimhosting.com'
USER = 'sxn7873_surya'
PASSWORD='Pn2E)^Gq&Dc]'
DATABASE='sxn7873_adb'




@app.route('/')
def index():
    return render_template('index.html')

#A specific function to set up a db connection
def dbConnect():
    global conn # defining a global variable
    #connect to database
    conn = mysql.connect(host=HOST,user=USER,password=PASSWORD,database=DATABASE)
    return conn

def groupByMag(fields):
    query = "select t.new as 'mag_range', count(*) as 'number_of_occurences' from ( "
    query+="select case when mag>=1 and mag<2 then '1-2' "
    query+="when mag>=2 and mag<3 then '2-3' when mag>=3 and mag<4 then '3-4' "
    query+="when mag>=4 and mag<5 then '4-5' when mag>=5 and mag<6 then '5-6' "
    query+="when mag>=6 and mag<7 then '6-7' else 'other(negatives)' end as new "
    query+="from earthquake "
    query+="where date(time)>=date(curdate()-"
    query+=fields['days']+")"
    query+=" ) t group by t.new"
    dbConnect()
    cursor = conn.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    print(query)
    print(res)
    conn.close()
    return res


@app.route('/groupby',methods=['POST','GET'])
def groupBy():
    if request.method=='POST':
        dic={}
        for key,value in request.form.items():
            if value!='':
                dic[key]=value

        if dic:
            result=groupByMag(dic)
            if result==[]:
                result=[]
                flash('No records of earthquake for above mentioned days')

        else:
            result=[]
            flash('Please enter values in the field')

        
    return render_template('index.html',data2=result)



if __name__ == "__main__":
    app.run()