
from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import joblib
import plotly.express as px
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# DB Connection Function
def get_sales_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="agri_sales_db"
    )
    df = pd.read_sql("SELECT * FROM sales_data", conn)
    conn.close()
    return df

@app.route('/')
def landing_page():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    df = get_sales_data()
    fig = px.line(df, x='date', y='sales', title='Sales Trend Over Time')
    graph = fig.to_html(full_html=False)

    kpis = {
        "Total Sales": f"${df['sales'].sum():,.2f}",
        "Avg Order Value": f"${df['sales'].mean():,.2f}",
        "Conversion Rate": "2.9%",
        "Customer Acquisition Cost": "$38.50"
    }

    return render_template('dashboard.html', graph=graph, kpis=kpis)

@app.route('/analysis')
def analysis():
    df = get_sales_data()
    category_chart = px.bar(df, x='product_category', y='sales', title='Sales by Category')
    channel_pie = px.pie(df, names='sales_channel', values='sales', title='Sales by Channel')
    return render_template('analysis.html', 
                           bar_chart=category_chart.to_html(full_html=False), 
                           pie_chart=channel_pie.to_html(full_html=False))

@app.route('/recommendations')
def recommendations():
    df = get_sales_data()
    recs = []
    peak = df[df['sales'] > df['sales'].quantile(0.75)]
    low = df[df['sales'] < df['sales'].quantile(0.25)]

    if not peak.empty:
        recs.append({
            "title": "Maintain Peak Performers",
            "desc": "Boost marketing, maintain inventory for top-selling products."
        })
    if not low.empty:
        recs.append({
            "title": "Improve Low Performers",
            "desc": "Adjust pricing, marketing or replace underperforming products."
        })

    return render_template('recommendations.html', recs=recs)

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True)
