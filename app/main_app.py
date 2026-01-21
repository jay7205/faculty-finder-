import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api import FacultyAPI

st.set_page_config(
    page_title="Faculty Finder",
    layout="wide"
)

api = FacultyAPI()

st.title("Faculty Directory Search")
st.markdown("Explore faculty profiles, research specializations, and contact information.")

search_query = st.text_input("Search by Name, Specialization, or Biography", "")

if search_query:
    results = api.search(search_query)
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
    total, data = api.get_all(page=1, limit=9)
    st.write(f"Displaying {len(data)} of {total} faculty members")
    
    for i in range(0, len(data), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(data):
                faculty = data[i + j]
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
