#import plotly.graph_objects as go
import pandas as pd
import streamlit as st
#import spacy
#import os
import requests
#import json
from io import BytesIO

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        #st.write(st.session_state["username"])
        #st.write(st.session_state["password"])
        if (
            #st.session_state["username"] in st.secrets["passwords"]
            #and st.session_state["password"]
            #== st.secrets["passwords"][st.session_state["username"]]
            
            st.session_state["password"]== 'test123' and st.session_state["username"]== 'user1'
            
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    #st.write("Here goes your normal Streamlit app...")
    #st.button("Click me")
            
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """


    auth_tokn=requests.get('https://api.jobdiva.com/api/authenticate',
                      params={'clientid':1245,
                              'username':'jobdiva.api@cogentinfo.com',
                             'password':'Pass@001'})



    tokn=auth_tokn.text

    csrf=requests.get('https://api.jobdiva.com/csrf')
    csrf=csrf.text[10:46]


    hdr={'Authorization':tokn,
        'X-CSRF-TOKEN': csrf}


    #st.title('Filter candidate records based on Skill: ')
    #Ask user to input Skill  and pass to parms

    #original_title = '<p style="font-family:Arial; color:Black; font-size: 30px; align:center;">Filter candidate records based on Skill</p>'
    #st.markdown(original_title, unsafe_allow_html=True)
    st.title('Filter candidates based on Skill')

    #skill = st.text_input('Enter Skill :', value='Java')
    #Instead of user typing out the skill present a dropdown 
    skill=st.selectbox('Enter a skill: ',('Java','Oracle','.Net','MS SQL Server',
                        'QA/Tester',
                        'Project Manager',
                        'Business Analyst',
                        'Enterprise Architect',
                        'Technical Writer',
                        'DBA',
                        'DevOps'))
    st.write('Your selected skill is: ',skill)

    quoted_skill=str(skill)
    #skill='.Net'
    print(skill)
    urlquery='https://api.jobdiva.com/api/jobdiva/searchCandidateProfile?maxreturned=10&candidateQuals={"catId": 28,"dcatNames": "'+quoted_skill+'"}'

    #Pull candidate detail
    #parms={
    #    'maxreturned':10
    #      ,
    #     'candidateQuals':
    #    {
    #            'catId': 28,
    #            'dcatNames': quoted_skill
    #           }
    #      }

    #payload = {'request':  json.dumps(parms) }

    #print(payload)

    search_cand_prfl=requests.post(urlquery,
                                  headers=hdr
                                  #params=parms,
                                  #params=payload

                           )

    searched_cand=pd.read_json(BytesIO(search_cand_prfl.content),orient='records')

    #searched_cand=pd.DataFrame(pd.read_json(search_cand_prfl.text),index=[0])

    df1 = searched_cand.replace({r'\s+$': '', r'^\s+': ''}, regex=True).replace(r'\n',  ' ', regex=True)

    #df2=df1['zipcode'].astype(object)
    #df2=df1.fillna()


    # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    #st.dataframe(searched_cand)

    st.dataframe(df1)
    #st.dataframe(df2)

