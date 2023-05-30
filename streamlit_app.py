import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

st.title("My Mom's New Healthy Diner")

st.header('Breakfast Favorites')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# st.dataframe(my_fruit_list)
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# set_index (0,1,2..가 아니라 Fruit열을 인덱스로 만들어줘)
my_fruit_list = my_fruit_list.set_index('Fruit') 
# DataFrame.set_index(keys, drop=True, append=False, inplace=False)
# drop: 인덱스로 세팅한 열을 DataFrame 내에서 삭제할지 여부 결정(option)
# append: 기존에 존재하던 인덱스 삭제 여부 결정(option)
# inplace: 원본 객체 변경 여부 결정(option)


# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on the page
st.dataframe(fruits_to_show)

# create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

# New Section to display fruityvice api response
st.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    st.dataframe(back_from_function)
except URLError as e:
  st.error()


# don't run anything past here while we troubleshoot
st.stop()

st.header("The fruit load list contains:")
# Snowflake-related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

#  Add a button to load the fruit
if st.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  st.dataframe(my_data_rows)

# Allow the end user to add a fruit to the list
add_my_fruit = st.text_input('What fruit would you like to add?','')
st.write('Thanks for adding ', add_my_fruit)

# This will not work correctly, but just go with it for now
my_cur.execute("insert into fruit_load_list values('from streamlit')")
