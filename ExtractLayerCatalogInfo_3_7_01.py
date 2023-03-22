"""
Title:          ExtractLayerCatalogInfo_3_7_01.py
Description:    This script traverses the supplied
                Layer Catalog site xml file and lists all the following
                information for any Layer in the site:
                - Layer URL
                - Layer Name
                - GXE Display Name
                - ServiceID
                  
Author:           Pete Smyth
Date:             21st March 2023
Required Modules: arcpy   Version 3.7(Installed with ArcGIS Pro)
                  xml (native)
                  requests (???)
                  csv (native)
                  time (native)

xml module source: https://docs.python.org/2/library/xml.etree.elementtree.html#module-xml.etree.ElementTree
                  
"""

import xml.etree.ElementTree as ET
import requests
import csv
from time import strftime, localtime

fileToRead = 'IMS_LC_Site_20230321.xml'


def getServiceID(serviceURL):
    '''Gets the ServiceID (itemID) for the requested service url
    
    Parameters
    ----------
    serviceURL : string
        The url of the service for which you need the Service ID

    Returns
    -------
    string
        A string of the ServiceID
    
    '''
    url = serviceURL
    headers = {'accept-encoding':'gzip, deflate, br', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'}
    params = {'f': 'pjson'}
    proxies={'https':'http://165.225.114.16:10170','http':'http://165.225.114.16:10170'}
    r = requests.get(url[:-2] + '/?',params=params,headers=headers,verify=True,proxies=proxies)
    ServiceInfoJSON = r.json()
    return ServiceInfoJSON['serviceItemId']
    

def getLayerInfoFromLayerCatalog(readfile):
    '''Gets the following attributes from a Geocortex Layer Catalog site:
        - Feature Layer (Service) Connection String
        - Feature Layer (Service) Display Name
        - Layer (service Layer) Display Name
        - Service Item ID (from the getServiceID function)
    
    Parameters
    ----------
    readfile : string
        The filename and path of the geocortex layer catalog site file
        for which you need the above listed attributes

    Uses
    ----
    getLayerInfoFromLayerCatalog : function
    
    Returns
    -------
    List
        A list of lists containing the Layer URL,Layer Name,
        GXE Display Name & ServiceID for each Feature Layer (Service)
        in the Layer Catalog
    
    '''
    tree = ET.parse(fileToRead)
    root = tree.getroot()
    layerInfo = []
    layerInfo.append(['Layer URL','Layer Name','GXE Display Name','ServiceID'])

    for child in root:
        count = 1
        for item in child:
            # print(item.tag)
            if item.tag == "MapServices":
                for featureLayer in item:
                    # print(featureLayer.tag,featureLayer.attrib['ConnectionString'],featureLayer.attrib['DisplayName'])
                    for info in featureLayer:
                        # print(info.tag)
                        if info.tag == "Layers":
                            for layer in info:
                                print(str(strftime("%Y%m%d_%H%M%S"))+ " - " + child.tag + " - " + item.tag + " - " + featureLayer.tag + " - " + info.tag + " - Processing Layer " + str(count))
                                # print(layer.tag, layer.attrib['DisplayName'])
                                line = []
                                line.append(featureLayer.attrib['ConnectionString'].replace('url=',''))
                                line.append(featureLayer.attrib['DisplayName'])
                                line.append(layer.attrib['DisplayName'])
                                line.append(getServiceID(featureLayer.attrib['ConnectionString'].replace('url=','')))
                                layerInfo.append(line)
                                count += 1
    return layerInfo



def main(outFile):
    with open(outFile, 'w', newline='') as f:
        w = csv.writer(f)
        layerCatalogInfo = getLayerInfoFromLayerCatalog(fileToRead)
        for line in layerCatalogInfo:
            w.writerow(line)
    


if __name__ == "__main__":
    print(str(strftime("%Y%m%d_%H%M%S - ")) + "Beginning Processing")
    outputfile = r"C:\Users\044231\Storage\Python\Results\LayerCatalogInfo_" + str(strftime("%Y%m%d_%H%M%S")) + ".csv"
    # calling main function
    main(outputfile)
    print(str(strftime("%Y%m%d_%H%M%S - ")) + "Finished Processing")
