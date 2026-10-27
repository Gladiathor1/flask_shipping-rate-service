# Shipping Rate Service

A small Python serverless function that returns **UPS shipping rates** for a package. It calls the UPS Rating SOAP web service (using the WSDL/XSD files in this repo) in "Shop" mode, so a single request returns the available UPS services and their prices. It was written for the USA Printing e-commerce platform to show shipping costs at checkout.

## How it works

1. The front end sends a JSON request with the package weight, the destination address and the requested service.
2. `main.py` builds a UPS `RateRequest` — adding the UPS security header and the shipper's origin address — and sends it with the [zeep](https://docs.python-zeep.org/) SOAP client.
3. The UPS response is converted to JSON and returned with CORS headers so it can be called from a browser.

The entry point is the `shipping(request)` function, which follows the Google Cloud Functions (Flask request) signature and also handles CORS preflight (`OPTIONS`) requests.

## Request

`POST` with a JSON body:

```json
{
  "Weight": "5",
  "Service": { "Code": "03", "Description": "Ground" },
  "ShipTo": {
    "Name": "Jane Doe",
    "Address": {
      "AddressLine": ["123 Main St"],
      "City": "Los Angeles",
      "StateProvinceCode": "CA",
      "PostalCode": "90001",
      "CountryCode": "US"
    }
  }
}
```

The response is the serialized UPS `RateResponse`, which contains a `RatedShipment` entry for each available service. If UPS returns a fault, the fault detail XML is returned instead.

## Files

| File | Description |
| --- | --- |
| `main.py` | The function: builds the request, calls UPS, returns JSON |
| `RateWS.wsdl` | UPS Rating web-service definition |
| `RateWebServiceSchema.xsd`, `common.xsd`, `UPSSecurity.xsd`, `Error1.1.xsd` | UPS XML schemas used by the WSDL |
| `requirements.txt` | Python dependencies (`zeep`) |

## Setup

1. Get UPS developer credentials (username, password and access license number) from the [UPS Developer Portal](https://developer.ups.com/).
2. Put your credentials and shipper details in `getShippingRates` in `main.py` — ideally reading them from environment variables rather than committing them.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Deploy to Google Cloud Functions

```bash
gcloud functions deploy shipping --runtime python39 --trigger-http --allow-unauthenticated --entry-point shipping
```

### Run locally

```bash
pip install functions-framework
functions-framework --target shipping --debug   # http://localhost:8080
```
