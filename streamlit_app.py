# -- Import python packages
import streamlit as st
import requests
import pandas as pd

# -- import the function col so that we bring back only the column name at rather than the whole table at line 26 
from snowflake.snowpark.functions import col


# -- Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruit you want in the custom smoothie.
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order  )



#------------Adding a select box------------ 
# option = st.selectbox(
#     "What is your favourite fruit?",
#     ("Banana", "Strawberries", "Peaches"),
# )

# st.write("You favourite fruit is:", option)
# ------------------------------------------


# -- Display the Fruit Options List (insert a table)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')) 
# st.dataframe(data=my_dataframe, use_container_width=True) 
# st.stop()

# Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function 
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)

# -- Add a multiselect (the data type of the ingredients_list variable is a LIST)
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe 
    , max_selections = 5
)

if ingredients_list: 

    ingredients_string = ''

    for fruit_chosen in ingredients_list: 
        ingredients_string += fruit_chosen + ' '

        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')

        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("http://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)

    # st.write(ingredients_string) 

    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    # st.write(my_insert_stmt) 
    # st.stop() -- for trouble shooting or test
    
    time_to_insert = st.button('Submit Order')    
    
    if time_to_insert: 
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")










