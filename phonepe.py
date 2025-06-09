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
    st.title("1.User Registration Analysis")
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
    st.write("Track registration trends over time by year for the selected state.")
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
    st.write("Discover the top 5 districts codes based on registration volume, growth, and growth percentage.")
    st.dataframe(top5[['District', 'Previous_Users', 'Current_Users', 'Growth', 'Growth_Percent']])
    
    st.subheader(f"🔽 Bottom 5 Shrinking Districts ({prev_year} Q{prev_quarter} → {current_year} Q{current_quarter})")
    st.write("Discover the Bottom  5 districts codes based on registration volume, growth, and growth percentage.")
    st.dataframe(bottom5[['District', 'Previous_Users', 'Current_Users', 'Growth', 'Growth_Percent']])
     
elif page == "analytics":
    st.subheader("2.Transaction Performance Analysis Across Indian States and Districts")
   
    df = pd.read_csv("C:/Users/Jeeva/Documents/PhonePepluse/Phonepe_Pluse_Analyzer/Data_Extract/Map_transaction.csv")
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["State"] = df["State"].replace(state_name_map)
    df['District'] = df['District'].str.upper()

    selected_state = st.selectbox("Select State", sorted(df["State"].unique()))
    filtered_df = df[df["State"] == selected_state] 
    district_summary = (
    filtered_df.groupby("District")[["Transaction_amount", "Transaction_count"]]
    .sum()
    .reset_index()
    .sort_values(by="Transaction_amount", ascending=False)
    .head(10)
    )

    fig = px.bar(
        district_summary,
        x="District",
        y="Transaction_amount",
        text="Transaction_amount",
         
        title=f"Top 10 Districts in {selected_state}",
        labels={"Transaction_amount": "Transaction Amount (₹)", "District": "District"},
        color_discrete_sequence=["#5F259F"]
     )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(
        xaxis_title="District",
        yaxis_title="Transaction Amount",
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        plot_bgcolor="#f9f9f9"
    )
    st.write(f"Top Performing  Districts in PhonePe Transaction {selected_state}")
    st.plotly_chart(fig, use_container_width=True)

    state_df = df[df["State"] == selected_state]
    yearly_growth = state_df.groupby("Year")[["Transaction_amount", "Transaction_count"]].sum().reset_index()
   
    st.subheader(f"📈 Growth Trend of Transaction Amount in {selected_state}")

    fig2 = px.line(
        yearly_growth,
        x="Year",
        y="Transaction_amount",
        markers=True,
        text="Transaction_amount",
        title=f"Yearly Transaction Growth in {selected_state}",
        labels={"Transaction_amount": "Transaction Amount (₹)", "Year": "Year"},
    )
    fig2.update_traces(
        text=df["Transaction_amount"],
        texttemplate="%{text:.2s}",    # ✅ SI format (like 1.2B)
        textposition="top center",
        line=dict(color="royalblue", width=3),
        marker=dict(color="royalblue", size=8))
   
    fig2.update_layout(
        yaxis_title="Transaction Amount (₹)",
        xaxis_title="Year",
        plot_bgcolor="#f9f9f9",
        
    )

    st.plotly_chart(fig2, use_container_width=True) 


    st.subheader("3. Device Dominance and User Engagement Analysis")
    df1 = pd.read_csv("C:/Users/Jeeva/Documents/PhonePepluse/Phonepe_Pluse_Analyzer/Data_Extract/Aggregated_user.csv")
    df1["Year"] = pd.to_numeric(df1["Year"], errors="coerce")
    df1["State"] = df1["State"].replace(state_name_map)
     
    df1['Brand'] = df1['Brand'].str.upper()

    brand_summary = df1.groupby('Brand')['Transaction_count'].sum().reset_index()
    top_5_brands = brand_summary.sort_values(by='Transaction_count', ascending=False).head(10)
 
    fig3= px.bar(
        top_5_brands,
        x='Brand',
        y='Transaction_count',
        title='Top 10 Device Brands by Transaction Count',
        color='Brand',
        text='Transaction_count'
    )
    
    fig3.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig3.update_layout(xaxis_title='Device Brand', yaxis_title='Total Transaction Count')

    st.write(f"Top 10 Device Brands by Transaction Count on {selected_state}")
    st.plotly_chart(fig3, use_container_width=True) 

    # Ensure percentage column is numeric
    df1['Transaction_percentage'] = pd.to_numeric(df1['Transaction_percentage'], errors='coerce')

    # Group by Brand and calculate the average transaction percentage
    avg_percentage_by_brand = df1.groupby('Brand')['Transaction_percentage'].mean().reset_index()

    # Sort to get the top 5 brands by average percentage
    top_5_percentage_brands = avg_percentage_by_brand.sort_values(by='Transaction_percentage', ascending=False).head(5)

    # Display the result
   

    # Optional: Visualize as bar chart
    fig4 = px.bar(
        top_5_percentage_brands,
        x='Brand',
        y='Transaction_percentage',
        title='Top 5 Device Brands by Average Transaction Percentage',
        color='Brand',
        text='Transaction_percentage'
    )
    fig4.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig4.update_layout(xaxis_title='Device Brand', yaxis_title='Avg. Transaction %')
    
    st.write(f"Top 5 Device Brands by Growth Percentage on {selected_state}")
    st.plotly_chart(fig4, use_container_width=True) 
    
elif page == "reports":
    st.subheader("4.Decoding Transaction Dynamics on PhonePe")
    df = pd.read_csv("C:/Users/Jeeva/Documents/PhonePepluse/Phonepe_Pluse_Analyzer/Data_Extract/Aggregated_transaction.csv")
     
    # Sort by State and Quater to ensure correct ordering
    df = df.sort_values(by=['State', 'Quater'])
    df["State"] = df["State"].replace(state_name_map)
    # Calculate growth rate (Quater-over-Quater) per state
    df['Growth_Rate (%)'] = df.groupby('State')['Transacion_amount'].pct_change() * 100
   
 
    # Optional: Filter to only latest quarter per state
    latest_quarter_df = df.sort_values("Quater").groupby("State").tail(1)

    # Select metric to visualize
    metric = st.selectbox("Select metric to visualize", ["Transacion_amount", "Growth_Rate (%)"])

    fig = px.bar(
        latest_quarter_df,
        x="State",
        y=metric,
        color=metric,
        text=metric,
        title=f"{metric} in Latest Quater",
        color_continuous_scale="Viridis"
    )
    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig.update_layout(yaxis_title=metric)
    st.write("Transaction Volume and Growth Rate by State and Quater")
    st.plotly_chart(fig, use_container_width=True)



    df = df.rename(columns={
    "Transacion_type": "Transaction_type",
    "Transacion_amount": "Transaction_amount",
    "Transacion_count": "Transaction_count",
    "Quater": "Quarter"  # Also fix this one
    })
    selected_state = st.selectbox("Select State", sorted(df["State"].unique()))
    filtered_df = df[df["State"] == selected_state]
    
    # PIE CHART — Transaction Amount Share by Type
    st.subheader(f"Transaction Amount Share in {selected_state} ")
    fig_pie = px.pie(
        filtered_df,
        names='Transaction_type',
        values='Transaction_amount',
        hole=0.4,
        title='Transaction Amount Distribution by Type'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    df1 = pd.read_csv("C:/Users/Jeeva/Documents/PhonePepluse/Phonepe_Pluse_Analyzer/Data_Extract/Top_insurance.csv")
    # Clean and prepare data
    df1["State"] = df1["State"].replace(state_name_map)
    df1["Transaction_Amount"] = pd.to_numeric(df1["Transaction_Amount"], errors='coerce')
    df1["Quarter"] = df1["Quarter"].astype(str)
    df1["Year_Quarter"] = df1["Year"].astype(str) + " Q" + df1["Quarter"]

    # Filters
    
    col1, col2 = st.columns(2)
    with col1:
        years = sorted(df1["Year"].unique(), reverse=True)
        selected_year = st.selectbox("Select Year", years)
    with col2:
        quarters = sorted(df1[df1["Year"] == selected_year]["Quarter"].unique(), key=int, reverse=True)
        selected_quarter = st.selectbox("Select Quarter", quarters)
    
    # Define current and previous period
    current_period = f"{selected_year} Q{selected_quarter}"
    if int(selected_quarter) > 1:
        previous_period = f"{selected_year} Q{int(selected_quarter) - 1}"
    else:
        previous_period = f"{selected_year - 1} Q4"

    # Filter data
    df_current = df1[df1["Year_Quarter"] == current_period].copy()
    df_previous = df1[df1["Year_Quarter"] == previous_period].copy()

    # Group and aggregate
    current_group = df_current.groupby("State")["Transaction_Amount"].sum().reset_index(name="Transaction_Amount")
    previous_group = df_previous.groupby("State")["Transaction_Amount"].sum().reset_index(name="Previous_Amount")

    # Merge and calculate
    summary_df = pd.merge(current_group, previous_group, on="State", how="left")

    total_amount = summary_df["Transaction_Amount"].sum()
    summary_df["Share %"] = (summary_df["Transaction_Amount"] / total_amount * 100).round(2)
    summary_df["Growth"] = (summary_df["Transaction_Amount"] - summary_df["Previous_Amount"]).fillna(0).round(2)
    summary_df["Growth %"] = ((summary_df["Growth"] / summary_df["Previous_Amount"]) * 100).replace([float("inf"), -float("inf")], 0).fillna(0).round(2)

    # Sort and rename
    summary_df = summary_df.sort_values(by="Transaction_Amount", ascending=False)
    summary_df.rename(columns={
        "Transaction_Amount": "Volume (₹)",
        "Previous_Amount": "Previous Volume (₹)"
    }, inplace=True)


    # Display in Streamlit
    st.subheader(f"📋 Insurance Transaction Summary by State - {current_period}")
    st.dataframe(summary_df.style.format({
        "Volume (₹)": lambda x: f"₹{x/1_000_000:.2f}M",
        "Previous Volume (₹)": lambda x: f"₹{x/1_000_000:.2f}M",
        "Share %": "{:.2f}%",
        "Growth": lambda x: f"₹{x/1_000_000:.2f}M",
        "Growth %": "{:.2f}%"
    }), use_container_width=True)
    
elif page == "settings":
    st.write("Settings page here.")

 
