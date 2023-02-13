import streamlit as st
import firebase_admin 
from firebase_admin import db
import pandas

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
ref = db.reference(ref_path)

# Load all movies in dataframe
snapshot = ref.get()
df=pandas.DataFrame(snapshot.items())
df.columns = ['_id', '_object']

df1 = pandas.DataFrame([x for x in df['_object']]).join(df['_id'])

def convert_date_firebase(date):
    return pandas.Timestamp(date, unit='ms').year

df1['years'] = df1['date'].apply(convert_date_firebase)
f1 = df1.sort_values(by='date', ascending=False)

st.title('Moleskine')
st.subheader('Les 10 derniers films vus')

#st.dataframe(df1[['title','director']])
count = 0
for i, j in df1.iterrows():
	count = count+1
	str_cinema = ''
	if (j['cinema'] == True):
		str_cinema=':cinema:'
	st.markdown(j['title']+' ('+j['director']+')'+str_cinema)
	if (count == 10):
		break
#st.sidebar.header('Filtrer')
#years = df1['date'].unique().tolist()
#years_selected = st.sidebar.multiselect('Années', years, years)

#selected_years = st.sidebar.slider("Années", 2009, 2025, (2023, 2023))

#creates masks from the sidebar selection widgets
#mask_years = df1['director'].isin(years_selected)

#df_movies_filtered = df1[mask_years]
#st.write(df_movies_filtered)

#df2 = df1.groupby(['date'])['date'].count().reset_index(name='count')
#st.bar_chart(df2,x='date',y='count')

