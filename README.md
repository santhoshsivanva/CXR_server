# CXR Server
The CXR Server is a server-side application designed to process chest X-ray images and detect signs of COVID-19 using machine learning. The application is built using Flask, a popular Python web framework, and is hosted on an EC2 AWS instance. The CXR images are stored in an S3 bucket, which is accessed through the application.

# API Website
The server-side application is hosted on the following website: [covidapiss.site](https://covidapiss.site/)

# Usage
To use the CXR server, send a POST request to the server's API endpoint with a JSON payload containing the image's filename, which is stored on the S3 bucket. The server will respond like covid or not.

```python
import requests
import json

url = 'http://covidxapiss.site/'

filename = 'patient001.jpg'

data = {'filename': filename}

response = requests.post(url, json=data)

if response.status_code == 200:
    cxr_detect = response.text
    # process the CXR image as required
    
else:
    print('Failed to get CXR image from server.')
```

# Our deep learning Model
Using densenet121 with PEPX design architecture.

Our team is currently working on a research paper 

# Deployement Diagram
 ![Architecture diagram for deployement](https://covidapiss.s3.jp-tok.cloud-object-storage.appdomain.cloud/Untitled%20Diagram.drawio%20(2).png) 

# License
This project is licensed under the MIT License. See the LICENSE file for details.
