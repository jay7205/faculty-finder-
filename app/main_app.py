import streamlit as st
import sys
import os
import pandas as pd
import json
import sqlite3
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import DatabaseManager
from src.config import DATABASE_PATH

st.set_page_config(
    page_title="Faculty Finder",
    layout="wide"
)

db = DatabaseManager(DATABASE_PATH)

def get_export_data():
    return db.get_all_faculty()

st.sidebar.title("Data Exports")
st.sidebar.info("Download the faculty dataset in your preferred format for further analysis.")

all_data = get_export_data()
df = pd.DataFrame(all_data)

csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="Download CSV",
    data=csv,
    file_name=f"faculty_data_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv",
)

json_data = json.dumps(all_data, indent=2, default=str).encode('utf-8')
st.sidebar.download_button(
    label="Download JSON",
    data=json_data,
    file_name=f"faculty_data_{datetime.now().strftime('%Y%m%d')}.json",
    mime="application/json",
)

st.sidebar.divider()
st.sidebar.write("**Direct Database Access**")
st.sidebar.write("Collaborators can access the raw SQLite database file at:")
st.sidebar.code("database/faculty.db")

st.title("Faculty Directory Search")
st.markdown("Explore faculty profiles, research specializations, and contact information.")

search_query = st.text_input("Search by Name, Specialization, or Biography", "")

if search_query:
    conn = db.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    q = f"%{search_query}%"
    cursor.execute("""
        SELECT * FROM faculty 
        WHERE name LIKE ? 
        OR specialization LIKE ? 
        OR biography LIKE ?
    """, (q, q, q))
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    st.write(f"Found {len(results)} matching profiles")
    
    for i in range(0, len(results), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(results):
                faculty = results[i + j]
                with cols[j]:
                    with st.container(border=True):
                        if faculty['image_url'] != "Not Provided":
                            st.image(faculty['image_url'], use_container_width=True)
                        
                        st.subheader(faculty['name'])
                        st.info(f"**Specialization:** {faculty['specialization']}")
                        st.write(f"**Email:** {faculty['email']}")
                        
                        with st.expander("View Full Profile"):
                            st.write(f"**Education:** {faculty['education']}")
                            st.write(f"**Biography:** {faculty['biography']}")
                            st.write(f"**Teaching:** {faculty['teaching']}")
                            st.write(f"**Publications:** {faculty['publications']}")
else:
    display_data = all_data[:12]
    st.write(f"Displaying {len(display_data)} of {len(all_data)} faculty members")
    
    for i in range(0, len(display_data), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(display_data):
                faculty = display_data[i + j]
                with cols[j]:
                    with st.container(border=True):
                        if faculty['image_url'] != "Not Provided":
                            st.image(faculty['image_url'], use_container_width=True)
                        
                        st.subheader(faculty['name'])
                        st.info(f"**Specialization:** {faculty['specialization']}")
                        st.write(f"**Email:** {faculty['email']}")
                        
                        with st.expander("View Full Profile"):
                            st.write(f"**Education:** {faculty['education']}")
                            st.write(f"**Biography:** {faculty['biography']}")
                            st.write(f"**Teaching:** {faculty['teaching']}")
                            st.write(f"**Publications:** {faculty['publications']}")
