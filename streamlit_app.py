# Import python packages
import streamlit as st
import os
import requests  
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":rocket: My own aPP :rocket:")
st.write(
  """**Choose the ingridients**
  """
)
title = st.text_input('Smothies Name')
st.write("The name on your cup will be: ---", title)
#option = st.selectbox(
#    "Which fruits would you prefer?",
#    ("Apple", "Orange", "Cucumber"),
#)

#st.write("You selected:", option)

# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingridients_list = st.multiselect(
    "Choose up to 5 ingridients:",
    my_dataframe, max_selections=5
)

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
st.text(smoothiefroot_response.json)

if ingridients_list :
   # st.write(ingridients_list)
   # st.text(ingridients_list)

    ingredients_string=''
    for fruit in ingridients_list:
        ingredients_string += fruit + ' '
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """','""" + title + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit order!')
    if time_to_insert and ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered {title} !" , icon="✅")
    
st.markdown("""
- :page_with_curl: [Streamlit open source documentation](https://docs.streamlit.io)
- :snowflake: [Streamlit in Snowflake documentation](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)
- :books: [Demo repo with templates](https://github.com/Snowflake-Labs/snowflake-demo-streamlit)
- :memo: [Streamlit in Snowflake release notes](https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake)
""")
