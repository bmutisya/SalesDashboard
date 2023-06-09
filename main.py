import requests
import plotly.express as px
import streamlit as st
import numpy as np
import calendar
import pandas as pd

df = pd.read_excel('sales_data.xlsx')
df= df.mask(df == '')
df.columns = df.columns.str.replace(" ","_")
#print(df.columns)


st.set_page_config(page_title = "Sales Dashboard",
                   page_icon =":bar_chart:",
                   layout= "wide")
#st.dataframe(df)

#sidebar
st.sidebar.header("please select Filter Here")
salesrep = st.sidebar.multiselect(
    "Flter by Sales Rep:",
    options=df["Sales_Rep"].unique(),default=df["Sales_Rep"].unique())

def extract_month(df):
    date_col = pd.DatetimeIndex(df['Date_Sold'])
    #date_col
    #df['year']=date_col.year
    df['month']=date_col.month
    #df['Day']=date_col.day
    df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])

extract_month(df)
month= st.sidebar.multiselect("Filter by month:",options=df["month"].unique(),default=df["month"].unique())
# Replace NAN with uncategorised
df['Client_Category']= df['Client_Category'].replace(np.nan, 'Uncategorised')

clientcategory = st.sidebar.multiselect(
    "Filter by Client Category:",
    options=df["Client_Category"].unique(),default=df["Client_Category"].unique())
# Replace NAN with uncategorised
df['Product_Sub_Category']= df['Product_Sub_Category'].replace(np.nan, 'Uncategorised')
productcategory = st.sidebar.multiselect(
    "Filter by product SubCategory:",
    options=df["Product_Sub_Category"].unique(),default=df["Product_Sub_Category"].unique())
df_selection = df.query(
    "Sales_Rep == @salesrep & Client_Category == @clientcategory & Product_Sub_Category == @productcategory & month == @month"
)
#st.dataframe(df)
# Main Page
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

#TopKPIS
total_sales = int(df_selection["value"].sum())
sales_tonnes = round(df_selection["Volume_in_Tonnes"].sum(),1)
left_column,middle_column,right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"KSH  {total_sales:,}")
with middle_column:
    st.subheader("Volume in Tonnes:")
    st.subheader(sales_tonnes)
with right_column:
    st.subheader("Total Sales:")
    st.subheader(f"KSH {total_sales:,}")
#insert a divider with the makdown tool
st.markdown("---")


#plot a barchart
#sales_by_salesrep= (df_selection.groupby(by=["Sales_Rep"]).sum()[["value"]].sort_values(by="value"))
sales_by_salesrep=pd.DataFrame(df_selection.groupby("Sales_Rep")["value"].sum())
fig_salesreps = px.bar( sales_by_salesrep,
                        x=sales_by_salesrep.index,y="value",
                        orientation="v",
                        title="<b>Sales by  SalesRep</b>",
                        color_discrete_sequence=["#FF00FF"] *len (sales_by_salesrep),
                        template="plotly_white",
)
fig_salesreps.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis= (dict(showgrid=False))
)
#draw the graph
#st.plotly_chart(fig_salesreps)

#sales_by_clientcategory= (df_selection.groupby(by=["Client_Category"]).sum()[["value"]].sort_values(by="value"))
sales_by_clientcategory= pd.DataFrame(df_selection.groupby("Client_Category")["value"].sum())
fig_clientcategory = px.bar( sales_by_clientcategory,
                        x=sales_by_clientcategory.index,y="value",
                        orientation="v",
                        title="<b>Sales by Client Category</b>",
                        color_discrete_sequence=["#FF00FF"] *len (sales_by_clientcategory),
                        template="plotly_white",
)
fig_clientcategory.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis= (dict(showgrid=False))
)
left_column,right_column =st.columns(2)
left_column.plotly_chart(fig_salesreps, use_container_width=True)
right_column.plotly_chart(fig_clientcategory,use_container_width=True)

st.markdown("___")
#st.plotly_chart(fig_salesreps)

sales_by_product= (df_selection.groupby(by=["Product_Name"]).sum()[["Volume_in_Tonnes"]].sort_values(by="Volume_in_Tonnes"))
fig_product = px.bar( sales_by_product,
                        x=sales_by_product.index,y="Volume_in_Tonnes",
                        orientation="v",
                        title="<b>Sales by Product Name</b>",
                        color_discrete_sequence=["#FF00FF"] *len (sales_by_product),
                        template="plotly_white",
)
fig_product.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis= (dict(showgrid=False))
)
st.plotly_chart(fig_product)

jupi=pd.DataFrame(df_selection.groupby('Sales_Rep')['Client'].nunique())
fig_unique_clients=px.bar(jupi,x=jupi.index,y=jupi.Client,orientation="v",
                        title="<b>Unique Clients Sold To</b>",
                        color_discrete_sequence=["#FF00FF"] *len (jupi),
                        template="plotly_white")
st.plotly_chart(fig_unique_clients)


df

















# Hide Streamlit Style

hide_st_style = """
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>

"""
st.markdown(hide_st_style, unsafe_allow_html = True)
