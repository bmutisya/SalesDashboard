import requests
import plotly.express as px
import streamlit as st
import numpy as np
import calendar
import pandas as pd

st.set_page_config(page_title="Diary Analysis",
                   page_icon=":🕰:",
                   layout="wide")


@st.cache_data
def get_data_from_excel():
    df = pd.read_excel('appointments-data.xlsx')
    df = df.mask(df == '')
    df.columns = df.columns.str.replace(" ", "_")
    df["hour"] = pd.to_datetime(df["Checkin_Time"], format="mixed").dt.hour

    return df


# print(df.columns)
df = get_data_from_excel()


def extract_month(df):
    date_col = pd.DatetimeIndex(df['Appointment_Date'])
    # date_col
    # df['year']=date_col.year
    df['month'] = date_col.month
    df['Day']=date_col.day
    df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])


extract_month(df)
# st.dataframe(df)

st.sidebar.header("Please Filter Here")
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
status = st.sidebar.multiselect("Filter By Appointments Status:",
                                options=df["Status"].unique(),
                                default=df["Status"].unique()
                                )

# we use @ to refere to the above variables
df_selection = df.query("Sales_Unit == @region & Sales_Rep == @salesrep & Status ==@status & month ==@month")

df_selection['Status'] = df_selection['Status'].where(
    df_selection['Status'].isin(['Attended', 'Missed', 'Addressed']),
    'Addressed'
)

st.title(":bar_chart: Dairy Analysis")
st.markdown("---")
# Use Markdown syntax with CSS styling to center the subheader
st.markdown("<h4 style='text-align: center;'>Appointments Analysis</h4>", unsafe_allow_html=True)

st.markdown("##")

total_appointments = df_selection.shape[0]
total_attended = df_selection[df_selection['Status'] == 'Attended'].shape[0]
total_missed = df_selection[df_selection['Status'] == 'Missed'].shape[0]
total_addressed = df_selection[df_selection['Status'] == 'Addressed'].shape[0]
efficiency = round((total_attended / total_appointments) * 100, 2)
efficiency = f" {efficiency} %"
left_column, middle_column, right_column, last_column, five_column = st.columns(5)
with left_column:
    with st.container():
        st.subheader("Total")
        st.subheader(total_appointments)

        # Apply CSS styling for circular box background
        st.markdown("""
            <style>
            .stContainer {
                border-radius: 50px;
                background-color: #F5F5F5;
                padding: 20px;
            }
            </style>
        """, unsafe_allow_html=True)
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

appointment_by_status = (
    df_selection.groupby(by=["Status"]).count()[["Client"]].sort_values(by="Client")
)
fig_status = px.bar(
    appointment_by_status,
    x=appointment_by_status.index,
    y="Client",
    orientation="v",
    title="<b> Appointments by Status</b>",
    color=appointment_by_status.index,
    # color_discrete_sequence=["#0086B8"] * len(appointment_by_status),
    template="plotly_white"
)
# how to remove background color by use of layout.
fig_status.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))
)
st.plotly_chart(fig_status)

import plotly.express as px

appointments_by_hour = (
    df_selection[df_selection['Status'] == 'Attended'].groupby(by=["hour", "month"]).count()[["Client"]]
        .sort_values(by="hour").reset_index()
)
# appointments_by_hour=appointments_by_hour.reset_index()
fig_appointments_hour = px.line(
    appointments_by_hour,
    x="hour",
    y="Client",
    color="month",
    orientation="v",
    title="<b> Appointments analysis by hour</b>",
    # color_discrete_sequence=["#0086B8"]*len(appointments_by_hour),
    template="plotly_white"
)
fig_appointments_hour.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))
)
st.plotly_chart(fig_appointments_hour)

# unique_clients_visited = (
#     df_selection[df_selection['Status'] == 'Attended'].groupby('Sales_Rep')['Client'].nunique()
# )
# fig_unique_clients = px.bar(
#     unique_clients_visited,
#     x=unique_clients_visited.index,
#     y="Client",
#     orientation="v",
#     title="<b> Unique Clients Visited Per Rep</b>",
#     color_discrete_sequence=["#0086B8"] * len(unique_clients_visited),
#     template="plotly_white"
# )
# # how to remove background color by use of layout.
# fig_unique_clients.update_layout(
#     plot_bgcolor="rgba(0,0,0,0)",
#     yaxis=(dict(showgrid=False))
# )
# st.plotly_chart(fig_unique_clients)

unique_clients_visited = (
    df_selection[df_selection['Status'] == 'Attended'].groupby('Sales_Rep')['Client'].nunique()
)

fig_unique_clients = px.bar(
    unique_clients_visited,
    x=unique_clients_visited.index,
    y="Client",
    orientation="v",
    title="<b> Unique Clients Visited Per Rep</b>",
    color=unique_clients_visited.index,  # Assigning different colors based on Sales_Rep
    template="plotly_white"
)

# Remove background color using layout
fig_unique_clients.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(showgrid=False)
)

st.plotly_chart(fig_unique_clients)

# Calculate count of clients with the status of "Attended" per rep
attended_clients = df_selection[df_selection['Status'] == 'Attended'].groupby('Sales_Rep').size()
# Calculate count of all clients per rep
total_clients = df_selection.groupby('Sales_Rep').size()
# Calculate compliance percentage per rep
compliance = (attended_clients / total_clients) * 100
# Round the compliance values to two decimal places
compliance = compliance.round(2)

fig_rep_compliance = px.bar(
    x=compliance.index,
    y=compliance.values,
    title="<b>Compliance Percentage per Rep</b>",
    labels={'x': 'Sales Rep', 'y': 'Compliance Percentage'},
    color=compliance.index,
    template="plotly_white"
)

# Customize the layout
fig_rep_compliance.update_layout(
    xaxis_tickangle=-45,
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(showgrid=False),
)

# Show the chart
st.plotly_chart(fig_rep_compliance)










st.dataframe(df_selection)

hide_st_style = """
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>

"""
st.markdown(hide_st_style, unsafe_allow_html=True)
