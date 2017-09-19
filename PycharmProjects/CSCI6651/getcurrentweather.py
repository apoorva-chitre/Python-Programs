#!/usr/local/bin/python3

import sys
import json
import xml.etree.ElementTree as et
import urllib.request

if len(sys.argv) != 2 :
	print("Missing or extra information - give a single zipcode.")
else :
	if len(sys.argv[1]) == 5 and sys.argv[1].isdigit() :
		request = "http://api.openweathermap.org/data/2.5/weather?zip="+sys.argv[1]+",us&units=imperial&mode=json&APPID=b0d45b8cc18faf92d77e9825fd5aae74"	
		request2 = "http://api.openweathermap.org/data/2.5/weather?zip="+sys.argv[1]+",us&units=imperial&mode=xml&APPID=b0d45b8cc18faf92d77e9825fd5aae74"	

		try :
			urlobject = urllib.request.urlopen(request)
			urlobject2 = urllib.request.urlopen(request2)
		except BaseException as e :
			print("Error contacting server:", e)

		if urlobject.getcode() == 200 :
			jsonresponse = urlobject.read()
			jsonresponse = jsonresponse.decode("utf-8")
			#print(jsonresponse)

			jsonobject = json.loads(jsonresponse)
			#print(jsonobject)

			temperature = jsonobject['main']['temp']
			humidity = jsonobject['main']['humidity']
			pressure = jsonobject['main']['pressure']
			windspeed = jsonobject['wind']['speed']
			winddir = jsonobject['wind']['deg']

			windnames = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N']
			winddirname = windnames[int((winddir + 11.25)/22.5)]
			place = jsonobject['name']

			print("The current weather conditions for", place)
			print("Temperature =", temperature, "degrees Fahrenheit")
			print("Humidity =", humidity, "%")
			print("Barometric pressure =", pressure, "Hectopascals")
			print("Wind is at", windspeed, "m/h from the", winddirname)

			xmlresponse = urlobject2.read()
			xmlresponse = xmlresponse.decode("utf-8")
			#print(xmlresponse)

			xmlobject = et.fromstring(xmlresponse)
			#print(xmlobject)
			#print(xmlobject.tag, xmlobject.text, xmlobject.attrib)
			#for subobject in xmlobject.iter() :
				#print(subobject.tag, subobject.text, subobject.attrib)
			#print(xmlobject[0].tag, xmlobject[0].text, xmlobject[0].attrib)

			#temperature = xmlobject[1].attrib['value']
			#humidity = xmlobject[2].attrib['value']
			#pressure = xmlobject[3].attrib['value']
			#windspeed = xmlobject[4][0].attrib['value']
			#winddirname = xmlobject[4][2].attrib['code']
			#place = xmlobject[0].attrib['name']

			temperature = xmlobject.find('temperature').attrib['value']
			humidity = xmlobject.find('humidity').attrib['value']
			pressure = xmlobject.find('pressure').attrib['value']
			windspeed = xmlobject.find('wind').find('speed').attrib['value']
			winddirname = xmlobject.find('wind').find('direction').attrib['code']
			place = xmlobject.find('city').attrib['name']

			print("The current weather conditions for", place)
			print("Temperature =", temperature, "degrees Fahrenheit")
			print("Humidity =", humidity, "%")
			print("Barometric pressure =", pressure, "Hectopascals")
			print("Wind is at", windspeed, "m/h from the", winddirname)
		else :
			print("Bad status code:", urlobject.getcode())
	else :
		print("Bad zip code.")

