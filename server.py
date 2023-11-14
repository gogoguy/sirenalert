import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Function to simulate live updates
def simulate_live_update():
    # Simulate fetching data from your JSON server
    data = pd.read_json("alerts.json")

    # Convert 'alertDate' to datetime
    data['alertDate'] = pd.to_datetime(data['alertDate'])

    return data

# Main Streamlit app
def main():
    # Sidebar for date range selectors
    st.sidebar.header("Date Range")
    start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-10-01"), key="start_date")
    end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2023-12-31"), key="end_date")

    with st.sidebar.expander("Alert Location"):
        location_options = pd.read_json("alerts.json")["data"].unique().tolist()
        # Add an "All" option to select all locations
        all_selected_loc = st.checkbox("Select All Locations", key="select_all_loc", value=True)

        if all_selected_loc:
            selected_locations = location_options
            st.multiselect("Select Locations", location_options)
        else:
            # Use multiselect to allow selecting multiple locations
            selected_locations = st.multiselect("Select Locations", location_options)


    with st.sidebar.expander("Alert Type"):
        alert_options = pd.read_json("alerts.json")["category_desc"].unique().tolist()
        # Add an "All" option to select all alerts
        all_selected_al = st.checkbox("Select All Alerts", key="select_all_al", value=True)

        if all_selected_al:
            selected_alerts = alert_options
            st.multiselect("Select Alert Types", alert_options)
        else:
            # Use multiselect to allow selecting multiple alerts
            selected_alerts = st.multiselect("Select Alert Types", alert_options)

    # Set the title dynamically based on selected filters
    title = "Alert Graphs"
    header_loc = ""
    header_al = ""
    if not all_selected_loc:
        header_loc += f"Locations: {', '.join(selected_locations)}"
    else:
        header_loc += "Locations: All"
    if not all_selected_al:
        header_al += f"\nAlert Types: {', '.join(selected_alerts)}"
    else:
        header_al += "\nAlert Types: All"

    st.title(title)
    st.write(header_loc)
    st.write(header_al)


    # Placeholder for live update
    live_update_placeholder_hist = st.empty()
    live_update_placeholder_scat = st.empty()

    # Simulate initial data load
    data = simulate_live_update()

    # Display initial histogram
    fig, ax = plt.subplots()
    sns.histplot(data["alertDate"].dt.hour, bins=range(0, 25), kde=False, ax=ax)
    ax.set_xticks(range(0, 24, 2))  # Set x-axis ticks for every other hour
    ax.set_xlabel("Hour of the Day")
    ax.set_ylabel("Number of Rockets")
    live_update_placeholder_hist.pyplot(fig)
    live_update_placeholder_hist.text("Live updates are enabled. Data is updating automatically.")

    # Simulate live updates every 5 seconds
    while True:
        # Simulate waiting for updates
        time.sleep(1)

        # Update the data
        data = simulate_live_update()

        # Filter data based on date range and selected locations
        filtered_data = data[
            (data['alertDate'].dt.date >= start_date) & (data['alertDate'].dt.date <= end_date) &
            (data['data'].isin(selected_locations)) &
            (data['category_desc'].isin(selected_alerts))
        ]


     # Update the histogram in the placeholder
        fig, ax = plt.subplots()
        sns.histplot(filtered_data["alertDate"].dt.hour, bins=range(0, 25), kde=False, ax=ax)
        ax.set_xticks(range(0, 24, 2))  # Set x-axis ticks for every other hour
        ax.set_xlabel("Hour of the Day")
        ax.set_ylabel("Number of Rockets")
        live_update_placeholder_hist.pyplot(fig)

        # Scatter plot
        scatter_fig, scatter_ax = plt.subplots()
        # Convert the time to hours, including fractions
        hours = filtered_data["alertDate"].dt.hour + filtered_data["alertDate"].dt.minute/60 + filtered_data["alertDate"].dt.second/3600
        scatter_ax.scatter(hours, filtered_data["alertDate"].dt.date, alpha=0.5)
        scatter_ax.set_xticks(range(0, 24, 2))
        scatter_ax.set_xlabel("Hour of the Day")
        scatter_ax.set_ylabel("Date")
        scatter_ax.set_title("Scatter Plot of Sirens")
        scatter_ax.yaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        live_update_placeholder_scat.pyplot(scatter_fig)


# Run the app
if __name__ == "__main__":
    main()

