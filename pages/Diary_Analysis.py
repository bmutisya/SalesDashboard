import requests
import plotly.express as px
import streamlit as st
import numpy as np
import calendar
import pandas as pd

st.set_page_config(page_title = "Diary Analysis",
                   page_icon =":🕰:",
                   layout= "wide")
@st.cache_data
def get_data_from_excel():
   df = pd.read_excel('appointments-data.xlsx')
   df= df.mask(df == '')
   df.columns = df.columns.str.replace(" ","_")
   df["hour"] = pd.to_datetime(df["Checkin_Time"], format="mixed").dt.hour

   return df
#print(df.columns)
df=get_data_from_excel()

def extract_month(df):
    date_col = pd.DatetimeIndex(df['Appointment_Date'])
    #date_col
    #df['year']=date_col.year
    df['month']=date_col.month
    #df['Day']=date_col.day
    df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])

extract_month(df)
#st.dataframe(df)

st.sidebar.header("Please Filter Here")
region= st.sidebar.multiselect("Filter By Region:",
                               options=df["Sales_Unit"].unique(),
                               default=df["Sales_Unit"].unique()
                               )
salesrep= st.sidebar.multiselect("Filter by Sales Person:",
                               options=df["Sales_Rep"].unique(),
                               default=df["Sales_Rep"].unique()
                               )
status= st.sidebar.multiselect("Filter By Appointments Status:",
                               options=df["Status"].unique(),
                               default=df["Status"].unique()
                               )
month= st.sidebar.multiselect("Filter By Month:",
                               options=df["month"].unique(),
                               default=df["month"].unique()
                               )
# we use @ to refere to the above variables
df_selection= df.query("Sales_Unit == @region & Sales_Rep == @salesrep & Status ==@status & month ==@month")
st.dataframe(df_selection)

st.title(":bar_chart: Dairy Analysis")
st.markdown("---")
# Use Markdown syntax with CSS styling to center the subheader
st.markdown("<h4 style='text-align: center;'>Appointments Analysis</h4>", unsafe_allow_html=True)


st.markdown("##")

total_appointments = df_selection.shape[0]
total_attended = df_selection.shape[0]
total_missed = df_selection.shape[0]
total_addressed = df_selection.shape[0]
efficiency = (total_attended/total_appointments)* 100
left_column,middle_column,right_column,last_column,five_column =st.columns(5)
with left_column:
    st.subheader("Total")
    st.subheader(total_appointments)
with middle_column:
    st.subheader("Attended")
    st.subheader(total_attended)
with right_column:
    st.subheader("Missed")
    st.subheader(total_missed)
with last_column:
    st.subheader("Addressed")
    st.subheader(total_addressed)
with five_column:
    st.subheader("% Efficiency")
    st.subheader(efficiency)
st.markdown("---")

appointment_by_status =(
    df_selection.groupby(by=["Status"]).count()[["Client"]].sort_values(by="Client")
)
fig_status= px.bar(
    appointment_by_status,
    x=appointment_by_status.index,
    y="Client",
    orientation="v",
    title="<b> Appointments by Status</b>",
    color_discrete_sequence=["#0086B8"]*len(appointment_by_status),
    template="plotly_white"
)
#how to remove background color by use of layout.
fig_status.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))
)
st.plotly_chart(fig_status)


import plotly.express as px






appointments_by_hour = (
    df_selection.groupby(by=["hour","month"]).count()[["Client"]].sort_values(by="hour").reset_index()
)
#appointments_by_hour=appointments_by_hour.reset_index()
fig_appointments_hour= px.line(
    appointments_by_hour,
    x="hour",
    y="Client",
    color="month",
    orientation="v",
    title="<b> Appointments by Status</b>",
    #color_discrete_sequence=["#0086B8"]*len(appointments_by_hour),
    template="plotly_white"
)
fig_appointments_hour.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))
)
st.plotly_chart(fig_appointments_hour)











hide_st_style = """
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>

"""
st.markdown(hide_st_style, unsafe_allow_html = True)