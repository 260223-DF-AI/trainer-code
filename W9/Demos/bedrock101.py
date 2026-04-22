"""
Verify AWS Bedrock Access
LangChain Version: v1.0+
"""
import boto3

def verify_bedrock_access():
    """Test that Bedrock is accessible with current credentials."""
    # Create Bedrock client
    bedrock = boto3.client(
        service_name='bedrock',
        region_name='us-east-1'  # Adjust to your region
    )
    
    # List available foundation models
    response = bedrock.list_foundation_models()
    
    print("Available Bedrock Models:")
    print("-" * 50)
    for model in response['modelSummaries']:
        print(f"  {model['modelId']}")
        print(f"    Provider: {model['providerName']}")
        print(f"    Input: {model['inputModalities']}")
        print(f"    Output: {model['outputModalities']}")
        print()

if __name__ == "__main__":
    verify_bedrock_access()