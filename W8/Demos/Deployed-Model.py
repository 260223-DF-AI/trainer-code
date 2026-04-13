# could run http reqests - anything can use http
# could run boto3 to talk to aws - al little more fundamental
# could make a predictor (sagemake SDK - python - heavyweight package)

import boto3
import json
import sagemaker
import time
from sagemaker.predictor import Predictor
from sagemaker.serializers import JSONSerializer
from sagemaker.deserializers import JSONDeserializer

def prediction_with_sagemaker(input_data, endpoint_name):
    print("Predicting with SageMaker SDK...")
    predictor = Predictor(
        endpoint_name=endpoint_name,
        serializer=JSONSerializer(),
        deserializer=JSONDeserializer()
        )
    
    response = predictor.predict(input_data)
    print(f"Response: {response}")
    predictor.delete_endpoint()

def prediction_with_boto3(input_data, endpoint_name):
    print("Predicting with Boto3...")
    
    client = boto3.client('sagemaker-runtime')

    payload = json.dumps(input_data)

    response = client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='application/json',
        Body=payload
    )

    result_body = response['Body'].read().decode('utf-8')
    result = json.loads(result_body)

    print(f"Response: {result}")    


def main():
    input_data = [17, 5, -40]
    endpoint_name = "ThisIsMyEndpoint,YouCantHaveIt!" # You generally don't want to leave this in your repo either.
    

    start = time.time()
    prediction_with_sagemaker(input_data, endpoint_name)
    print(f"Time: {time.time() - start}")

    # start = time.time()
    # prediction_with_boto3(input_data, endpoint_name)
    # print(f"Time: {time.time() - start}")

if __name__ == "__main__":
    print("Starting...")
    main()
    print("Goodbye!")