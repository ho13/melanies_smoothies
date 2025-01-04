# -- Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session -- this only works in SiS (streamlit in snowflake)

# -- import the function col so that we bring back only the column name at rather than the whole table at line 26 
from snowflake.snowpark.functions import col , when_matched

# -- Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders:cup_with_straw:")
st.write(
    """Order that need to filled.
    """
)

# -- Display the Fruit Options List (insert a table)
# session = get_active_session() -- this only works in SiS 
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.orders").filter(col('ORDER_FILLED')==0).collect()
# st.dataframe(data=my_dataframe, use_container_width=True) #show the dataframe (not editable)

# Show the table if the dataframe exists, otherwise show a message saying no orders
if my_dataframe: 
    editable_df = st.data_editor(my_dataframe) # convert the dataframe to a data editor
    
    submitted = st.button('Submit')
    
    if submitted: 
        
        # Add a Merge Statement so when the order_filled is ticked, the value of the ORDER_FILLED column in the underlying dataset will be undated
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
    
        try: 
            og_dataset.merge(edited_dataset
                            , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                            , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                            )
            st.success("Someone clicked the button.", icon = "👍")
        except: 
            st.write('Something went wrong.')
else: 
    st.success('There are no pending orders right now.', icon = "👍")







