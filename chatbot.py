import pandas as pd
import openai
import streamlit as st


data = pd.read_csv('/Users/lulali1/Documents/Chatbot-project/ml_project1_data.csv')


for col in data.columns:
    if pd.api.types.is_numeric_dtype(data[col]):
        data[col].fillna(data[col].median(), inplace=True)
    else:
        data[col].fillna(data[col].mode()[0], inplace=True)


openai.api_key = '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' 

def process_query(user_query):

    user_query = user_query.lower()


    potential_id = [int(s) for s in user_query.split() if s.isdigit()]

   
    if potential_id:
       
        customer_id = potential_id[0]

  
        if customer_id in data['ID'].values:
           
            customer_info = data[data['ID'] == customer_id].iloc[0]
            
            
            info_str = ', '.join([f"{col}: {val}" for col, val in zip(customer_info.index, customer_info.values)])
            
            return f"Information for customer ID {customer_id}: {info_str}"
        else:
            return f"No customer found with ID {customer_id}."

    
    try:
        
        if "average" in user_query and "income" in user_query:
            answer_data = data['Income'].mean()
            return f"The average income of customers is ${answer_data:.2f}."

       
        elif "income distribution" in user_query:
            return str(data['Income'].describe())
        
        
        elif "average spending" in user_query and "wines" in user_query:
            answer_data = data['MntWines'].mean()
            return f"The average spending on wines is ${answer_data:.2f}."
        
       
        elif "how many" in user_query and "phd" in user_query:
            answer_data = data[data['Education'] == 'PhD'].shape[0]
            return f"There are {answer_data} customers with a PhD."

        
        elif "response rate" in user_query and "last marketing campaign" in user_query:
            answer_data = data['Response'].mean() * 100
            return f"The response rate to the last marketing campaign is {answer_data:.2f}%."

        
        elif "spent more" in user_query and "1000" in user_query and "wines" in user_query:
            answer_data = data[data['MntWines'] > 1000].shape[0]
            return f"There are {answer_data} customers who have spent more than $1000 on wines."

       
        elif "customers were acquired" in user_query and "2013" in user_query:
            data['Dt_Customer'] = pd.to_datetime(data['Dt_Customer'])
            answer_data = data[data['Dt_Customer'].dt.year == 2013].shape[0]
            return f"{answer_data} customers were acquired in 2013."
        
        
        elif "percentage of customers" in user_query and "complaint" in user_query:
            answer_data = data['Complain'].mean() * 100
            return f"{answer_data:.2f}% of customers have made a complaint."

        else:
            return ("I'm sorry, I couldn't understand your query. "
                    "Can you please provide more details or try a different question?")
    
    except Exception as e:
        print(f"Debug: Error processing query: {str(e)}")
        return "Sorry, I encountered an error processing your request."


def style():
    st.markdown("""
        <style>
            .chatbot-container {
                color: #fff;
                background-color: #E1BEE7;
                font-family: Arial, sans-serif; /* Change the font family */
                font-size: 16px; /* Change the font size */
                border: 2px solid #6A1B9A; /* Add a border around the entire interface */
                border-radius: 10px; /* Add border radius for a rounded appearance */
                padding: 20px; /* Add padding to create some space between content and the border */
            }
            .stTextInput input {
                background-color: purple !important; /* Change query box background color */
            }
            .stTextInput>div>div>input {
                color: white !important;
            }
            .send-button {
                float: right; /* Move the button to the right */
            }
            button {
                color: #6A1B9A;
                background-color: #E1BEE7;
                border: solid 2px #6A1B9A;
            }
            .userText {
                color: #6A1B9A;
                background-color: #E1BEE7;
                padding: 20px;
                border-radius: 10px;
                display: inline-block;
                max-width: 80%;
            }
            .botText {
                color: #fff;
                background-color: #6A1B9A;
                padding: 20px;
                border-radius: 10px;
                display: inline-block;
                max-width: 80%;
            }
        </style>
        """, unsafe_allow_html=True)

style()


col1, col2 = st.columns([50, 200]) 


image_url = "/Users/lulali1/Downloads/Untitled design.png" 
col1.image(image_url, use_column_width=True, caption="Hi! I'm Rosie the Robot!")


with col2:
    st.title("Customer AI Chatbot")


user_input = st.text_input("Please enter your query:")


if st.button("Send"):
   
    if user_input:
        
        st.markdown(f"<p class='userText'> {user_input}</p>", unsafe_allow_html=True)
        
        
        response = process_query(user_input)

        
        st.markdown(f"<p class='botText'><b>Chatbot:</b> {response}</p>", unsafe_allow_html=True)
    else:
        st.warning("Query cannot be empty!")
