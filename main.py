# from Services import SoapRate
from flask import make_response
from werkzeug.exceptions import HTTPException
from zeep import Client, Settings
from zeep.exceptions import Fault, TransportError, XMLSyntaxError
from zeep.helpers import serialize_object

import xml.etree.ElementTree as ET

settings = Settings(strict=False, xml_huge_tree=True)
client = Client('RateWS.wsdl', settings=settings)

def getShippingRates(params):
  headers = {
    'UPSSecurity': {
        'UsernameToken': {
            'Username': 'Usaprinting7925',
            'Password': 'Maryam262625'
        },

        'ServiceAccessToken': {
            'AccessLicenseNumber': '5D2181315D0C05CE'
        }

    }
  }

  # Create request dictionary
  requestDictionary = {
    "RequestOption": "Shop",
    "TransactionReference": {
        "CustomerContext": "Your Customer Context"
    }
  }

  # Create rate request dictionary
  rateRequestDictionary = {
    "Package": {
        "PackageWeight": {
            "UnitOfMeasurement": {
                "Code": "Lbs",
                "Description": "pounds"
            },
            "Weight": params['Weight'] # To be passed by frontend
        },
        "PackagingType": {
            "Code": "02",
            "Description": "Rate"
        }
    },
    "Service": params['Service'],
    "ShipTo": params['ShipTo'],
    "Shipper": {
        "Address": {
            "AddressLine": [
                "7925 Santa Monica Blvd.",
            ],
            "City": "West Hollywood",
            "CountryCode": "US",
            "PostalCode": "90046",
            "StateProvinceCode": "CA"
        },
        "Name": "USA PRINTING",
        "ShipperNumber": "520T1T"
    }
  }
  try:
    response = client.service.ProcessRate(_soapheaders=headers, Request=requestDictionary,
                                          Shipment=rateRequestDictionary)
    return serialize_object(response)

  except Fault as error:
      return ET.tostring(error.detail)

def getRates(params):
  try:
    response = getShippingRates(params)
    return response
  except:
      pass

def shipping(request):
  try:
    request_json = request.get_json()
    shippingRate = getRates(request_json)
  
    if request.method == 'OPTIONS':
      headers = {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST',
          'Access-Control-Allow-Headers': 'Content-Type',
          'Access-Control-Max-Age': '3600'
      }

      return ('', 204, headers)  
    
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    
    return ( shippingRate, 200, headers )
  except HTTPException as e:
      return e
