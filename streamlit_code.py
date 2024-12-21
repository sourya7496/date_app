import streamlit as st
import pandas as pd
import time
import requests 
import page2

def stream_data_y():
    line= "Will you go out on a date?"
    for word in line.split(" "):
        yield word + " "
        time.sleep(0.2)

def stream_data_n():
    line= "Ohh sorry to bother you! :("
    for word in line.split(" "):
        yield word + " "
        time.sleep(0.2)

def get_place_id(address):
    api_key = st.secrets['api_keys']['api_key_g']   
    base_url= f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
     
    response = requests.get(base_url)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        if data['status'] == 'OK':
            # Extract some details from the response
            lat = data['results'][0]['geometry']['location']['lat']
            lng = data['results'][0]['geometry']['location']['lng']
            for component in data['results'][0]['address_components']:
                if "country" in component['types']:
                    country_long_name = component['long_name']
                    break
                else:
                    country_long_name= 'Country not found'
            place_id= data['results'][0]['place_id']
            print(f"Latitude: {lat}")
            print(f"Longitude: {lng}")
            print("Country:", country_long_name)
            print("Place ID: ", place_id)
        else:
            print("No places found.")
        return place_id, country_long_name
    else:
        print(f"Error: {response.status_code}")
        return 0, 'Not found'


def api_call(place_id):
# Define the base URL and parameters for the request
    api_key = st.secrets['api_keys']['api_key_g']  
    base_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
    # Send a GET request to the API
    response = requests.get(base_url)
    img_links_arr=[]
    author_arr=[]
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        if data['status'] == 'OK':
            # Extract some details from the response
            photos = data['result']['photos']  # Get the first place result
            for i in range((5)):
                link= photos[i]["html_attributions"]
                just_link= link[0].split('href="')[1].split('">')[0]
                author= link[0].split('href="')[1].split('">')[1].split('</a')[0]
                img_links_arr.append(just_link)
                author_arr.append(author)

        else:
            print("No places found.")
        return img_links_arr, author_arr
        
    else:
        print(f"Error: {response.status_code}")



##pl_id, coun= get_place_id('California')
##img_links_arr, author_arr= api_call(pl_id)
if 'button_pressed' not in st.session_state:
    st.session_state.button_pressed = False

st.set_page_config(page_title="Important Message!!", page_icon="❤️")

st.title("Hey there! I have an important message for you!")

st.write("There is something serious I want to share. ")
y=st.button("Yes I want to see")
n=st.button("No, I am least interested")
print('1')
x=1
if y:
    st.session_state.button_pressed= True

if st.session_state.button_pressed== True:
    st.write_stream(stream_data_y)
    page2.main()

if n:
    st.write_stream(stream_data_n)





