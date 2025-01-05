import folium
from streamlit_folium import folium_static
import streamlit as st
import requests
from folium import plugins

def display_map():
    st.title("Hospital Navigation")
    
    # Create columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        user_location = st.text_input("Enter your location (address or coordinates)")
    
    with col2:
        transport_mode = st.selectbox(
            "Select transport mode",
            ["driving", "walking", "bicycling", "transit"]
        )

    # List of hospitals with their coordinates
    hospitals = [
        {"name": "Chirayu Multi Speciality Clinic", "lat": 22.7196, "lon": 75.8577},
        {"name": "Abhay Hospital", "lat": 22.7316, "lon": 75.8519},
        {"name": "Shreya Clinic", "lat": 22.7211, "lon": 75.8645},
    ]

    selected_hospital = st.selectbox(
        "Select destination hospital",
        [hospital["name"] for hospital in hospitals]
    )

    # Create the base map
    m = folium.Map(location=[12.92374198264633, 77.49863482253105], zoom_start=13)

    # Add the location search control
    plugins.LocateControl().add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)

    # Function to get coordinates from address using Nominatim
    def get_coordinates(address):
        try:
            url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json"
            response = requests.get(url)
            data = response.json()
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
            return None
        except Exception as e:
            st.error(f"Error getting coordinates: {e}")
            return None

    # If user enters location, add markers and route
    if user_location:
        user_coords = get_coordinates(user_location)
        if user_coords:
            # Add user marker
            folium.Marker(
                user_coords,
                popup="Your Location",
                icon=folium.Icon(color="blue", icon="user", prefix="fa"),
            ).add_to(m)

            # Find selected hospital coordinates
            dest_hospital = next(h for h in hospitals if h["name"] == selected_hospital)
            dest_coords = (dest_hospital["lat"], dest_hospital["lon"])

            # Add hospital marker
            folium.Marker(
                dest_coords,
                popup=selected_hospital,
                icon=folium.Icon(color="red", icon="plus", prefix="fa"),
            ).add_to(m)

            # Get route using OSRM
            try:
                route_url = f"http://router.project-osrm.org/route/v1/driving/{user_coords[1]},{user_coords[0]};{dest_coords[1]},{dest_coords[0]}?overview=full&geometries=geojson"
                response = requests.get(route_url)
                route_data = response.json()
                
                if route_data["code"] == "Ok":
                    # Draw the route
                    route_coords = route_data["routes"][0]["geometry"]["coordinates"]
                    route_coords = [[coord[1], coord[0]] for coord in route_coords]
                    
                    folium.PolyLine(
                        route_coords,
                        weight=4,
                        color='blue',
                        opacity=0.8
                    ).add_to(m)

                    # Calculate and display distance and estimated time
                    distance = route_data["routes"][0]["distance"] / 1000  # Convert to km
                    duration = route_data["routes"][0]["duration"] / 60    # Convert to minutes
                    
                    st.success(f"Distance: {distance:.2f} km")
                    st.success(f"Estimated time: {duration:.0f} minutes")

            except Exception as e:
                st.error(f"Error calculating route: {e}")

    # Add markers for all hospitals
    for hospital in hospitals:
        folium.Marker(
            location=[hospital["lat"], hospital["lon"]],
            popup=hospital["name"],
            icon=folium.Icon(color="red", icon="plus", prefix="fa"),
        ).add_to(m)

    # Add search box
    plugins.Search(
        layer=folium.FeatureGroup().add_to(m),
        geom_type="Point",
        placeholder="Search for places...",
        collapsed=False,
    ).add_to(m)

    # Display the map
    folium_static(m)
