import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# Fullskjerm layout
st.set_page_config(layout="wide")

geolocator = Nominatim(user_agent="jobb_lokalisering", timeout=10)
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "show_form" not in st.session_state:
    st.session_state.show_form = False

job_suggestions = [
    "Klippe gresset", "Hårklipp", "Handle for noen", "Hente noe", "Levere noe", "Kjøre noen",
    "Bære noe", "Sette opp IKEA", "Vanne planter", "Passe hunden", "Levere nøkler",
    "Holde eldre med selskap", "Dugnadshjelp", "Sjekke om noe er glemt", "Håndverkertjenester",
    "Små oppussingsjobber", "Male terskel", "Skru sammen hundehus", "Koble opp lampe",
    "Skru opp støvsuger", "Bytte kjøkkenbenk", "Hente grus", "Kaste noe", "Vaske vinduer",
    "Vaskehjelp", "Rydde", "Dele ut flyers", "Levere bil til verksted", "Skifte dekk",
    "Sjekke dør på hytta"
]

st.title("Nabolagsmikrojobs")

with st.sidebar:
    if st.button("Legg til oppdrag"):
        st.session_state.show_form = True

# Smal venstre kolonne, bred høyre kolonne
col1, col2 = st.columns([1, 4])

with col1:
    if st.session_state.show_form:
        st.subheader("Legg inn en jobb")
        with st.form("job_form"):
            title = st.text_input("Jobbtittel")
            job_type = st.selectbox("Velg oppdragstype", job_suggestions)
            description = st.text_area("Beskrivelse")
            street_address = st.text_input("Gateadresse")
            city = st.text_input("By")
            price = st.slider("Pris", min_value=39, max_value=200, value=100, step=1)
            urgent = st.checkbox("Hasteoppdrag (300 kr ekstra)")
            image = st.file_uploader("Last opp bilde av oppdraget", type=["jpg", "jpeg", "png"])
            submitted = st.form_submit_button("Send inn jobb")
            if submitted:
                full_address = f"{street_address}, {city}, Norge"
                location = geolocator.geocode(full_address)
                if location:
                    job_entry = {
                        "title": title,
                        "type": job_type,
                        "location": [location.latitude, location.longitude],
                        "description": description,
                        "price": f"{price} kr" + (" + Haste" if urgent else ""),
                        "urgent": urgent,
                        "image": image.name if image else None
                    }
                    st.session_state.jobs.append(job_entry)
                    st.success(f"Jobben '{title}' ble lagt inn på {full_address}!")
                    st.session_state.show_form = False
                else:
                    st.error("Adressen kunne ikke geolokaliseres. Prøv en annen adresse.")

with col2:
    st.subheader("Jobber på kartet")
    oslokart = folium.Map(location=[59.9139, 10.7522], zoom_start=12)
    for job in st.session_state.jobs:
        color = "red" if job.get("urgent") else "blue"
        folium.CircleMarker(
            location=job["location"],
            radius=8,
            color=color,
            fill=True,
            fill_color=color,
            popup=f"{job['title']} ({job['type']}): {job['description']} ({job['price']})"
        ).add_to(oslokart)
    st_data = st_folium(oslokart, width=1200)
