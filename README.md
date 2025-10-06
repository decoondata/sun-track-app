# ☀️ SUN TRACK - MVP (Miraflores as Sample)

**Smart Well Cities prototype — Healthy walking routes with lower solar exposure 🌳**

This project is a **prototype** designed to help users find **walking routes with lower solar exposure**, promoting healthier and safer urban mobility.  
The current version uses **Miraflores (Lima, Peru)** as a **sample location** for testing and demonstration, but it is **scalable** to other cities.

---

## 🚀 Features

- 🗺️ **Interactive Map** to calculate and visualize up to **3 walking routes**  
- 🌳 **Shade simulation**: suggests the path with higher shade coverage  
- 🧠 **Smart routing**: prioritizes user health by reducing sun exposure  
- 📊 **Data Analysis** from NASA and OSM datasets to understand global solar trends  
- 📎 Includes **scientific references** and **open datasets** for reproducibility  

---

## 🧭 App Sections

### 1. **Introduction**
Explains the concept and benefits of choosing shaded, low-solar-exposure walking routes.

### 2. **Map**
Users can:
- Enter **origin** and **destination** (address or coordinates)  
- Visualize **three alternative routes**  
- See **distance**, **duration**, and **simulated shade percentage**  

### 3. **Analysis**
Global insights from NASA datasets:
- **Seasonal Variation** — shortwave & longwave peaks  
- **Long-Term Trends** — +15% solar increase since 1983  
- **Regional Differences** — Asia & Africa most exposed  
- **Country Hotspots** — Pakistan, Oman, UAE  
- **Spatial Clusters** — equatorial & desert belts with high UV

📓 Reproducibility Notebook:  
🔗 [Google Colab Analysis](https://colab.research.google.com/drive/1rKnuQe6UydH8H0ZGUVVh0Rb4JOQujOU0?usp=sharing)

### 4. **References**
Links to NASA datasets, WHO guidelines, and related research papers.

---

## 🧠 Algorithm

The prototype uses:
- **OSMnx** and **NetworkX** to build and query walking networks  
- **Geopy** to compute distances and travel times  
- **Simulated shade percentages** (future versions will integrate real tree & park data from OSM and Sentinel imagery)

🧩 *Greedy heuristic:*  
Selects routes by length and simulated shading to recommend the healthiest option.

---

## 🧰 Tech Stack

| Category | Tools |
|----------|-------|
| 💻 Language | Python 3.10 |
| 🌐 Web App | [Streamlit](https://streamlit.io/) |
| 🗺️ Mapping | [OSMnx](https://osmnx.readthedocs.io/), [Folium](https://python-visualization.github.io/folium/) |
| 📐 Graphs | [NetworkX](https://networkx.org/) |
| 📏 Geocoding | [Geopy](https://geopy.readthedocs.io/) |
| 📊 Analysis | Matplotlib, Pandas, Numpy |
| ☁️ Dev Environment | Visual Studio Code, Google Colab |
| 🔢 Datasets | NASA EarthData, WHO, OpenStreetMap |

---

## 🌍 Data Sources

### 🛰️ NASA Datasets
- **Global High Resolution Daily Extreme Urban Heat Exposure (1983–2016)**  
  🔗 [EarthData Search](https://search.earthdata.nasa.gov/search/granules/collection-details?p=C3540912037-ESDIS&pg[0][v]=f&pg[0][gsk]=-start_date&q=1983&gdf=CSV&tl=946684800!5)  
- **BOREAS Follow-On HMet-03 (1994–1996)**  
  🔗 [EarthData Catalog](https://www.earthdata.nasa.gov/data/catalog/ornl-cloud-bfo-hmet03-hourly-met-p1-608-1?utm_source)  
- **Land Surface Temperature Anomaly & Net Radiation**  
  🔗 [NASA Earth Observatory](https://earthobservatory.nasa.gov/global-maps/MOD_LSTAD_M/CERES_NETFLUX_M)

### 🧠 Scientific & Institutional References
- [WHO — Ultraviolet Radiation](https://www.who.int/health-topics/ultraviolet-radiation#tab=tab_2)  
- [Sun Exposure: Beyond the Risks (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6830553/#sec15)  
- [Urban Green Spaces & Cooling (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S2210670725003890#sec5)

---

## 📈 Future Improvements

- 🌳 **Integration with OSM tree & park data** for real shade measurement  
- 🕒 **Time-of-day solar exposure model**  
- 📱 **User preferences** (health goals, sun sensitivity)  
- ☁️ **Weather & UV index API integration**  
- 🤖 **Machine Learning** for route prediction under varying conditions  

---

## 📜 License
MIT License © 2025 — Sun Track MVP Prototype
