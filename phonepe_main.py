import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu
from PIL import Image
from git.repo.base import Repo

icon = Image.open("phone.png")
st.set_page_config(page_title= "Phonepe Pulse Data Visualization | By GOBINATH M",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
)

st.sidebar.header(" :green[**Hello! Welcome to the dashboard**]")

#Repo.clone_from("https://github.com/PhonePe/pulse.git", "E:/Phonepe_Pulse_project/Data")

config=sql.connect(
host="127.0.0.1",
user="root",
password="Gobi_7890",
database='phonepe_pulse'
)
print(config)
mycursor = config.cursor(buffered=True)

with st.sidebar:
    Type = option_menu("Menu", ["Home","Top Charts","Explore Data"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#00ff00"},
                        "nav-link-selected": {"background-color": "#ffa500"}})

if Type == "Home":
    st.markdown("# :blue[Data Visualization and Exploration]")
    st.markdown("## :blue[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :red[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :red[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
    with col2:
        st.image("phonegif.gif")
if Type == "Top Charts":
    st.markdown("## :green[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.selectbox("**Year**", options=list(range(2018, 2023)))
        Quarter = st.radio("Quarter", options=[1, 2, 3, 4])
    
    with colum2:
        
        st.write(
    """
    #### <span style='color:blue'>From this menu we can get insights like :</span>
    - <span style='color:green'>Overall ranking on a particular Year and Quarter.</span>
    - <span style='color:purple'>Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.</span>
    - <span style='color:orange'>Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.</span>
    - <span style='color:red'>Top 10 mobile brands and its percentage based on the how many people use phonepe.</span>
    """,
    unsafe_allow_html=True)

 
    
if Type == "Transactions":
    col1, col2, col3 = st.columns([1, 1, 1], gap="small")

    with col1:
        st.markdown("### :green[State]")
        mycursor.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from agg_trans where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count', 'Total_Amount'])
        
        fig = px.pie(df, 
             values='Total_Amount',
             names='State',
             title='Top 10 States by Transaction Amount',
             color_discrete_sequence=px.colors.qualitative.Set3,  
             hover_data=['Transactions_Count'],
             labels={'Transactions_Count': 'Transactions Count'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### :green[District]")
        mycursor.execute(f"select district, sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count', 'Total_Amount'])

        fig = px.pie(df, values='Total_Amount',
                     names='District',
                     title='Top 10 Districts by Transaction Amount',
                     color_discrete_sequence=px.colors.sequential.Darkmint,
                     hover_data=['Transactions_Count'],
                     labels={'Transactions_Count': 'Transactions Count'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.markdown("### :green[Pincode]")
        mycursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count', 'Total_Amount'])
        fig = px.pie(df, values='Total_Amount',
                     names='Pincode',
                     title='Top 10 Pincodes by Transaction Amount',
                     color_discrete_sequence=px.colors.sequential.Magenta,  
                     hover_data=['Transactions_Count'],
                     labels={'Transactions_Count': 'Transactions Count'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

# Top Charts - USERS          
if Type == "Users":
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2], gap="small")

    with col1:
        st.markdown("### :green[Brands]")
        if Year == 2022 and Quarter in [2, 3, 4]:
            st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
        else:
            mycursor.execute(f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users', 'Avg_Percentage'])
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="Brand",
                         orientation='h',
                         color='Avg_Percentage',
                         color_continuous_scale='viridis')  
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### :green[District]")
        mycursor.execute(f"select district, sum(Registered_User) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users', 'Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(float)
        fig = px.bar(df,
                     title='Top 10',
                     x="Total_Users",
                     y="District",
                     orientation='h',
                     color='Total_Users',
                     color_continuous_scale='viridis')  
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.markdown("### :green[Pincode]")
        mycursor.execute(f"select Pincode, sum(Registered_Users) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
        fig = px.pie(df,
                     values='Total_Users',
                     names='Pincode',
                     title='Top 10',
                     color_discrete_sequence=px.colors.sequential.Plasma)  
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown("### :green[State]")
        mycursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
        fig = px.pie(df, values='Total_Users',
                     names='State',
                     title='Top 10',
                     color_discrete_sequence=px.colors.sequential.Plasma,  
                     hover_data=['Total_Appopens'],
                     labels={'Total_Appopens': 'Total_Appopens'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
            

if Type == "Explore Data":
    Year = st.sidebar.number_input("Select Year", min_value=2018, max_value=2022, value=2022, step=1)  
    Quarter = st.sidebar.select_slider("Select Quarter", options=[1, 2, 3, 4])  
    Type = st.sidebar.selectbox("Select Data Type", ("Transactions", "Users"), key="data_type_select") 

    col1, col2 = st.columns(2)

    
   
    with col1:
        st.markdown("<span style='color:blue; font-size: large;'>Overall State Data - Transactions Amount</span>", unsafe_allow_html=True)
        mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
        df2 = pd.read_csv('Statenames.csv')
        df1.State = df2

        fig = px.scatter_geo(df1, 
                             locations='State',
                             locationmode='country names',
                             color='Total_amount',
                             color_continuous_scale='Viridis',  
                             hover_name='State',
                             size='Total_amount',
                             projection='natural earth',
                             scope='asia',  
                            )
        fig.update_geos(
        center=dict(lon=78, lat=22),  
        projection_scale=5,  
        )
        
        st.plotly_chart(fig, use_container_width=True)

    
    with col2:
        st.markdown("<span style='color:green; font-size: large;'>Overall State Data - Transactions Count</span>", unsafe_allow_html=True)
        mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
        df2 = pd.read_csv('Statenames.csv')
        df1.Total_Transactions = df1.Total_Transactions.astype(int)
        df1.State = df2

        fig = px.scatter_geo(df1, 
                             locations='State',
                             locationmode='country names',
                             color='Total_Transactions',
                             color_continuous_scale='Viridis',  
                             hover_name='State',
                             size='Total_Transactions',
                             projection='natural earth',
                             scope='asia',  
                             )  
        
        fig.update_geos(
        center=dict(lon=78, lat=22),  
        projection_scale=5, 
        )
        st.plotly_chart(fig, use_container_width=True)
