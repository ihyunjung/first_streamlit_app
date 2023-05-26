import streamlit as st

st.title('My Parents New Healthy Diner')

st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas as pd
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

# New Section to display fruityvice api response
st.header('Fruityvice Fruit Advice!')

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json()) # just writes the date to the screen

# take the json version of the response and normalize it
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# output it the screen as a table
st.dataframe(fruityvice_noramlized)
