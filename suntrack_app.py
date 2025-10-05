# suntrack_app.py
import streamlit as st
import osmnx as ox
import networkx as nx
from itertools import islice
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium
import random

st.set_page_config(page_title="SUN TRACK MVP", layout="wide")

# 🌞 Header
st.title("☀️ SUN TRACK - MVP (Miraflores)")
st.markdown("Smart Well Cities prototype — **Healthy walking routes with lower solar exposure** 🌳")

# 🧭 Tabs
tabs = st.tabs(["🏙️ Introduction", "🗺️ Map", "📊 Analysis", "📚 Reference"])

# ---------------- INTRO ----------------
with tabs[0]:
    st.header("About Sun Track")
    st.markdown("""
    **Sun Track** helps you find walking routes in Miraflores with **lower solar exposure**.  
    ☀️ Based on **OpenStreetMap** and **urban data**.  
    🌳 Encourages healthy, shaded mobility.

    ### Why use it
    - ☀️ Less UV exposure = less skin damage  
    - 🧠 Promotes healthier habits  
    - 🌳 Shady routes feel cooler and safer
    """)
    st.image("images/suntrack.png", caption="Smart Well Cities Vision", use_container_width=False, width=400)

# ---------------- MAP ----------------
with tabs[1]:
    st.header("🗺️ Interactive Map")
    st.markdown("Enter your origin and destination below to calculate **three walking routes** and visualize them 🌳")

    # Function to get coordinates
    def get_coords(name):
        geolocator = Nominatim(user_agent="suntrack")
        try:
            loc = geolocator.geocode(name + ", Miraflores, Lima, Peru")
            return (loc.latitude, loc.longitude) if loc else None
        except:
            return None

    # Inputs
    col1, col2 = st.columns(2)
    with col1:
        origin = st.text_input("Enter starting point:", "Avenida José Pardo")
    with col2:
        dest = st.text_input("Enter destination:", "Calle Tarata")

    # Store map persistently
    if "map_data" not in st.session_state:
        st.session_state.map_data = None
        st.session_state.results = None

    if st.button("🚶 Calculate Route"):
        o = get_coords(origin)
        d = get_coords(dest)

        if not o or not d:
            st.error("❌ Place not found. Try another name or use coordinates (lat, lon).")
        else:
            G = ox.graph_from_point(o, dist=1500, network_type='walk')
            G_simple = nx.Graph(G)
            nO = ox.distance.nearest_nodes(G, o[1], o[0])
            nD = ox.distance.nearest_nodes(G, d[1], d[0])
            routes = list(islice(nx.shortest_simple_paths(G_simple, nO, nD, weight='length'), 3))

            m = folium.Map(location=o, zoom_start=16)
            colors = ['red', 'blue', 'green']
            results = []

            for i, r in enumerate(routes):
                coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in r]
                # Calcular distancia total con geodesic
                length_m = sum(geodesic(coords[j], coords[j+1]).meters for j in range(len(coords)-1))
                time_min = length_m / 80  # 80 m/min ≈ 4.8 km/h
                shade_percent = random.randint(50, 90)  # valor simulado

                folium.PolyLine(
                    coords,
                    color=colors[i],
                    weight=5,
                    opacity=0.8,
                    tooltip=f"Route {i+1}: {length_m:.0f} m | {time_min:.1f} min | 🌳 {shade_percent}% shade"
                ).add_to(m)

                results.append({
                    "id": i+1,
                    "distance": length_m,
                    "time": time_min,
                    "shade": shade_percent
                })

            folium.Marker(o, popup="Origin", icon=folium.Icon(color='green')).add_to(m)
            folium.Marker(d, popup="Destination", icon=folium.Icon(color='red')).add_to(m)

            # Save in session
            st.session_state.map_data = m
            st.session_state.results = results

    # Display map and info
    if st.session_state.map_data:
        st_folium(st.session_state.map_data, width=1000, height=600)

        st.subheader("🧾 Route Summary")
        for r in st.session_state.results:
            st.markdown(f"**Route {r['id']}** — 🛣️ {r['distance']:.0f} m | ⏱️ {r['time']:.1f} min | 🌳 {r['shade']}% shade")

        st.success("✅ Recommended route has more shade and lower sun exposure.")
        st.info("☀️ Avoid sun exposure between **10 a.m. and 4 p.m.**")
        st.info("💧 Stay hydrated and wear **a hat, long sleeves, and sunscreen**.")

# ---------------- ANALYSIS ----------------
with tabs[2]:
    st.header("📊 Analysis")
    st.write("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

# ---------------- REFERENCE ----------------
with tabs[3]:
    st.header("📚 References")
    st.write("""
    - OpenStreetMap API  
    - NASA Earth Observatory Data  
    - WHO Urban Health Guidelines
    """)
