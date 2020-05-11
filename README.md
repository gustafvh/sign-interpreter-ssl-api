# Sign Interpreter Application API for Swedish Sign Language
Deep Neural Network for predicting Swedish Sign Language Signs that utilises CNN and Transfer Learning. Contains Backend Python code for a Flask Server API. Has a single endpoint ```(/predict)``` in which a binary encoded image is accepted via a TLS-encrypted HTTP POST-request. The models top three predictions for that image, with respective confidence in percent, is returned as a response. 

By [Gustaf Halvardsson](https://github.com/gustafvh) & [Johanna Peterson](https://github.com/johannakin) 

## Technologies
- Written in **Python3** using **Flask**
- Containerised using **Docker**.
- Deployed as **Kubernetes** pod on **Google Kubernetes Engine** to avoid pre-loading model on every request.

## Endpoint

All endpoints originate from the domain: ```https://sign-interpreter.com/* ```

```(/predict)``` 

**Input:** Binary Encoded Image 

**Output:** Predictions in the following format
```
{
  "predictions": [
    {
      "confidence": 97.96156883,
      "letter": "A"
    },
    {
      "confidence": 1.00027621,
      "letter": "O"
    },
    {
      "confidence": 0.68401303,
      "letter": "S"
    }
  ],
  "success": true
}
```


## Frontend & Model used
This API accompanies a seperated frontend in React that we have also written. It also contains the neural network used. 
You can view that frontend and model repository here: https://github.com/gustafvh/SignInterpreterSSL

## Architecture

<img src="./cloud-architecture.png" alt="cloud-architecture"
	title="cloud-architecture" width="600" />
  
In order to make fast predictions, the back end API was deployed from a Docker image in a Kubernetes cluster via Googles Kubernetes Engine as an always-running service. This way the model was pre-loaded on the server to avoid costly operations for every request. To be able to handle TLS-encrypted requests, some additional components were needed. 

Firstly, a trusted SSL-certificate was issued via GCS and connected to a domain name (sign-interpreter.com). The domain name was issued via Amazon Route 53 that served as the outer endpoint for the API. The domain name was then configured with DNS A-record to point to the IP-address of the ingress-controller which was hosted as a service on GCS. 

The ingress controller handled all incoming requests, and by using its verified certificate, it was used as a proxy to forward the request to another internal GCS-service, a load-balancer. The load-balancer was used to split the incoming traffic between three nodes that independently handled requests as well as exposed the nodes to the ingress-controller. The nodes were contained in a Kubernetes cluster to handle workload scaling. One out of three nodes was used to handle the request and return the prediction which was passed back as a response to the client.

Try the app here: https://sign-interpreter-ssl.herokuapp.com/
