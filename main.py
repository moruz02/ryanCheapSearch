#there's a limit to the ryanair API request, maybe you have to wait a little bit bro!

import streamlit as st
import pandas as pd
import numpy as np

#fare una lista ordinata e stamparla tutta

from datetime import datetime, timedelta
from ryanair import Ryanair
from ryanair.types import Flight

api = Ryanair(currency="EUR")
st.set_page_config(page_title="Ryanair Cheap Search")

def elaborate(): 
    for day in range (int(fromDay), int(toDay)): 
        departure_date_from = departure_date_to = fromYear+"-"+fromMonth+"-"+str(day).zfill(2)
        for rit in range (day, int(toDay)+1):
            return_date_from = return_date_to = toYear+"-"+toMonth+"-"+str(rit).zfill(2)
            val = api.get_cheapest_return_flights(airport, departure_date_from, departure_date_to, return_date_from, return_date_to)
            if len(val) > 2:
                price = val[0].totalPrice
                if float(price) < bestPrice:
                    cheapestFlight = val[0]

    data = {
        "Origin": [cheapestFlight.outbound.originFull, cheapestFlight.inbound.originFull],
        "Origin IATA": [cheapestFlight.outbound.origin, cheapestFlight.inbound.origin],
        "Destination": [cheapestFlight.outbound.destinationFull, cheapestFlight.inbound.destinationFull],
        "Destination IATA": [cheapestFlight.outbound.destination, cheapestFlight.inbound.destination],
        "Flight Number": [cheapestFlight.outbound.flightNumber, cheapestFlight.inbound.flightNumber],
        "Date - Time": [cheapestFlight.outbound.departureTime, cheapestFlight.inbound.departureTime],
        "Price": [cheapestFlight.outbound.price, cheapestFlight.inbound.price]
    }

    df = pd.DataFrame(data)

    st.title("Il risultato della tua ricerca:")
    st.table(df)
    st.title("TOTAL PRICE: "+str(cheapestFlight.totalPrice))
    link = "https://www.ryanair.com/it/it/trip/flights/select?adults=1&teens=0&children=0&infants=0&dateOut="\
            +str(cheapestFlight.outbound.departureTime).split()[0]+"&dateIn="+str(cheapestFlight.inbound.departureTime).split()[0]+\
            "&isConnectedFlight=false&discount=0&promoCode=&isReturn=true&originIata="+cheapestFlight.outbound.origin+\
            "&destinationIata="+cheapestFlight.inbound.origin+"&tpAdults=1&tpTeens=0&tpChildren=0&tpInfants=0&"\
            "tpStartDate="+str(cheapestFlight.outbound.departureTime).split()[0]+"&tpEndDate="+str(cheapestFlight.inbound.departureTime).split()[0]+\
            "&tpDiscount=0&tpPromoCode=&tpOriginIata="+cheapestFlight.outbound.origin+"&tpDestinationIata="+cheapestFlight.inbound.origin

    st.write("Link al tuo viaggio: ")
    st.write(link)

airport = str(st.text_input("Inserisci il codice IATA del tuo aeroporto di partenza (ad es.: 'VCE', 'MXP', ecc.)",
                         max_chars=3)).upper()

col1, col2 = st.columns(2)
with col1:
    fromDate = str(st.date_input("Da: ", value=datetime.now().date()))
    fromDay = fromDate.split('-')[2]
    fromMonth = fromDate.split('-')[1]
    fromYear = fromDate.split('-')[0]
with col2:
    toDate = str(st.date_input("A: ", value=datetime.now().date()+timedelta(days=1)))
    toDay = toDate.split('-')[2]
    toMonth = toDate.split('-')[1]
    toYear = toDate.split('-')[0]

cheapestFlight = ""
bestPrice = 100000

if st.button("Cerca"):
    if not airport:
        st.warning("Inserisci un aeroporto di partenza!")
    else:
        if fromDate <= toDate:
            elaborate()
        else:
            st.markdown("<h1 style='text-align: center;'>Inserisci delle date valide!</h1>", unsafe_allow_html=True)

 # Trip(
 #  totalPrice=85.31, 
 #  outbound=Flight(departureTime=datetime.datetime(2023, 3, 12, 7, 30), flightNumber='FR5437', 
 #      price=49.84, currency='EUR', origin='DUB', originFull='Dublin, Ireland', destination='EMA', 
 #      destinationFull='East Midlands, United Kingdom'), 
 #  inbound=Flight(departureTime=datetime.datetime(2023, 3, 13, 7, 45), flightNumber='FR5438',
 #      price=35.47, origin='EMA', originFull='East Midlands, United Kingdom', destination='DUB', 
 #      destinationFull='Dublin, Ireland')
 # )
