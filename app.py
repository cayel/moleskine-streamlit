import streamlit as st
import firebase_admin 
from firebase_admin import db
import pandas
import toml

#configuration of the page
st.set_page_config(layout="wide")

#load dataframes
if not firebase_admin._apps:
	# Créer une instance de FirebaseApp à l'aide des informations d'identification
	cred = firebase_admin.credentials.Certificate({
    	"type": st.secrets.type,
		"private_key" : st.secrets.private_key,
		"client_email" : st.secrets.client_email,
		"token_uri" : st.secrets.token_uri
	})
	default_app = firebase_admin.initialize_app(cred,{
		"databaseURL": st.secrets.databaseURL
		})

ref_path = "/movies/"+st.secrets.user_id
print(ref_path)
ref = db.reference(ref_path)

snapshot = ref.get()

df=pandas.DataFrame(snapshot.items())
df.columns = ['_id', '_object']
print(df)

df1 = pandas.DataFrame([x for x in df['_object']]).join(df['_id'])
df1 = df1.sort_index(1)
def convert_date_firebase(date):
    return pandas.Timestamp(date, unit='ms').year

df1['date'] = df1['date'].apply(convert_date_firebase)
print(df1)

st.title('Moleskine')
st.markdown("""
Cette application analyse les films regardés au cours des dernières années
""")

#st.dataframe(df1[['cinema','title','director','rating','date']])

st.sidebar.header('Select what to display')
directors = df1['director'].unique().tolist()
directors_selected = st.sidebar.multiselect('Réalisateurs', directors, directors)

#selected_years = st.sidebar.slider("Années", 2009, 2025, (2023, 2023))

#creates masks from the sidebar selection widgets
mask_directors = df1['director'].isin(directors_selected)

df_movies_filtered = df1[mask_directors]
st.write(df_movies_filtered)

df2 = df1.groupby(['date'])['date'].count().reset_index(name='count')
st.bar_chart(df2,x='date',y='count')


