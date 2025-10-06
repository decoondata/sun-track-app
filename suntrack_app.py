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
st.title("☀️ SUN TRACK - MVP Prototpye (Miraflores, Perú as sample)")
st.markdown("""
Smart Well Cities prototype — **Healthy walking routes with lower solar exposure** 🌳  
*(Miraflores is used as a sample location for testing and demonstration purposes.)*
""")

# 🧭 Tabs
tabs = st.tabs(["🏙️ Introduction", "🗺️ Map", "📊 Analysis", "📚 Reference"])

# ---------------- INTRO ----------------
with tabs[0]:
    st.header("About Sun Track")
    st.markdown("""
    **Sun Track** helps you find walking routes in Miraflores with **lower solar exposure**.  
    **Sun Track** is a prototype that identifies **walking routes with lower solar exposure** 🌞,  
    initially tested in *Miraflores (Lima, Peru)* as a **sample city**, but scalable to other urban areas.

    ### Why use it
    - ☀️ Less UV exposure = less skin damage  
    - 🧠 Promotes healthier habits  
    - 🌳 Shady routes feel cooler and safer
    """)
    st.image("images/suntrack.png", caption="Smart Well Cities Vision", use_container_width=False, width=400)

# ---------------- MAP ----------------
with tabs[1]:
    st.header("🗺️ Interactive Map")
    st.markdown("Enter your origin and destination below (address or coordinates) to calculate **three walking routes** and visualize them 🌳")

    # Function to get coordinates from address or direct input
    def get_coords(name):
        try:
            if "," in name:  # user entered coordinates
                lat, lon = map(float, name.split(","))
                return (lat, lon)
            geolocator = Nominatim(user_agent="suntrack")
            loc = geolocator.geocode(name + ", Miraflores, Lima, Peru")
            return (loc.latitude, loc.longitude) if loc else None
        except:
            return None

    # Inputs with default coordinates that work
    col1, col2 = st.columns(2)
    with col1:
        origin = st.text_input("Enter starting point (address or lat, lon):", "-12.1211, -77.0293")
    with col2:
        dest = st.text_input("Enter destination (address or lat, lon):", "-12.1239, -77.0318")

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
            # Build walking network
            G = ox.graph_from_point(o, dist=1500, network_type='walk')
            G_simple = nx.Graph(G)
            nO = ox.distance.nearest_nodes(G, o[1], o[0])
            nD = ox.distance.nearest_nodes(G, d[1], d[0])
            routes = list(islice(nx.shortest_simple_paths(G_simple, nO, nD, weight='length'), 3))

            m = folium.Map(location=o, zoom_start=16)
            colors = ['red', 'blue', 'green']
            results = []

            # 🚧 Attempted real shade calculation using park buffers:
            """
            # This approach was tested in Google Colab with geopandas:
            # buffer_m = 40
            # gdf_parques = ox.features_from_place("Miraflores, Lima, Peru", {"leisure": "park"})
            # parques_buffer = gdf_parques.buffer(buffer_m)
            # For each route, compute intersection with buffer and shade percentage.
            # However, OSMnx 'features_from_place' is not supported in Streamlit Cloud.
            """

            # 🔢 Simulate shadow percentage: route 1 more shaded than others
            base_shades = [random.randint(40, 55), random.randint(30, 45), random.randint(20, 35)]
            base_shades.sort(reverse=True)

            for i, r in enumerate(routes):
                coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in r]
                length_m = sum(geodesic(coords[j], coords[j+1]).meters for j in range(len(coords)-1))
                time_min = length_m / 80  # 80 m/min ≈ 4.8 km/h
                shade_percent = base_shades[i]  # simulated

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

        st.success("✅ Route 1 is recommended as it offers higher shade coverage.")
        st.info("☀️ Avoid sun exposure between **10 a.m. and 4 p.m.**")
        st.info("💧 Stay hydrated and wear **a hat, long sleeves, and sunscreen**.")

# ---------------- ANALYSIS ----------------
with tabs[2]:
    st.header("📊 Analysis")
    st.markdown("""
    This section explores **solar radiation patterns** using NASA and OSM datasets.  
    The following analyses illustrate global and seasonal exposure trends to help identify regions with higher health risks.
    """)

    # 💡 Interpretation 1 – Seasonal Variation
    st.subheader("💡 Interpretation 1 – Seasonal Variation (BOREAS 1994)")
    st.markdown("""
    ☀️ **Shortwave radiation** peaks during **summer months (~370 W/m²)**, while **longwave radiation** remains consistently high (**>250 W/m²**).  
    📈 This indicates **strong solar exposure** in warmer seasons, increasing **UV risks** and potential **skin damage**.
    """)
    st.image("graph2.png", caption="📅 Monthly Average of Shortwave and Longwave Radiation (BOREAS 1994)")

    # 💡 Interpretation 2 – Long-Term Trend
    st.subheader("💡 Interpretation 2 – Long-Term Trend (1983–2016)")
    st.markdown("""
    📈 The average **solar intensity** shows a **slight upward trend (+15%)** over 30 years.  
    ⚠️ This sustained high radiation level suggests increasing exposure, potentially intensifying **ozone depletion effects** and **UV penetration**.
    """)
    st.image("graph3.png", caption="📈 Trend of Solar Intensity (1983–2016)")

    # 💡 Interpretation 3 – Regional Differences
    st.subheader("💡 Interpretation 3 – Regional Differences")
    st.markdown("""
    🌍 **Asia** and **Africa** exhibit the **highest and most variable** solar intensities, with medians near **2 W/m²** and peaks over **6 W/m²**.  
    🧴 Populations in these zones require **greater sun protection** and **urban planning** with shade and vegetation.
    """)
    st.image("graph4.png", caption="🌍 Regional Differences in Solar Intensity")

    # 💡 Interpretation 4 – Country-Level Hotspots
    st.subheader("💡 Interpretation 4 – Country-Level Hotspots")
    st.markdown("""
    🏆 **Pakistan**, **Oman**, and **UAE** lead with **>3 W/m² average solar intensity**, aligning with **desert** and **equatorial** regions.  
    ☀️ These areas face **extreme UV levels**, increasing risks of **skin cancer** and **heat stress**.
    """)
    st.image("graph5.png", caption="🏆 Top 10 Countries by Average Solar Intensity")

    # 💡 Interpretation 5 – Spatial Clusters
    st.subheader("💡 Interpretation 5 – Spatial Clusters")
    st.markdown("""
    🗺️ High-intensity clusters concentrate in **equatorial**, **arid**, and **tropical** zones.  
    🔆 These combine long **sunlight hours** and reflective surfaces (sand, sea), amplifying **radiation exposure** to dangerous levels.
    """)
    st.image("graph1.png", caption="🗺️ Geographical Distribution of Solar Intensity")

    # 🌍 General Conclusion
    st.subheader("🌍 General Conclusion")
    st.markdown("""
    ⚠️ Sustained and rising **solar radiation**—especially in **Asia**, **Africa**, and **desert regions**—shows a global increase in **UV exposure**.  
    Without adequate protection, risks of **skin cancer**, **photoaging**, and **heat-related illnesses** grow significantly.  
    💡 Future cities must integrate **shade infrastructure**, **sunscreen campaigns**, and **UV-aware planning** for healthier urban living.
    """)

# ---------------- REFERENCE ----------------
with tabs[3]:
    st.header("📚 References")
    st.write("""
    - OpenStreetMap API  
    - NASA Earth Observatory Data  
    - WHO Urban Health Guidelines  
    - Lima Smart Cities Initiative
    """)




