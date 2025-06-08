import streamlit as st
import base64
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

st.set_page_config(page_title="Phonepe with Menu")


def get_image_base64_from_file(path):
    if not os.path.exists(path):
        st.error(f"Image file not found: {path}")
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = get_image_base64_from_file("image/PhonePe_Logo.PNG")

if logo_base64 == "":
    st.stop()  # stop running if no logo found

st.markdown(f"""
    <style>
    /* Set entire page background */
    body {{
         background: linear-gradient(to bottom right, #5F259F, #FFFFFF);

    }}

    /* Also override Streamlit's default background for main container */
    .stApp {{
         background: linear-gradient(to bottom, #5F259F, #FFFFFF);
    }}

    .header {{
        display: flex;
        align-items: center;
        background-color: #5F259F;
        padding: 10px 20px;
    }}

    .header img {{
        height: 50px;
        margin-right: 30px;
    }}

    .menu {{
        display: flex;
        gap: 20px;
    }}

    .menu a {{
        position: relative;
        text-decoration: none;
        font-weight: 600;
        color: #f2f2f2;
        transition: color 0.3s ease;
        padding-bottom: 4px;
    }}

    .menu a::after {{
        content: "";
        position: absolute;
        left: 0;
        bottom: 0;
        height: 2px;
        width: 0%;
        background-color: #ffffff;
        transition: width 0.3s ease;
    }}

    .menu a:hover {{
        color: #e0d3f5; /* lighter contrast on hover */
    }}

    .menu a:hover::after {{
        width: 100%;
    }}
    </style>

    <div class="header">
        <img src="data:image/png;base64,{logo_base64}" alt="PhonePe Logo">
        <div class="menu">
            <a href="?page=home">Home</a>
            <a href="?page=analytics">Analytics</a>
            <a href="?page=reports">Reports</a>
            <a href="?page=settings">Settings</a>
        </div>
    </div>
""", unsafe_allow_html=True)
state_name_map = {
    "andaman-&-nicobar-islands": "Andaman and Nicobar Islands",
    "andhra-pradesh": "Andhra Pradesh",
    "arunachal-pradesh": "Arunachal Pradesh",
    "assam": "Assam",
    "bihar": "Bihar",
    "chandigarh": "Chandigarh",
    "chhattisgarh": "Chhattisgarh",
    "dadra-&-nagar-haveli-&-daman-&-diu": "Dadra and Nagar Haveli and Daman and Diu",
    "delhi": "NCT of Delhi",
    "goa": "Goa",
    "gujarat": "Gujarat",
    "haryana": "Haryana",
    "himachal-pradesh": "Himachal Pradesh",
    "jammu-&-kashmir": "Jammu & Kashmir",
    "jharkhand": "Jharkhand",
    "karnataka": "Karnataka",
    "kerala": "Kerala",
    "ladakh": "Ladakh",
    "lakshadweep": "Lakshadweep",
    "madhya-pradesh": "Madhya Pradesh",
    "maharashtra": "Maharashtra",
    "manipur": "Manipur",
    "meghalaya": "Meghalaya",
    "mizoram": "Mizoram",
    "nagaland": "Nagaland",
    "odisha": "Odisha",
    "puducherry": "Puducherry",
    "punjab": "Punjab",
    "rajasthan": "Rajasthan",
    "sikkim": "Sikkim",
    "tamil-nadu": "Tamil Nadu",
    "telangana": "Telangana",
    "tripura": "Tripura",
    "uttarakhand": "Uttarakhand",
    "uttar-pradesh": "Uttar Pradesh",
    "west-bengal": "West Bengal"
}

# Get query parameters (new API)
page = st.query_params.get("page", "home")

 


if page == "home":
    st.title("Home - User Registration Analysis")
    st.write(" Visualize user registration intensity across India with a dynamic map showing state-wise adoption over time by year and quarter.")
    # Load your PhonePe data
    df = pd.read_csv("C:/Users/Jeeva/Documents/PhonePepluse/Phonepe_Pluse_Analyzer/Data_Extract/Map_user.csv")
    # Filter options
    years = sorted(df['Year'].unique())
    quarters = sorted(df['Quarter'].unique())
    # UI for filtering
    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox("Select Year", years)
    with col2:
        selected_quarter = st.selectbox("Select Quarter",  quarters)
    # Filter the dataframe
    filtered_df = df[(df['Year'] == selected_year) & (df['Quarter'] == selected_quarter)]
    # If Registered_Users contains commas, remove them and convert to int
    filtered_df["Registered_Users"] = df["Registered_Users"].astype(str).str.replace(",", "").astype(int)
     # Fix state names if needed
    filtered_df['State'] = filtered_df['State'].map(state_name_map)
    # External GeoJSON for India states (used in featureidkey)
    geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    india_states = requests.get(geojson_url).json()
    
    if filtered_df.empty:
         st.warning("No data available for selected filters.")
    else:
    # Create Choropleth
        fig = go.Figure(data=go.Choropleth(
        geojson=india_states,
        featureidkey='properties.ST_NM',
        locations=filtered_df['State'],
        z=filtered_df['Registered_Users'],
        colorscale=px.colors.sequential.Purples,
        zmin=10000,  
        zmax=1000000,
        marker_line_color='#5F259F',
        colorbar_title="Users"
        
    ))

    fig.update_geos(fitbounds="locations", 
    visible=False,
    projection=dict(
        type='conic conformal',
        parallels=[12.472944444, 35.172805555556],
        rotation={'lat': 24, 'lon': 80}
    ),
    lonaxis={'range': [68, 98]},
    lataxis={'range': [6, 38]}
    )

    fig.update_layout(
    title=dict(
        text="Registered PhonePe Users by State",
        xanchor='center',
        x=0.5,
        yref='paper',
        yanchor='bottom',
        y=1,
        pad={'b': 10}
    ),
    margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
    height=550, 
    width=550
    )

    # Display in Streamlit
    st.subheader(f"📍 Registered Users by State - {selected_year} Q{selected_quarter}")
    st.plotly_chart(fig, use_container_width=True)

    # Clean year column
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["State"] = df["State"].replace(state_name_map)

    selected_state = st.selectbox("Select State", sorted(df["State"].unique()))
    filtered_df = df[df["State"] == selected_state]
    # Group to avoid collapsing
    grouped_df = filtered_df.groupby("Year")["Registered_Users"].sum().reset_index()
   
    # Plot
    fig = px.line(
    grouped_df,
    x="Year",
    y="Registered_Users",
    markers=True,
    title=f"Registered Users Trend for {selected_state}",
    labels={"Year": "Year", "Registered_Users": "Registered Users"}
    )

    fig.update_layout(
    yaxis_title="Registered Users (in Millions)",
    yaxis=dict(
        tickformat=".2s",  # Format like 1M, 500K
        range=[0, grouped_df["Registered_Users"].max() * 1.1],  # Optional: set max range
     )
    )
    st.subheader(f"📈 Yearly Registration Trend in {selected_state}")
    st.plotly_chart(fig, use_container_width=True) 

    # Dropdown Filters Year and Quarter
    col1, col2 = st.columns(2)
    with col1:
        current_year = st.selectbox("Select Year", years,index=len(years)-1)
    with col2:
        current_quarter = st.selectbox("Select Quarter",  quarters,index=len(quarters)-1)


    # Logic to compute previous quarter and year
    if current_quarter == 1:
        prev_quarter = 4
        prev_year = current_year - 1
    else:
        prev_quarter = current_quarter - 1
        prev_year = current_year
    # Filter data
    current_df = df[(df['Year'] == current_year) & (df['Quarter'] == current_quarter)]
    prev_df = df[(df['Year'] == prev_year) & (df['Quarter'] == prev_quarter)]
    # Group by District
    current_group = current_df.groupby('District')['Registered_Users'].sum().reset_index()
    prev_group = prev_df.groupby('District')['Registered_Users'].sum().reset_index()
    # Rename columns
    current_group.rename(columns={'Registered_Users': 'Current_Users'}, inplace=True)
    prev_group.rename(columns={'Registered_Users': 'Previous_Users'}, inplace=True)
    # Merge
    merged = pd.merge(current_group, prev_group, on='District', how='outer').fillna(0)
    # Compute Growth
    merged['Growth'] = merged['Current_Users'] - merged['Previous_Users']
    merged['Growth_Percent'] = merged.apply(
        lambda row: (row['Growth'] / row['Previous_Users'] * 100) if row['Previous_Users'] > 0 else 0,
        axis=1
    )
    # Format district names
    merged['District'] = merged['District'].str.upper()
    # Top 5
    top5 = merged.sort_values(by='Growth', ascending=False).head(5).reset_index(drop=True)
    # Bottom 5
    bottom5 = merged.sort_values(by='Growth', ascending=True).head(5).reset_index(drop=True)
    # Show side-by-side tables
    
    st.subheader(f"🔼 Top 5 Growing Districts ({prev_year} Q{prev_quarter} → {current_year} Q{current_quarter})")
    st.dataframe(top5[['District', 'Previous_Users', 'Current_Users', 'Growth', 'Growth_Percent']])
    
    st.subheader(f"🔽 Bottom 5 Shrinking Districts ({prev_year} Q{prev_quarter} → {current_year} Q{current_quarter})")
    st.dataframe(bottom5[['District', 'Previous_Users', 'Current_Users', 'Growth', 'Growth_Percent']])
    
    

  
elif page == "analytics":
    st.write("Analytics section here.")
   
    df = pd.read_csv("C:/Users/Jeeva/Documents/PhonePepluse/Phonepe_Pluse_Analyzer/Data_Extract/Aggregated_transaction.csv")
    # UI for filtering
    states = sorted(df['State'].unique()) 
    col1, col2 = st.columns(2)
    with col1:
        selected_states = st.selectbox("Select State", states)
    # Filter the dataframe
    filtered_df = df[(df['Year'] == selected_states) ]
    
    # If Registered_Users contains commas, remove them and convert to int
    filtered_df["State"] = df["State"].astype(str).str.replace(",", "").astype(int) 
     
    filtered_df['State'] = filtered_df['State'].map(state_name_map) 

elif page == "reports":
    st.write("Reports section here.")
elif page == "settings":
    st.write("Settings page here.")

 
