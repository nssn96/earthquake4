# Name : Surya Narayanan Nadhamuni Suresh
# UTA ID : 1001877873

# References used for assignment 4

# https://developers.google.com/chart/interactive/docs/quick_start


# Dynamic charts implementation using flask 
# https://www.youtube.com/watch?v=kt80L6f9dj8

# scatter chart 
# https://developers.google.com/chart/interactive/docs/gallery/scatterchart

# bar chart
# https://developers.google.com/chart/interactive/docs/gallery/columnchart

# for time conversion
# 1) https://stackoverflow.com/questions/51625018/to-find-whether-its-day-or-night-using-time-module-in-python#:~:text=For%20something%20more%20airy-fairy%20%28like%20day%20and%20night%29%2C,%28%27It%20is%20night-time%27%29%20else%3A%20print%20%28%27It%20is%20day-time%27%29

# 2) https://www.geeksforgeeks.org/extract-time-from-datetime-in-python/



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
    query = "Select max(val),min(val) from tab"
    query2 = "select val from tab"
    dbConnect()
    cursor = conn.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    cursor.execute(query2)
    res2 = cursor.fetchall()
    print(query)
    print(res)
    for i in res:
        MAX = i[0]
        MIN = i[1]
    
    split = (int(MAX)-int(MIN))//int(fields['N'])
    temp=[]
    l = 0
    h=split
    
    for i in range(int(fields['N'])):
        count=0
        for j in res2:
            for k in j:

                if k>l and k<h:
                    count=count+1
        l=l+split
        h=h+split
        temp.append([i+1,count])
    
    print(temp)


    conn.close()
    return temp
    # dayC=0
    # nightC=0
    # temp=[]
    # for i in res:
    #     mytime= i[0].time()
    #     #print(mytime.hour)
    #     if mytime.hour < 6 or mytime.hour > 18:
    #         nightC=nightC+1
    #     else:
    #         dayC=dayC+1
    # temp.append(['AM',dayC])
    # temp.append(['PM',nightC])
    # print(temp)

def recentN(fields):
    query = "Select val from tab"
    dbConnect()
    cursor = conn.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    print(query)
    
    split = (int(fields['high'])-int(fields['low']))//int(fields['N'])
    temp=[]
    l = 0
    h=split
    
    for i in range(int(fields['N'])):
        count=0
        for j in res:
            for k in j:

                if k>l and k<h:
                    count=count+1
        l=l+split
        h=h+split
        temp.append([i+1,count])
    
    print(temp)


    conn.close()
    return temp


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

        
    return render_template('index.html',data1=result)


@app.route('/recent',methods=['POST','GET'])
def recent():
    if request.method=='POST':
        dic={}
        for key,value in request.form.items():
            if value!='':
                dic[key]=value

        if dic:
            result=recentN(dic)
            if result==[]:
                result=[]
                flash('No records of earthquake for above mentioned days')

        else:
            result=[]
            flash('Please enter values in the field')

        
    return render_template('index.html',data2=result)


if __name__ == "__main__":
    app.run()