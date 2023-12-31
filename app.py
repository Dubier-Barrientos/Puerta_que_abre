import paho.mqtt.client as paho
import time
import streamlit as st
import json
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
import paho.mqtt.client as paho
import os

values = 0.0
act1="OFF"

def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)

        


broker="157.230.214.127"
port=1883
client1= paho.Client("ErnestoDoor")
client1.on_message = on_message

st.write(" !Hola, bienvenido a Eco-House! ")
st.text(" La casa con sistema de cerradura inteligente ")


image = Image.open('eco-house.jpg')
st.image(image, width=200)

stt_button = Button(label=" Open/Close the door ", width=200)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        #st.write(result.get("GET_TEXT"))
        client1.on_publish = on_publish                            
        client1.connect(broker,port)  
        message =json.dumps({"Act1":result.get("GET_TEXT").strip()})
        ret= client1.publish("voz_pedro", message)

        if result.get("GET_TEXT") == "Open":
            act1="ABRE"
            client1= paho.Client("ErnestoDoor")                           
            client1.on_publish = on_publish                          
            client1.connect(broker,port)  
            message =json.dumps({"Act1":act1})
            ret= client1.publish("puerta_de_ernesto", message)
 
            #client1.subscribe("Sensores")
        else:
            st.write('')

        if result.get("GET_TEXT") == "Close":
            act1="CIERRA"
            client1= paho.Client("ErnestoDoor")                           
            client1.on_publish = on_publish                          
            client1.connect(broker,port)  
            message =json.dumps({"Act1":act1})
            ret= client1.publish("puerta_de_ernesto", message)
          
            
        else:
            st.write('')

    
    try:
        os.mkdir("temp")
    except:
        pass




