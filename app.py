import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Bug Tracker",
    page_icon="🐞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- SESSION STATE ----------------
if "bugs" not in st.session_state:
    st.session_state.bugs = []

# ---------------- SIDEBAR NAVIGATION ----------------
st.sidebar.title("Bug Tracker")
menu = st.sidebar.radio("Navigation", ["View Bugs", "Analytics"])

# ---------------- ADD BUG FORM (Always Visible) ----------------
st.header("Add New Bug")

with st.form(key="add_bug_form"):
    title = st.text_input("Bug Title")
    description = st.text_area("Description")
    severity = st.selectbox("Severity", ["Low", "Medium", "High"])
    status = st.selectbox("Status", ["Open", "In Progress", "Fixed"])
    submit = st.form_submit_button("Add Bug")

    if submit:
        if title and description:
            st.session_state.bugs.append({
                "Title": title,
                "Description": description,
                "Severity": severity,
                "Status": status
            })
            st.success(f"Bug '{title}' added successfully!")
        else:
            st.warning("Please fill all fields.")

st.markdown("---")

# ---------------- VIEW BUGS ----------------
if menu == "View Bugs":
    st.header("Bug List")

    if st.session_state.bugs:
        df = pd.DataFrame(st.session_state.bugs)

        # Filters
        col1, col2, col3 = st.columns([2,2,1])
        with col1:
            severity_filter = st.selectbox(
                "Filter by Severity", ["All", "Low", "Medium", "High"], key="filter_severity"
            )
        with col2:
            status_filter = st.selectbox(
                "Filter by Status", ["All", "Open", "In Progress", "Fixed"], key="filter_status"
            )
        with col3:
            view_mode = st.radio("View Mode", ["List", "Table"], horizontal=True)

        # Apply filters
        filtered_bugs = []
        for i, bug in enumerate(st.session_state.bugs):
            if (severity_filter == "All" or bug["Severity"] == severity_filter) and \
               (status_filter == "All" or bug["Status"] == status_filter):
                filtered_bugs.append((i, bug))

        if view_mode == "List":
            for i, bug in filtered_bugs:
                st.markdown(f"**{i+1}. {bug['Title']}**")
                st.write(f"Description: {bug['Description']}")
                st.write(f"Severity: {bug['Severity']}")

                # Editable Status
                new_status = st.selectbox(
                    "Status",
                    ["Open", "In Progress", "Fixed"],
                    index=["Open", "In Progress", "Fixed"].index(bug["Status"]),
                    key=f"status_{i}"
                )

                if new_status != bug["Status"]:
                    st.session_state.bugs[i]["Status"] = new_status
                    st.success(f"✅ Status updated to {new_status} for '{bug['Title']}'")

                st.markdown("---")
        else:  # Table view
            table_df = pd.DataFrame([bug for i, bug in filtered_bugs])
            st.dataframe(table_df, use_container_width=True)

    else:
        st.info("No bugs added yet.")


# ---------------- ANALYTICS ----------------
elif menu == "Analytics":
    st.header("Bug Analytics")

    if st.session_state.bugs:
        df = pd.DataFrame(st.session_state.bugs)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Bugs", len(df))
        with col2:
            st.metric("Open Bugs", len(df[df["Status"] == "Open"]))

        st.subheader("Severity Distribution")
        st.bar_chart(df["Severity"].value_counts())

        st.subheader("Status Distribution")
        st.bar_chart(df["Status"].value_counts())
    else:
        st.info("Add some bugs to see analytics.")



