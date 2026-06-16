import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')
st.set_page_config(page_title="Superstore!!",
                   page_icon=":bar_chart:",
                   layout="wide")
st.title(":bar_chart: Superstore!!!")
f1=st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if f1 is not None:
    filename=f1.name
    st.write(filename)
    df=pd.read_excel(filename)
else:
    os.chdir(r"C:\Users\EXTPLIK\Downloads\python\streamlit")
    df=pd.read_excel("Superstore.xls")
col1,col2=st.columns((2))
df["Order Date"]=pd.to_datetime(df["Order Date"])
startDate=pd.to_datetime(df["Order Date"]).min()
endDate=pd.to_datetime(df["Order Date"]).max()
with col1:
    date1=pd.to_datetime(st.date_input("enter start date : ",startDate))
with col2:
    date2=pd.to_datetime(st.date_input("enter end date : ",endDate))
df=df[(df["Order Date"]>=date1)&(df["Order Date"]<=date2)].copy()
st.sidebar.header("Choose you filter : ")
#region
region=st.sidebar.multiselect("Pick your region : ",df["Region"].unique())
if not region:
    df2=df.copy()
else:
    df2=df[df["Region"].isin(region)]
#state
state=st.sidebar.multiselect("Pick you state : ",df2["State"].unique())
if not state:
    df3=df2.copy()
else:
    df3=df2[df2["State"].isin(state)]
#city
city=st.sidebar.multiselect("Pick your city : ",df3["City"].unique())
if not city:
    df4=df3.copy()
else:
    df4=df3[df3["City"].isin(city)]
#filtered data
if not region and not state and not city :
    filter_data=df
elif not state and not city:
    filter_data=df2
elif not region and not city:
    filter_data=df[df["State"].isin(state)]
elif not region and not state:
    filter_data=df[df["City"].isin(city)]
elif region and state and city:
    filter_data=df4
elif region and state:
    filter_data=df3
elif state and city:
    filter_data=df[df["State"].isin(state) & df["City"].isin(city)]
elif region and city:
    filter_data=df[df["Region"].isin(region) & df["City"].isin(city)]
category_df=filter_data.groupby(by=["Category"],as_index=False)["Sales"].sum()
with col1:
    st.subheader("Ctegory wise Sales")
    fig=px.bar(category_df,x="Category",y="Sales",text = ['${:,.2f}'.format(x) for x in category_df["Sales"]],template="seaborn"
               )
    st.plotly_chart(fig,use_container_width=True,height=400)
with col2:
    st.subheader("Region wise sales")
    fig=px.pie(filter_data,values="Sales",names="Region",hole=0.5)
    st.plotly_chart(fig,use_container_width=True)
reg_data=filter_data.groupby(by="Region",as_index=False)["Sales"].sum()
cl1,cl2=st.columns((2))
with cl1:
    expander=st.expander("Category_Viewdata")
    expander.write(category_df.style.background_gradient(cmap="Blues"))
    csv=category_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download data",data=csv,file_name="Category wise sales.csv",mime="text/csv")
with cl2:
    expander=st.expander("Region_viewdata")
    expander.write(reg_data.style.background_gradient(cmap="Oranges"))
    csv=reg_data.to_csv(index=False).encode('utf-8')
    st.download_button("Download data",data=csv,file_name="Region wise sales.csv",mime="text/csv")
#timely sales analysis
filter_data["Month_year"]=filter_data["Order Date"].dt.to_period("M")
st.subheader("Timely Sales Analysis")
linechart=pd.DataFrame(filter_data.groupby(filter_data["Month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
fig2=px.line(linechart,x="Month_year",y="Sales",labels={"Sales":"Amount"},height=500,width=1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)
with st.expander("view data"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv=linechart.to_csv(index=False).encode("utf-8")
    st.download_button("download data",data=csv,file_name="Time Series analysis",mime="text/csv")
#tree map based on region,category,sub=category
treemap=df[["Region","Category","Sub-Category","Sales"]].groupby(by=["Region","Category","Sub-Category"])["Sales"].sum().reset_index()
fig4=px.treemap(treemap,
                path=["Region","Category","Sub-Category"],
                values="Sales",
                hover_data=["Sales"],
                color="Sub-Category",
                height=700,
                width=600)
st.plotly_chart(fig4,use_container_width=True)
chart1,chart2=st.columns((2))
with chart1:
    st.subheader("Segment wise sales")
    fig=px.pie(filter_data,values="Sales",names="Segment")
    fig.update_traces(text=filter_data["Segment"],textposition="inside")
    st.plotly_chart(fig,use_container_width=True)
with chart2:
    st.subheader("Category wise sales")
    fig=px.pie(filter_data,values="Sales",names="Category")
    fig.update_traces(text=filter_data["Category"],textposition="inside")
    st.plotly_chart(fig,use_container_width=True)
import plotly.figure_factory as ff
st.subheader(":point_right: Month wise Sub-Category Sales Summary")
with st.expander("Summary_table"):
    df_sample=df[0:5][["Region","State","City","Category","Sales","Profit","Quantity"]]
    fig=ff.create_table(df_sample,colorscale="Cividis")
    st.plotly_chart(fig,use_container_width=True)
    st.markdown("Month wise sub-category Tables")
    filter_data["month"]=filter_data["Order Date"].dt.month_name()
    sub_category_year=pd.pivot_table(data=filter_data,values="Sales",index=["Sub-Category"],columns="month")
    st.write(sub_category_year.style.background_gradient(cmap="Blues"))

#create a scatter plot
data1=px.scatter(filter_data,x="Sales",y="Profit",size="Quantity")
data1['layout'].update(title="Relationship between Sales and Profits using scatter plot",
                       font=dict(size=20),
                       xaxis=dict(title="Sales"),
                       yaxis=dict(title="Profit"))
st.plotly_chart(data1,use_container_width=True)

    
    





