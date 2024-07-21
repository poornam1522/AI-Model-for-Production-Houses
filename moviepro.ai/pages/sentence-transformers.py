import pandas as pd
import streamlit as st
import json
import streamlit.components.v1 as components
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import ast

st.markdown("<h1 style='text-align: center; color: blue;'>Moviepro.ai</h1>", unsafe_allow_html=True)
st.write("## Extract keywords, find similar movie plots with Sentence Transformers")

movie_plots_path = "American_Movie_Plots_2005_2021_v1_embeddings.csv"

@st.cache
def load_data():
     df = pd.read_csv(movie_plots_path,converters={'full_embeddings':ast.literal_eval})
     df.drop_duplicates(subset ="Wiki Link", keep = False, inplace = True)
     return df


def get_similar_movies(N,index):
  document_embedd = data.iloc[index]['full_embeddings']
  plot_embedds = data['full_embeddings'].to_list()

  word_doc_similarity = cosine_similarity(plot_embedds, [document_embedd])
  word_doc_similarity = word_doc_similarity.flatten()

  plots_idx = np.argsort(word_doc_similarity)
  plots_idx = plots_idx[::-1]

  related_docs_indices = list(plots_idx)[:N]
  titles=[]
  plots =[]
  links=[]
  for ind in related_docs_indices:
    title = data.iloc[ind]['Movie Name']
    movie_plot = data.iloc[ind]['Plot']
    link = data.iloc[ind]['Wiki Link']
    titles.append(title)
    plots.append(movie_plot)
    links.append(link)
  return titles,plots,links

# Read the data
data = load_data()

st.write("")
if "page" not in st.session_state:
    st.session_state.page = 0

def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1


page_number = 0
last_page = len(data)

prev, middle ,next = st.columns([2, 2, 2])

if st.session_state.page < last_page:
    next.button(">", on_click=next_page)
else:
    next.write("")  # this makes the empty column show up on mobile

if st.session_state.page > 0:
    prev.button("<", on_click=prev_page)
else:
    prev.write("")  # this makes the empty column show up on mobile

middle.write(f"Page {1+st.session_state.page} of {last_page}")

row = data.iloc[st.session_state.page]
movie_name = row['Movie Name']
link = row['Wiki Link']
plot = row['Plot']
st.header(movie_name)
st.write(link)
st.write(plot)


if st.button('Get similar plots'):
  movienames,movieplots,links = get_similar_movies(6,st.session_state.page)
  for name,plt,li in zip(movienames,movieplots,links):
    st.header(name)
    st.write(li)
    st.write(plt)
    st.markdown("""---""")