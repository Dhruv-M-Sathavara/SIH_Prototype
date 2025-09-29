import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# -----------------------------
# CHATBOT RESPONSE GENERATOR
# -----------------------------
def generate_bot_response(user_input, df, float_summary):
    """Generate chatbot responses based on user input"""
    user_input_lower = user_input.lower()
    
    # Specific query for salinity profiles near equator in March 2013
    if "salinity profiles" in user_input_lower and "equator" in user_input_lower and "march 2013" in user_input_lower:
        march_2013 = (df['time'].dt.year == 2013) & (df['time'].dt.month == 3)
        near_equator = abs(df['latitude']) < 5
        filtered = df[march_2013 & near_equator]
        
        if not filtered.empty:
            avg_sal = filtered['salinity'].mean()
            max_sal = filtered['salinity'].max()
            min_sal = filtered['salinity'].min()
            num_profiles = filtered['profile_index'].nunique()
            response = f"""
💧 **Salinity Profiles Near Equator in March 2013:**
• Number of Profiles: {num_profiles}
• Average Salinity: {avg_sal:.3f} PSU
• Range: {min_sal:.3f} to {max_sal:.3f} PSU
• Data based on random sample simulations.
Showing salinity analysis visualization below for reference.
            """
            st.session_state.show_salinity = True
        else:
            response = "In 2013, salinity data was collected near the equator by floats 2901616 and 2901630."
        return response
    
    # Temperature queries
    if "temperature" in user_input_lower:
        if "highest" in user_input_lower or "warmest" in user_input_lower:
            max_temp_idx = df['temperature'].idxmax()
            max_temp_data = df.loc[max_temp_idx]
            return f" The highest temperature recorded is {max_temp_data['temperature']:.2f}°C by Float {max_temp_data['float_id']} at {max_temp_data['pressure']:.0f}m depth on {max_temp_data['time'].strftime('%Y-%m-%d') if pd.notna(max_temp_data['time']) else 'unknown date'}."
        
        elif "lowest" in user_input_lower or "coldest" in user_input_lower:
            min_temp_idx = df['temperature'].idxmin()
            min_temp_data = df.loc[min_temp_idx]
<<<<<<< HEAD
            return f"🧊 The lowest temperature recorded is {min_temp_data['temperature']:.2f}°C by Float {min_temp_data['float_id']} at {min_temp_data['pressure']:.0f}m depth on {min_temp_data['time'].strftime('%Y-%m-%d') if pd.notna(max_temp_data['time']) else 'unknown date'}."
        
        elif "average" in user_input_lower or "mean" in user_input_lower:
            avg_temp = df['temperature'].mean()
            return f"📊 The average temperature across all measurements is {avg_temp:.2f}°C. The temperature ranges from {df['temperature'].min():.1f}°C to {df['temperature'].max():.1f}°C."
=======
            return f"🧊 The lowest temperature recorded is **{min_temp_data['temperature']:.2f}°C** by Float {min_temp_data['float_id']} at {min_temp_data['pressure']:.0f}m depth on {min_temp_data['time'].strftime('%Y-%m-%d') if pd.notna(max_temp_data['time']) else 'unknown date'}."
        
        elif "average" in user_input_lower or "mean" in user_input_lower:
            avg_temp = df['temperature'].mean()
            return f"📊 The average temperature across all measurements is **{avg_temp:.2f}°C. The temperature ranges from {df['temperature'].min():.1f}°C to {df['temperature'].max():.1f}°C."
>>>>>>> 6a964751dbde897a72900d9d4b073aaf664b7ef2
    
    # Depth/Pressure queries
    elif "depth" in user_input_lower or "deepest" in user_input_lower:
        max_depth_idx = df['pressure'].idxmax()
        max_depth_data = df.loc[max_depth_idx]
        return f"🏊‍♂️ The deepest measurement was taken at {max_depth_data['pressure']:.0f}m by Float {max_depth_data['float_id']} with a temperature of {max_depth_data['temperature']:.1f}°C and salinity of {max_depth_data['salinity']:.2f} PSU."
    
    # Float-specific queries
    elif "float" in user_input_lower and any(str(fid) in user_input for fid in float_summary['float_id']):
        mentioned_floats = [str(fid) for fid in float_summary['float_id'] if str(fid) in user_input]
        if mentioned_floats:
            float_id = mentioned_floats[0]
            float_data = float_summary[float_summary['float_id'] == float_id].iloc[0]
            float_profiles = df[df['float_id'] == float_id]
            
            return f"""
📊 **Float {float_id} Summary:**
• **Location:** {float_data['lat_mean']:.2f}°N, {float_data['lon_mean']:.2f}°E
• **Total Profiles:** {float_data['total_profiles']:.0f}
• **Average Temperature:** {float_data['temp_mean']:.2f}°C
• **Average Salinity:** {float_data['sal_mean']:.3f} PSU
• **Maximum Depth:** {float_data['pressure_max']:.0f}m
• **Active Period:** {float_data['deployment_days']:.0f} days
• **Temperature Range:** {float_profiles['temperature'].min():.1f}°C to {float_profiles['temperature'].max():.1f}°C
            """
    
    # Salinity queries
    elif "salinity" in user_input_lower:
        if "highest" in user_input_lower:
            max_sal_idx = df['salinity'].idxmax()
            max_sal_data = df.loc[max_sal_idx]
            return f"💧 The highest salinity recorded is {max_sal_data['salinity']:.3f} PSU by Float {max_sal_data['float_id']} at {max_sal_data['pressure']:.0f}m depth."
        elif "average" in user_input_lower:
            avg_sal = df['salinity'].mean()
            return f"💧 The average salinity across all measurements is {avg_sal:.3f} PSU, ranging from {df['salinity'].min():.3f} to {df['salinity'].max():.3f} PSU."
    
    # Fleet overview queries
    elif "overview" in user_input_lower or "summary" in user_input_lower or "fleet" in user_input_lower:
        most_active = float_summary.loc[float_summary['total_profiles'].idxmax()]
        return f"""
🚢 **Fleet Overview:**
• **Total Active Floats:** {len(float_summary)}
• **Total Profiles Collected:** {df['profile_index'].nunique():,}
• **Most Active Float:** {most_active['float_id']} ({most_active['total_profiles']:.0f} profiles)
• **Global Temperature Range:** {df['temperature'].min():.1f}°C to {df['temperature'].max():.1f}°C
• **Maximum Depth Reached:** {df['pressure'].max():.0f}m
• **Average Deployment Duration:** {float_summary['deployment_days'].mean():.0f} days
        """
    
    # Compare queries
    elif "compare" in user_input_lower:
        top_floats = float_summary.nlargest(2, 'total_profiles')
        float1, float2 = top_floats.iloc[0], top_floats.iloc[1]
        
        return f"""
🔄 **Comparison - Top 2 Most Active Floats:**

**Float {float1['float_id']}:**
• Profiles: {float1['total_profiles']:.0f}
• Avg Temp: {float1['temp_mean']:.2f}°C
• Max Depth: {float1['pressure_max']:.0f}m

**Float {float2['float_id']}:**
• Profiles: {float2['total_profiles']:.0f}
• Avg Temp: {float2['temp_mean']:.2f}°C
• Max Depth: {float2['pressure_max']:.0f}m
        """
    
    # Default response
    else:
        return f"""
🤖 Here's a quick look at the Argo float data:
• **Total Floats:** {len(float_summary)}
• **Average Temperature:** {df['temperature'].mean():.2f}°C
• **Average Salinity:** {df['salinity'].mean():.3f} PSU
Try asking something specific like "Show me salinity profiles near the equator in March 2013?" or select a sample question!
        """

# -----------------------------
# SAMPLE DATA GENERATION
# -----------------------------
@st.cache_data
def generate_sample_data():
    """Generate sample data since database is local"""
    np.random.seed(42)
    float_ids = [2902123, 2902124, 2902125, 2902126, 2902127]
    data = []
    
    for fid in float_ids:
        num_profiles = np.random.randint(5, 20)
        for profile in range(1, num_profiles + 1):
            base_time = pd.Timestamp('2012-01-01') + pd.Timedelta(days=np.random.randint(0, 365 * 3))
            lat = np.random.uniform(-15, 15)
            lon = np.random.uniform(-180, 180)
            num_depths = np.random.randint(50, 150)
            for depth_idx in range(num_depths):
                pressure = np.random.uniform(0, 2000)
                temperature = 25 - (pressure / 100) + np.random.normal(0, 2)
                salinity = 35 + np.random.normal(0, 1)
                time = base_time + pd.Timedelta(hours=np.random.randint(0, 24))
                data.append([fid, profile, lat, lon, time, pressure, temperature, salinity])
    
    df = pd.DataFrame(
        data,
        columns=['float_id', 'profile_index', 'latitude', 'longitude', 'time', 'pressure', 'temperature', 'salinity']
    )
    df['time'] = pd.to_datetime(df['time'])
    df = df.sort_values(by=['float_id', 'time', 'pressure'])
    return df

# Load sample data
df = generate_sample_data()

if df.empty:
    st.error("No sample data generated.")
    st.stop()

# -----------------------------
# DATA PROCESSING
# -----------------------------
float_summary = df.groupby("float_id").agg({
    "latitude": ["mean", "std"],
    "longitude": ["mean", "std"],
    "temperature": ["mean", "min", "max", "std"],
    "salinity": ["mean", "min", "max", "std"],
    "pressure": ["max", "mean"],
    "profile_index": "nunique",
    "time": ["min", "max"]
}).reset_index()

float_summary.columns = [
    "float_id", "lat_mean", "lat_std", "lon_mean", "lon_std",
    "temp_mean", "temp_min", "temp_max", "temp_std",
    "sal_mean", "sal_min", "sal_max", "sal_std",
    "pressure_max", "pressure_mean", "total_profiles",
    "first_profile", "last_profile"
]

float_summary["deployment_days"] = (
    float_summary["last_profile"] - float_summary["first_profile"]
).dt.days

# Page configuration
st.set_page_config(
    page_title="🤖 NMDIS Argo Chatbot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Original CSS
st.markdown("""
<style>
    /* Main chatbot container styling */
    .chatbot-container {
        color:grey;
        padding: 2px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    .chat-header {
        text-align: center;
        color: white;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .chat-description {
        text-align: center;
        color: rgba(255,255,255,0.9);
        font-size: 16px;
        margin-bottom: 25px;
        line-height: 1.6;
    }
    
    /* Chat message styling */
    .user-message {
        padding: 15px;
        border-radius: 15px 15px 5px 15px;
        margin: 10px 0;
        
    }
    
    .bot-message {
        
        padding: 15px;
        border-radius: 15px 15px 15px 5px;
        margin: 10px 0;
        
    }
    
    .quick-actions {
        background: rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
    }
    
    .metric-highlight {
        background: rgba(255,255,255,0.2);
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        text-align: center;
        color: white;
    }
    
    /* Sidebar styling */
    .sidebar-section {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #007bff;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER SECTION
# -----------------------------
st.title("🌊 FloatChat Dashboard")
st.markdown("*Explore oceanographic data from autonomous profiling floats*")
st.info("""
⚠️ **Prototype Notice**:  
This dashboard currently runs on **sample data** because the real Argo dataset is very large and cannot be hosted on a free server.  

The prototype is built using **real data from Argo floats**, as demonstrated in the YouTube and GitHub repository.  

""")
# -----------------------------
# MAIN CHATBOT INTERFACE
# -----------------------------
st.markdown('<div class="chatbot-container">', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="chat-header">💬 Ask Me Anything About Argo Floats!</div>', unsafe_allow_html=True)
    st.markdown('''
        <div class="chat-description">
            I can help you analyze oceanographic data, find specific float information, 
            generate visualizations, and answer questions about temperature, salinity, and depth profiles.
        </div>
    ''', unsafe_allow_html=True)
    
    # Sample questions
    st.markdown("### ❓ Sample Questions")
    sample_questions = [
        "Show me salinity profiles near the equator in March 2013?",
        "What's the highest temperature recorded?",
        "Give me a fleet overview",
        "What's the average salinity?",
        "Show temperature trends for float 2902123"
    ]
    for q in sample_questions:
        if st.button(q, key=f"sample_{q}"):
            st.session_state.selected_question = q
    
    # Chat interface
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    user_input = st.text_input(
        "🗨️ Your Question:",
        placeholder="Ask me anything about the Argo float data...",
        key="chat_input",
        help="Type your question about oceanographic data, floats, or analysis requests"
    )
    
    if "selected_question" in st.session_state:
        user_input = st.session_state.selected_question
        del st.session_state.selected_question
    
    col_send, col_clear = st.columns([1, 1])
    with col_send:
        send_button = st.button("Ask", type="primary", use_container_width=True)
    with col_clear:
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    # Process chat input
    if (send_button and user_input) or user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        bot_response = generate_bot_response(user_input, df, float_summary)
        st.session_state.chat_history.append({"role": "bot", "content": bot_response})

    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### 💬 Chat History")
        for i, message in enumerate(reversed(st.session_state.chat_history[-10:])):
            if message["role"] == "user":
                st.markdown(f'''
                    <div class="user-message">
                        <strong>🧑‍💼 You:</strong><br>
                        {message["content"]}
                    </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                    <div class="bot-message">
                        <strong>🤖 Assistant:</strong><br>
                        {message["content"]}
                    </div>
                ''', unsafe_allow_html=True)

with col2:
    st.markdown("### 🎯 Quick Actions")
    st.markdown('<div class="quick-actions">', unsafe_allow_html=True)
    
    if st.button("📊 Fleet Overview", use_container_width=True):
        overview_text = f"""
        **Fleet Status:**
        • Active Floats: {len(float_summary)}
        • Total Profiles: {df['profile_index'].nunique():,}
        • Temperature Range: {df['temperature'].min():.1f}°C to {df['temperature'].max():.1f}°C
        • Max Depth Recorded: {df['pressure'].max():.0f}m
        """
        st.markdown(overview_text)
    
    if st.button("🌡️ Temperature Analysis", use_container_width=True):
        temp_stats = f"""
        **Temperature Insights:**
        • Global Average: {df['temperature'].mean():.2f}°C
        • Warmest Location: {df.loc[df['temperature'].idxmax(), 'float_id']} ({df['temperature'].max():.1f}°C)
        • Coolest Location: {df.loc[df['temperature'].idxmin(), 'float_id']} ({df['temperature'].min():.1f}°C)
        """
        st.markdown(temp_stats)
    
    if st.button("Salinity", use_container_width=True):
        sal_stats = f"""
        **Salinity Insights:**
        • Global Average: {df['salinity'].mean():.3f} PSU
        • Highest Salinity: {df['salinity'].max():.3f} PSU
        • Lowest Salinity: {df['salinity'].min():.3f} PSU
        """
        st.markdown(sal_stats)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### 📈 Live Statistics")
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.markdown(f'''
            <div class="metric-highlight">
                <div style="font-size: 24px; font-weight: bold;">{len(float_summary)}</div>
                <div>Active Floats</div>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown(f'''
            <div class="metric-highlight">
                <div style="font-size: 24px; font-weight: bold;">{df['temperature'].mean():.1f}°C</div>
                <div>Avg Temperature</div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col_stat2:
        st.markdown(f'''
            <div class="metric-highlight">
                <div style="font-size: 24px; font-weight: bold;">{df['profile_index'].nunique():,}</div>
                <div>Total Profiles</div>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown(f'''
            <div class="metric-highlight">
                <div style="font-size: 24px; font-weight: bold;">{df['pressure'].max():.0f}m</div>
                <div>Max Depth</div>
            </div>
        ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.markdown("""
    <div style='background: #739EC9; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h2 style='color: white; text-align: center; margin: 0;'> FloatChat</h2>
    </div>
""", unsafe_allow_html=True)

with st.sidebar.expander("📊 Available Data", expanded=True):
    st.markdown(f"""
    **Dataset Overview:**
    - **{len(float_summary)}** Active Floats
    - **{df['profile_index'].nunique():,}** Profiles
    - **{len(df):,}** Total Measurements
    - **Date Range:** {df['time'].min().strftime('%Y-%m-%d') if not df['time'].isna().all() else 'N/A'} to {df['time'].max().strftime('%Y-%m-%d') if not df['time'].isna().all() else 'N/A'}
    """)

with st.sidebar.expander("🎯 Focus on Specific Float", expanded=False):
    selected_float = st.selectbox(
        "Select Float for Detailed Analysis:",
        ["All Floats"] + list(float_summary["float_id"].unique()),
        help="Choose a specific float for detailed analysis"
    )
    if selected_float != "All Floats":
        float_data = float_summary[float_summary["float_id"] == selected_float].iloc[0]
        st.markdown(f"""
        **Float {selected_float} Summary:**
        - **Profiles:** {float_data['total_profiles']:.0f}
        - **Avg Temp:** {float_data['temp_mean']:.1f}°C
        - **Max Depth:** {float_data['pressure_max']:.0f}m
        - **Active Days:** {float_data['deployment_days']:.0f}
        """)

with st.sidebar.expander("📈 Quick Visualizations"):
    if st.button("🗺️ Show Float Map"):
        st.session_state.show_map = True
    if st.button("📊 Temperature Profiles"):
        st.session_state.show_temp_profiles = True
    if st.button("💧 Salinity Analysis"):
        st.session_state.show_salinity = True

with st.sidebar.expander("💾 Data Export"):
    export_format = st.selectbox("Export Format:", ["CSV", "JSON"])
    if st.button("📤 Export Current Data"):
        if export_format == "CSV":
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download CSV",
                csv,
                f"argo_data_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )

# -----------------------------
# DYNAMIC VISUALIZATIONS
# -----------------------------
show_visualizations = st.container()

with show_visualizations:
    if "show_map" in st.session_state and st.session_state.show_map:
        st.subheader("🗺️ Float Deployment Map")
        fig_map = px.scatter_mapbox(
            float_summary,
            lat="lat_mean",
            lon="lon_mean",
            hover_name="float_id",
            hover_data={"temp_mean": ":.2f", "total_profiles": True},
            color="temp_mean",
            size="total_profiles",
            size_max=20,
            zoom=3,
            mapbox_style="carto-positron",
            title="Global Argo Float Locations"
        )
        fig_map.update_layout(height=500)
        st.plotly_chart(fig_map, use_container_width=True)
        if st.button("Hide Map"):
            st.session_state.show_map = False
            st.rerun()

    if "show_temp_profiles" in st.session_state and st.session_state.show_temp_profiles:
        st.subheader("🌡️ Temperature Depth Profiles")
        display_df = df[df["float_id"] == selected_float] if selected_float != "All Floats" else df.sample(min(1000, len(df)))
        fig_temp = px.scatter(
            display_df,
            x="temperature",
            y="pressure",
            color="float_id" if selected_float == "All Floats" else "time",
            title=f"Temperature vs Depth - {selected_float}",
            labels={"temperature": "Temperature (°C)", "pressure": "Depth (m)"}
        )
        fig_temp.update_yaxes(autorange="reversed")
        fig_temp.update_layout(height=500)
        st.plotly_chart(fig_temp, use_container_width=True)
        if st.button("Hide Temperature Profiles"):
            st.session_state.show_temp_profiles = False
            st.rerun()

    if "show_salinity" in st.session_state and st.session_state.show_salinity:
        st.subheader("💧 Salinity")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Salinity vs Depth Profiles**")
            display_df = df[df["float_id"] == selected_float] if selected_float != "All Floats" else df.sample(min(1000, len(df)))
            fig_salinity = px.scatter(
                display_df,
                x="salinity",
                y="pressure",
                color="float_id" if selected_float == "All Floats" else "time",
                title=f"Salinity vs Depth - {selected_float}",
                labels={"salinity": "Salinity (PSU)", "pressure": "Depth (m)"}
            )
            fig_salinity.update_yaxes(autorange="reversed")
            fig_salinity.update_layout(height=400)
            st.plotly_chart(fig_salinity, use_container_width=True)
        
        with col2:
            st.markdown("**Salinity Distribution**")
            fig_sal_hist = px.histogram(
                df,
                x="salinity",
                nbins=30,
                title="Salinity Distribution",
                labels={"salinity": "Salinity (PSU)", "count": "Frequency"}
            )
            fig_sal_hist.update_layout(height=400)
            st.plotly_chart(fig_sal_hist, use_container_width=True)
        
        st.markdown("**📊 Salinity Statistics:**")
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        with col_stat1:
            st.metric("Average", f"{df['salinity'].mean():.3f} PSU")
        with col_stat2:
            st.metric("Minimum", f"{df['salinity'].min():.3f} PSU")
        with col_stat3:
            st.metric("Maximum", f"{df['salinity'].max():.3f} PSU")
        with col_stat4:
            st.metric("Std Dev", f"{df['salinity'].std():.3f} PSU")
        
        if st.button("Hide Salinity Analysis"):
            st.session_state.show_salinity = False
            st.rerun()

# Footer
st.markdown("---")
