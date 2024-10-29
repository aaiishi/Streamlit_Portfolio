import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.title("Data Visualization Project")
st.write("---")

# Load and clean your museum data
@st.cache_data
def load_data():
    df = pd.read_csv("assets/frequentation-des-musees-de-france.csv", delimiter=';')
    
    df['ANNEE'] = pd.to_datetime(df['ANNEE'], format='%Y')
    df['DATE APPELLATION'] = pd.to_datetime(df['DATE APPELLATION'], format='%d/%m/%Y', errors='coerce')
    
    df['PAYANT'] = df['PAYANT'].fillna(0)
    df['GRATUIT'] = df['GRATUIT'].fillna(0)
    df['TOTAL'] = df['TOTAL'].fillna(0)
    
    df['REGION'] = df['REGION'].str.strip().str.title()
    df['VILLE'] = df['VILLE'].str.strip().str.title()
    
    df['NET_VISITORS'] = df['PAYANT'] + df['GRATUIT']
    
    df = df.dropna(subset=['TOTAL'])
    df = df.drop(columns=['NOTE', 'ID MUSEOFILE', 'OBSERVATIONS'])
    
    return df

# Calculate statistics by year
def aggregate_data_by_year(df):
    df_annual = df.groupby(df['ANNEE'].dt.year).agg({
        'REF DU MUSEE': 'nunique',
        'NET_VISITORS': 'sum',
        'GRATUIT': 'sum',
        'PAYANT': 'sum'
    }).reset_index()

    df_annual.rename(columns={'REF DU MUSEE': 'TOTAL_MUSEES'}, inplace=True)
    return df_annual

# Create charts function
def create_metric_chart(df, column, chart_type, height=150):
    chart_data = df[[column, 'ANNEE']].set_index('ANNEE')
    if chart_type == 'Bar':
        st.bar_chart(chart_data, height=height)
    elif chart_type == 'Area':
        st.area_chart(chart_data, height=height)

# Load the museum data
df = load_data()

# Sidebar widgets
with st.sidebar:
    st.title("Museum Dashboard")
    st.header("⚙️ Settings")
    
    min_year = df['ANNEE'].dt.year.min()
    max_year = df['ANNEE'].dt.year.max()
    
    start_year = st.slider("Select Start Year", min_value=min_year, max_value=max_year, value=min_year)
    end_year = st.slider("Select End Year", min_value=min_year, max_value=max_year, value=max_year)

    chart_selection = st.selectbox("Select a chart type", ("Bar", "Area"))

# Filter data based on user selection
df_filtered = df[(df['ANNEE'].dt.year >= start_year) & (df['ANNEE'].dt.year <= end_year)]
df_annual = aggregate_data_by_year(df_filtered)

# Display main statistics
st.subheader("All-Time Statistics")
metrics = [
    ("Total Museums", "TOTAL_MUSEES"),
    ("Net Visitors", "NET_VISITORS"),
    ("Free Entries", "GRATUIT"),
    ("Paid Entries", "PAYANT")
]

# Create columns for displaying metrics
cols = st.columns(2)
for col, (title, column) in zip(cols, metrics[:2]):
    total_value = df_annual[column].sum()
    with col:
        st.metric(title, f"{total_value:,}")
        create_metric_chart(df_annual, column, chart_selection)

# Create another set of columns for the remaining metrics
cols = st.columns(2)
for col, (title, column) in zip(cols, metrics[2:]):
    total_value = df_annual[column].sum()
    with col:
        st.metric(title, f"{total_value:,}")
        create_metric_chart(df_annual, column, chart_selection)

# Display the filtered DataFrame
with st.expander('See DataFrame (Selected time frame)'):
    st.dataframe(df_filtered)

st.write("---")

# Extract department information and standardize names
df['DEPARTMENT'] = df['DEPARTEMENT'].str.extract('([\w-]+)')[0].str.strip()

# Mapping of departments to ensure they match GeoJSON properties if necessary
department_mapping = {
    "TARN": "Tarn",
    "TARN-ET-GARONNE": "Tarn-et-Garonne",
    # Add other mappings as needed
}

# Apply mapping to the DEPARTMENT column
df['DEPARTMENT'] = df['DEPARTMENT'].replace(department_mapping)

# Calculate total net visitors by department
df_department_visitors = df.groupby('DEPARTMENT')['NET_VISITORS'].sum().reset_index()
df_department_visitors.rename(columns={'NET_VISITORS': 'TOTAL_VISITORS'}, inplace=True)

# Select the top 10 departments by total visitors
top_departments = df_department_visitors.nlargest(10, 'TOTAL_VISITORS')

# Display the DataFrame for top departments
st.subheader("Top 10 Departments by Net Visitors")
st.dataframe(top_departments)

# Check if the DataFrame is empty before plotting
if not top_departments.empty:
    st.subheader("Pie Chart of Top 10 Net Visitors by Department")
    
    # Create a pie chart for the top departments
    plt.figure(figsize=(10, 8))
    plt.pie(top_departments['TOTAL_VISITORS'], labels=top_departments['DEPARTMENT'], autopct='%1.1f%%', startangle=140)
    plt.title("Top 10 Net Visitors by Department")
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Display the pie chart in Streamlit
    st.pyplot(plt)
else:
    st.warning("No data available for top departments.")

st.write("---")

# Calculate the number of museums by department
df_museum_count = df.groupby('DEPARTMENT')['REF DU MUSEE'].nunique().reset_index()
df_museum_count.rename(columns={'REF DU MUSEE': 'NUM_MUSEES'}, inplace=True)

# Select the top 15 departments by number of museums
top_museum_departments = df_museum_count.nlargest(15, 'NUM_MUSEES')

# Display the DataFrame for museum counts
st.subheader("Top 15 Departments by Number of Museums")
st.dataframe(top_museum_departments)

# Check if the DataFrame is empty before plotting
if not top_museum_departments.empty:
    st.subheader("Bar Chart of Number of Museums by Department")
    
    # Create a bar plot for the number of museums
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_museum_departments, x='DEPARTMENT', y='NUM_MUSEES', palette='coolwarm')
    plt.title("Number of Museums by Department")
    plt.xlabel("Department")
    plt.ylabel("Number of Museums")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Display the bar chart in Streamlit
    st.pyplot(plt)
else:
    st.warning("No data available for museum counts.")

st.write("---")

# Calculate total net visitors by museum in Paris
df_paris = df[df['VILLE'] == 'Paris']
df_museum_visitors_paris = df_paris.groupby('NOM DU MUSEE')['NET_VISITORS'].sum().reset_index()
df_museum_visitors_paris.rename(columns={'NET_VISITORS': 'TOTAL_VISITORS'}, inplace=True)

# Select the top 10 museums by total visitors
top_museums_paris = df_museum_visitors_paris.nlargest(10, 'TOTAL_VISITORS')

# Display the DataFrame for top museums
st.subheader("Top 10 Most Visited Museums in Paris")
st.dataframe(top_museums_paris)

# Check if the DataFrame is empty before plotting
if not top_museums_paris.empty:
    st.subheader("Area Chart of Top 10 Most Visited Museums in Paris")
    
    # Create an area chart for the top museums
    area_chart_data = top_museums_paris.set_index('NOM DU MUSEE')['TOTAL_VISITORS']
    
    st.area_chart(area_chart_data)

else:
    st.warning("No data available for the top museums in Paris.")

st.write("---")

# Select the top 3 most visited museums in Paris
top_3_museums_paris = top_museums_paris.nlargest(3, 'TOTAL_VISITORS')

# Calculate total free and paid entries for the top 3 museums
df_top_3 = df_paris[df_paris['NOM DU MUSEE'].isin(top_3_museums_paris['NOM DU MUSEE'])]

# Group by museum and calculate the sum of free and paid entries
df_free_paid = df_top_3.groupby('NOM DU MUSEE').agg({'GRATUIT': 'sum', 'PAYANT': 'sum'}).reset_index()

# Create a new column with the last word of the museum names
df_free_paid['LAST_WORD'] = df_free_paid['NOM DU MUSEE'].str.split().str[-1]

# Melt the DataFrame for plotting
df_melted = df_free_paid.melt(id_vars='LAST_WORD', value_vars=['GRATUIT', 'PAYANT'], var_name='ENTRY_TYPE', value_name='NUMBER_OF_ENTRIES')

# Check if the DataFrame is empty before plotting
if not df_melted.empty:
    st.subheader("Bar Chart of Free and Paid Entries for the Top 3 Museums in Paris")
    
    # Create a bar plot for free and paid entries
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_melted, x='LAST_WORD', y='NUMBER_OF_ENTRIES', hue='ENTRY_TYPE', palette='coolwarm')
    plt.title("Free and Paid Entries for the Top 3 Museums in Paris")
    plt.xlabel("Museum Name")
    plt.ylabel("Number of Entries")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Display the bar chart in Streamlit
    st.pyplot(plt)
else:
    st.warning("No data available for free and paid entries.")

st.write("---")

# Calculate the net visitors for each museum by year
df_museum_yearly = df.groupby(['NOM DU MUSEE', df['ANNEE'].dt.year]).agg({'NET_VISITORS': 'sum'}).reset_index()

# Calculate the net visitor change from 2001 to 2021
df_museum_change = df_museum_yearly.pivot(index='NOM DU MUSEE', columns='ANNEE', values='NET_VISITORS').reset_index()
df_museum_change['VISITOR_CHANGE'] = df_museum_change[2021] - df_museum_change[2001]

# Select the top 5 museums by visitor change
top_museums_change = df_museum_change.nlargest(5, 'VISITOR_CHANGE')

# Filter the original yearly data for these top museums
df_top_museums_yearly = df_museum_yearly[df_museum_yearly['NOM DU MUSEE'].isin(top_museums_change['NOM DU MUSEE'])]

# Check if the DataFrame is empty before plotting
if not df_top_museums_yearly.empty:
    st.subheader("Line Chart of Top 5 Museums by Increase in Net Visitors (2001-2021)")
    
    # Create a line plot for the top museums
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_top_museums_yearly, x='ANNEE', y='NET_VISITORS', hue='NOM DU MUSEE', marker='o', palette='tab10')
    plt.title("Net Visitors Change for Top 5 Museums (2001-2021)")
    plt.xlabel("Year")
    plt.ylabel("Net Visitors")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Display the line chart in Streamlit
    st.pyplot(plt)

    # Dropdown for museum names and locations
    selected_museum = st.selectbox("Select a museum to view its location:", top_museums_change['NOM DU MUSEE'].tolist())
    location_info = df[df['NOM DU MUSEE'] == selected_museum][['NOM DU MUSEE', 'VILLE', 'DEPARTEMENT']].drop_duplicates()
    st.write(f"**Location:** {location_info['VILLE'].values[0]}, {location_info['DEPARTEMENT'].values[0]}")
else:
    st.warning("No data available for the top museums' visitor changes.")

st.write("---")

# Filter the DataFrame for museums in Paris
df_paris = df[df['VILLE'] == 'Paris']

# Calculate the net visitors for each museum in Paris by year
df_museum_yearly_paris = df_paris.groupby(['NOM DU MUSEE', df['ANNEE'].dt.year]).agg({'NET_VISITORS': 'sum'}).reset_index()

# Calculate the net visitor change from 2001 to 2021 for Paris museums
df_museum_change_paris = df_museum_yearly_paris.pivot(index='NOM DU MUSEE', columns='ANNEE', values='NET_VISITORS').reset_index()
df_museum_change_paris['VISITOR_CHANGE'] = df_museum_change_paris[2021] - df_museum_change_paris[2001]

# Select the top 5 museums in Paris by visitor change
top_museums_change_paris = df_museum_change_paris.nlargest(5, 'VISITOR_CHANGE')

# Filter the original yearly data for these top museums in Paris
df_top_museums_yearly_paris = df_museum_yearly_paris[df_museum_yearly_paris['NOM DU MUSEE'].isin(top_museums_change_paris['NOM DU MUSEE'])]

# Check if the DataFrame is empty before plotting
if not df_top_museums_yearly_paris.empty:
    st.subheader("Line Chart of Top 5 Museums in Paris by Increase in Net Visitors (2001-2021)")
    
    # Create a line plot for the top museums in Paris
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_top_museums_yearly_paris, x='ANNEE', y='NET_VISITORS', hue='NOM DU MUSEE', marker='o', palette='tab10')
    plt.title("Net Visitors Change for Top 5 Museums in Paris (2001-2021)")
    plt.xlabel("Year")
    plt.ylabel("Net Visitors")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Display the line chart in Streamlit
    st.pyplot(plt)