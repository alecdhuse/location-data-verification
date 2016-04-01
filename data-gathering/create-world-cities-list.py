import json
import requests
import sys
import urllib, urllib2
import xml.etree.ElementTree as ET

api_url     = "http://overpass-api.de/api/interpreter"
output_file = "/Users/dhuse/Desktop/world_places.css"

try:
    progress = 0.0
    write_file = open(output_file,'w')
    
    for lat in range(-90, 90):
        for lng in range (-180, 180):
            
            bounds = '(' + str(lat) + ',' + str(lng) + ',' + str(lat + 1) + ',' + str(lng + 1) + ')'
            query  = '( node ["place"="borough"] ' + bounds + '; node ["place"="city"] ' + bounds + '; node ["place"="hamlet"] ' + bounds + '; node ["place"="municipality"] ' + bounds + '; node ["place"="neighbourhood"] ' + bounds + '; node ["place"="quarter"] ' + bounds + '; node ["place"="suburb"] ' + bounds + '; node ["place"="town"] ' + bounds + '; node ["place"="village"] ' + bounds + '; ); (._;>;); out;'

            data_for_api = urllib.urlencode({
                'data' : query
            })

            response = urllib2.urlopen(api_url, data_for_api).read()
            progress = progress + 0.001
            
            #Read Response
            response_data = response
            root = ET.fromstring(response_data)

            for child in root.iter('node'):
                place_attrs = child.attrib
                place_name  = "(unknown name)"               
                place_lat   = place_attrs.get('lat')
                place_lng   = place_attrs.get('lon')
                
                for tag_k in child:
                    if (tag_k.attrib.get('k') == 'name'):
                        place_name = tag_k.attrib.get('v') 
                        break

                css_line = place_name + "," + str(place_lat) + "," + str(place_lng) + "\n"
                write_file.write(css_line) 

            print str(progress) + "% complete."
        
except:
    error = sys.exc_info()[0]
    print "Script Error"
    print error

write_file.close()
print "Script finished"
    
