import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import spacy
import os
import requests
import json


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
skill = st.text_input('Enter Skill :')
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

searched_cand=pd.read_json(search_cand_prfl.content)

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


st.dataframe(df1)
#st.dataframe(df2)

#footer {
#	
#	visibility: hidden;
#	
#	}

#footer:after {
#	content:'(c) Cogent Infotech'; 
#	visibility: visible;
#	display: block;
#	position: relative;
#	#background-color: red;
#	padding: 5px;
#	top: 2px;
#}