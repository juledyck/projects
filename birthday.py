import streamlit as st
import random
import time
import json
from streamlit_extras.let_it_rain import rain
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta


token_json_secret = st.secrets["token"]
tokensecret = json.loads(token_json_secret)

# Google Drive API einrichten
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
folder_id = '1HEC4cAZ6G70v26llUIskK9I5w11paLRv'

def load_credentials():
    creds = Credentials.from_authorized_user_info(tokensecret, SCOPES)
    return creds


#Definitionen für Die Rezepte
def list_text_files(service, folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents and mimeType='text/plain'",
        fields="files(id, name)"
    ).execute()
    return results.get('files', [])

def read_file_content(file_id):
    request = service.files().get_media(fileId=file_id)
    file_content = request.execute()
    return file_content.decode('utf-8')

#Definitionen für die Bilder
def list_image_files(service, folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents and mimeType='image/jpeg'",
        fields="files(id, name)"
    ).execute()
    return results.get('files', [])

def read_image_file_content(file_id):
    request = service.files().get_media(fileId=file_id)
    file_content = request.execute()
    return file_content

def start_rain(emojii):
    rain(
        emoji=emojii,
        font_size=54,
        falling_speed=5,
        animation_length="5s"
    )



st.title("Dyckhome")

#Das Radio
st.sidebar.title("Dycksches Radio")
st.sidebar.write("Pick your favourite Playlist")

st.sidebar.write("Arnes Mix")
spotify_embed_code = """
<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/65q5bhglITXhDffQzH0MTc?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>"""
st.sidebar.markdown(spotify_embed_code, unsafe_allow_html=True)


st.sidebar.write("Jules Mix")
spotify_embed_code2 = """
<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/59I9uVzvd7rZFYtj9GFb0w?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>"""
st.sidebar.markdown(spotify_embed_code2, unsafe_allow_html=True)

st.write("")
st.write("")

st.sidebar.write("Karens Mix")
spotify_embed_code3 = """
<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/7lKXo4oipZUkh0o7QBf1Ma?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>"""
st.sidebar.markdown(spotify_embed_code3, unsafe_allow_html=True)

st.sidebar.write("HK Mix")
spotify_embed_code4 = """
<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/1E2ob6ZfTx4r0YC5Yyryx5?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>"""
st.sidebar.markdown(spotify_embed_code4, unsafe_allow_html=True)



col0, col01 = st.columns([2,1])
with col0:
    st.write("Eine Website für die besten Eltern der Welt.")
with col01:
    if st.button("Refresh-Button"):
        start_rain("❤️")
col1, colo, col2 = st.columns([2,1,2])

#Bilder
with col1:
    st.header("Picture of the day")

    creds = load_credentials()
    service = build("drive", "v3", credentials=creds)

    image_files = list_image_files(service, folder_id)

    if image_files:
        random_image = random.choice(image_files)
        image_id = random_image['id']
        image_name = random_image['name']

        image_content = read_image_file_content(image_id)

        st.image(image_content, caption=image_name, use_column_width=True)
    else:
        st.write("Keine Bilddateien im angegebenen Ordner gefunden.")


#Countdown
with col2:    
    # Liste der Events
    events = {
        "zu Karens Geburtstag": datetime(2024, 9, 29),
        "zu Hans-Karls Geburtstag": datetime(2024, 10, 1),
        "zum kirchlichen Hochzeitstag und Jules Tauftag": datetime(2024, 10, 9),
        "zum standesamtlichen Hochzeitstag": datetime(2024, 10, 10),
        "zu Arnes Geburtstag": datetime(2024, 11, 11), 
        "zu Jules Geburtstag": datetime(2024, 11, 19),
        "zu Gerti Geburtstag": datetime(2024, 12, 11),
        "zu Weihnachten": datetime(2024, 12, 24),
        "zu Friederikes Geburtstag": datetime(2024, 12, 28),
        "zu Wolfgangs Geburtstag": datetime(2025, 7, 30),  
        "zu Kallis Geburtstag": datetime(2025, 9, 3),  
    }

    now = datetime.now()

    next_event = None
    next_event_name = ""
    event_today = None

    #Überprüfen, ob heute ein Event ist
    for event_name, event_time in events.items():
        if event_time.date() == now.date():
            event_today = event_name
            break

    #Anzeigen des heutigen Events
    st.write("")
    st.write("")
    if event_today:
        st.write(f"🎉 Glückwunsch {event_today}!")
    else:
        st.write("☁️ Für heute steht nichts an.")

    #Nächstes Event
    for event_name, event_time in events.items():
        if event_time > now:
            next_event = event_time
            next_event_name = event_name
            break

    # Countdown berechnen
    if next_event:
        time_remaining = next_event - now
        days, seconds = time_remaining.days, time_remaining.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        # Countdown anzeigen
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("Noch... ")

        day_progress = round(100 - (days / 365 * 100))  # Verbleibende Tage in % von 365
        hour_progress = round(100 - (hours / 24 * 100))  # Verstrichene Stunden in % von 24
        minute_progress = round(100 - (minutes / 60 * 100))  # Verstrichene Minuten in % von 60

        # Anzeige in Spalten
        coll, colm, coln = st.columns(3)
        coll.metric("Tage", days, f"{day_progress}%")
        colm.metric("Stunden", hours, f"{hour_progress}%")
        coln.metric("Minuten", minutes, f"{minute_progress}%")

        st.write(f"bis {next_event_name}")        
        
    else:
        st.write("Keine zukünftigen Events gefunden.")

#Rezept
st.header("Rezeptgenerator")
st.write("")

if folder_id:
    creds = load_credentials()
    print(creds)
    service = build("drive", "v3", credentials=creds)

    files = list_text_files(service, folder_id)

    if files:
        selected_file = st.selectbox("Hier kannst du ein neues Lieblingsrezept finden:", [file['name'] for file in files])
        file_id = next(file['id'] for file in files if file['name'] == selected_file)

        if st.button("Inhalt anzeigen"):
            content = read_file_content(file_id)
            st.text_area("Dateiinhalt:", content, height=300)
    else:
        st.write("Keine Textdateien im angegebenen Ordner gefunden.")
