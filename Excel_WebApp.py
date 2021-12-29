#### Import Libraries
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

### Set up the page

st.set_page_config(page_title = "Survey Results")
st.header("Survey Results 2021")

### Load the dataframe

excel_file = "Survey_Results.xlsx"
sheet_name = "DATA"
# Load the data using the read_excel method
# Use Sheet named Data
# Use columns B until D and the header is row 3
df = pd.read_excel(excel_file, sheet_name= sheet_name, usecols="B:D", header= 3 )

# Load the second table to be used.
# Load the data using the read_excel method
# Use Sheet named Data
# Use columns F until G and the header is row 3
df_participants = pd.read_excel(excel_file, sheet_name= sheet_name, usecols="F:G", header= 3 )


### STREAMLIT SELECTION

# Filter the data using the departments
# Get the unique number of departments
# Put them in a list
department = df["Department"].unique().tolist()

# Filter the data using the ages of the participants
# Get the unique number of ages
# Put them in a list
ages = df["Age"].unique().tolist()

# We will use a slider to select the age on the webapp
age_selection = st.slider("Age: ",
                          min_value=min(ages),
                          max_value=max(ages),
                          value = (min(ages), max(ages)))

# The slider will have a range, which is determined from the ages list

# Use a Multiselect widget for selecting the department
department_selection = st.multiselect("Department: ",
                                      department,
                                      default=department)

# Create the filters that will be used
# The mask will be used to grab the data we want from df dataframe based based on
# Ages selected and the Departments Selected
mask = (df["Age"].between(*age_selection) & (df["Department"].isin(department_selection)))

# The below is the number of entries that meet the required mask filter
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

# Group the dataframe after Selection

df_grouped = df[mask].groupby(by=["Rating"]).count()[["Age"]]
df_grouped = df_grouped.rename(columns = {"Age": "Votes"})
df_grouped = df_grouped.reset_index()

# Plot a Bar Chart on the number of votes based on the Age
bar_chart = px.bar(df_grouped,
                   x = "Rating",
                   y = "Votes",
                   text = "Votes",
                   color_discrete_sequence = ['#F63366']*len(df_grouped),
                   template = "plotly_white")

st.plotly_chart(bar_chart)

# Lets use the df_participants data frame
col1, col2 = st.columns(2)

# Add an image
image = Image.open("images/survey.jpg")
print(image)

# Add the image to the first column
col1.image(image,
           caption = "Designed by slidesgo/FreePik",
           use_column_width = True)

# Add the search results to the second column
# The second column will show the search results as a dataframe
col2.dataframe(df[mask])

# Plot a Pie Chart
pie_chart = px.pie(df_participants,
                   title = "Total Number of Participants",
                   values = "Participants",
                   names = "Departments")

st.plotly_chart(pie_chart)








