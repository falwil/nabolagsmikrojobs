
import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# Initialiser geolokalisering
geolocator = Nominatim(user_agent="jobb_lokalisering", timeout=10)

# Bruk session state for å lagre jobber
if "jobs" not in st.session_state:
    st.session_state.jobs = [
        {"title": "Gressklipping", "location": [59.9139, 10.7522], "description": "Klipp plenen foran huset.", "price": "200 kr"},
        {"title": "Handle dagligvarer", "location": [59.92, 10.75], "description": "Hente dagligvarer fra nærbutikk.", "price": "150 kr"}
    ]

# Layout for Streamlit-app
st.title("Nabolagsmikrojobs")

# Skjema for å legge inn jobb
st.subheader("Legg inn en jobb")
with st.form("job_form"):
    title = st.text_input("Jobbtittel")
    description = st.text_area("Beskrivelse")
    street_address = st.text_input("Gateadresse")
    city = st.text_input("By")
    price = st.text_input("Pris")
    submitted = st.form_submit_button("Send inn jobb")
    if submitted:
        full_address = f"{street_address}, {city}, Norge"
        location = geolocator.geocode(full_address)
        if location:
            st.session_state.jobs.append({
                "title": title,
                "location": [location.latitude, location.longitude],
                "description": description,
                "price": price
            })
            st.success(f"Jobben '{title}' ble lagt inn på {full_address}!")
        else:
            st.error("Adressen kunne ikke geolokaliseres. Prøv en annen adresse.")

# Kartvisning
st.subheader("Jobber på kartet")
oslokart = folium.Map(location=[59.9139, 10.7522], zoom_start=12)
for job in st.session_state.jobs:
    folium.Marker(location=job["location"], popup=f"{job['title']}: {job['description']} ({job['price']})").add_to(oslokart)
st_data = st_folium(oslokart, width=700)

# Skjema for tjenestetilbyder
st.subheader("Tilby dine tjenester")
with st.form("service_form"):
    name = st.text_input("Ditt navn")
    skills = st.text_area("Ferdigheter")
    availability = st.text_input("Tilgjengelighet")
    submitted_service = st.form_submit_button("Send inn tjeneste")
    if submitted_service:
        st.success(f"Tjeneste fra '{name}' ble sendt inn!")

# Skjema for vurdering
st.subheader("Vurder en jobbopplevelse")
with st.form("rating_form"):
    rater = st.text_input("Ditt navn")
    ratee = st.text_input("Hvem vurderer du?")
    rating = st.slider("Vurdering", 1, 5)
    comments = st.text_area("Kommentarer")
    submitted_rating = st.form_submit_button("Send inn vurdering")
    if submitted_rating:
        st.success(f"Vurdering sendt inn for {ratee} av {rater}!")
