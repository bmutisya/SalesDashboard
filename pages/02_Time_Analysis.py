import requests
import plotly.express as px
import streamlit as st
import numpy as np
import calendar
import pandas as pd

st.set_page_config(page_title="Time Analysis",
                   page_icon=":⏰:",
                   layout="wide")


df = pd.read_excel('appointments_productivity.xlsx')
df = df.mask(df == '')
df.columns = df.columns.str.replace(" ", "_")
#df["hour"] = pd.to_datetime(df["Checkin_Time"], format="mixed").dt.hour
df = df.dropna(subset=['Total_Time_In_Market'])

def extract_month(df):
    date_col = pd.DatetimeIndex(df['Date'])
    # date_col
    # df['year']=date_col.year
    df['month'] = date_col.month
    df['Day']=date_col.day
    df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])


extract_month(df)
st.dataframe(df)

target_time = 12840

st.sidebar.header("Select Filter here")
month = st.sidebar.multiselect("Filter By Month:",
                               options=df["month"].unique(),
                               default=df["month"].unique()
                               )
region = st.sidebar.multiselect("Filter By Region:",
                                options=df["Sales_Unit"].unique(),
                                default=df["Sales_Unit"].unique()
                                )

salesrep = st.sidebar.multiselect("Filter by Sales Person:",
                                options=df["Sales_Rep"].unique(),
                                default=df["Sales_Rep"].unique()
                                  )
df_selection = df.query("Sales_Unit == @region & Sales_Rep == @salesrep & month ==@month")



st.title("Time Analysis")
st.markdown("##")

gf=df_selection.groupby(by=["Sales_Rep"]).sum()[["Total_Time_In_Market(Minutes)"]].sort_values(by="Total_Time_In_Market(Minutes)").reset_index()
no_months=df['month'].nunique()
gf['Target']= (12840* no_months)
gf['Compliance'] = ((gf['Total_Time_In_Market(Minutes)']/gf['Target'])*100).round(2)

total_time_in_appointments = df_selection['Total_Time_On_Appointments(Minutes)'].sum()
total_time_in_market = df_selection['Total_Time_In_Market(Minutes)'].sum()
total_target_time = gf["Target"].sum()
total_time_in_motion=total_time_in_market-total_time_in_appointments
time_efficiency =(total_time_in_market/total_target_time)*100
time_efficiency=time_efficiency.round(2)


#target_time_in_market=
left_column, middle_column, right_column, last_column,five_column = st.columns(5)
with left_column:
    st.subheader("T.T.App")
    st.subheader(total_time_in_appointments)
with middle_column:
    st.subheader("T.T.Market")
    st.subheader(total_time_in_market)
with right_column:
    st.subheader("T.T.Time")
    st.subheader(total_target_time)
with last_column:
    st.subheader("% T.Market")
    st.subheader(f"{time_efficiency} %")
with five_column:
    st.subheader("T.T.Motion")
    st.subheader(total_time_in_motion)
st.markdown("---")

fig_time_in_market = px.bar(
    gf,
    x="Sales_Rep",
    y="Compliance",
    orientation="v",
    title="<b> % Time in Market per Rep</b>",
    color="Sales_Rep",
    # color_discrete_sequence=["#0086B8"] * len(appointment_by_status),
    template="plotly_white"
)
fig_time_in_market.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
    title_x = 0.4
)
st.plotly_chart(fig_time_in_market)

data = {
    'Category': ['Total Appointments', 'Total Time in Market', 'Total Target Time','Total Time in Motion'],
    'Value': [total_time_in_appointments, total_time_in_market, total_target_time,total_time_in_motion]
}

df_time = pd.DataFrame(data)
fig_time_in_market = px.bar(
    df_time,
    x="Category",
    y="Value",
    orientation="v",
    title="<b> % Time in Market per Rep</b>",
    color="Category",
    # color_discrete_sequence=["#0086B8"] * len(appointment_by_status),
    template="plotly_white"
)
fig_time_in_market.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
    title_x = 0.4
)
st.plotly_chart(fig_time_in_market)

# Line Plot - Check-in and Check-out Times
fig_checkin_out = px.line(df, x='Date', y=['First_Checkin_Time', 'Last_Checkout_Time'],
                          title='Check-in and Check-out Times')
#st.plotly_chart(fig_checkin_out)
fig_monthly = px.line(df, x='month', y=['Total_Appointments_Attended', 'Time_Productivity_Ratio(%)'],
                      title='Monthly Performance Trends')
st.plotly_chart(fig_monthly)

fig_ratio = px.pie(df, names='Sales_Rep', values='Ratio(%)', title='Appointment Attendance Ratio')
st.plotly_chart(fig_ratio)