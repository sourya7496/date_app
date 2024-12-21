import streamlit as st
import pandas as pd
import time
import requests

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

def stream_data_success():
    line= "Letsss Goooo!!"
    for word in line.split(" "):
        yield word + " "
        time.sleep(0.1)

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

def get_place_photo(photo_reference, api_key):
    # Construct the image URL using the photo reference and API key
    url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_reference}&key={api_key}"
    return url

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
            print(photos)
            for i in range((5)):
                link= photos[i]["html_attributions"]
                photo_ref= photos[i]["photo_reference"]
                urls= get_place_photo(photo_ref, api_key)
                author= link[0].split('href="')[1].split('">')[1].split('</a')[0]
                img_links_arr.append(urls)
                author_arr.append(author)

        else:
            print("No places found.")
        return img_links_arr, author_arr
        
    else:
        print(f"Error: {response.status_code}")

def main():
    print('2')
    choice = st.radio(
    "(Please do not say a No 😀)",
    ("Yes!!!", "No"), index=None)
    ##if st.button("Yes!!!"):
    if choice=='Yes!!!':
        input_text= st.text_input("Where do you want to go on a date? 😉")
        print('3')
        if len(input_text)>0:
            pl_id, coun= get_place_id(input_text)
            img_links_arr, author_arr= api_call(pl_id)
            st.write_stream(stream_data_success)
            if len(img_links_arr)>0:
                for i in range(len(img_links_arr)):
                    st.image(img_links_arr[i], caption=author_arr[i],use_container_width=True)
                st.write("Which ones would you want to visit with me?")
            else:
                st.write("Why do you give wrong places here? :()")

            
