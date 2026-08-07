import json
import requests
from datetime import datetime

def generate_security_hub_finding(title: str, description: str, resource_type: str, resource_id: str) -> dict:
    now = datetime.utcnow().isoformat() + "Z"
    return {
        "version": "0",
        "id": "mock-event-id-1234",
        "detail-type": "Security Hub Findings - Imported",
        "source": "aws.securityhub",
        "account": "123456789012",
        "time": now,
        "region": "us-east-1",
        "resources": [f"arn:aws:securityhub:us-east-1:123456789012:hub/default"],
        "detail": {
            "findings": [
                {
                    "SchemaVersion": "2018-10-08",
                    "Id": f"arn:aws:securityhub:us-east-1:123456789012:subscription/mock/{resource_id}",
                    "ProductArn": "arn:aws:securityhub:us-east-1::product/aws/securityhub",
                    "GeneratorId": "aws-foundational-security-best-practices/v/1.0.0/EC2.2",
                    "AwsAccountId": "123456789012",
                    "Types": ["Software and Configuration Checks/Industry and Regulatory Standards"],
                    "FirstObservedAt": now,
                    "LastObservedAt": now,
                    "CreatedAt": now,
                    "UpdatedAt": now,
                    "Severity": {
                        "Label": "HIGH",
                        "Normalized": 70
                    },
                    "Title": title,
                    "Description": description,
                    "ProductFields": {},
                    "Resources": [
                        {
                            "Type": resource_type,
                            "Id": resource_id,
                            "Partition": "aws",
                            "Region": "us-east-1"
                        }
                    ],
                    "WorkflowState": "NEW",
                    "RecordState": "ACTIVE"
                }
            ]
        }
    }

def main():
    # Simulate an S3 bucket finding
    s3_payload = generate_security_hub_finding(
        title="S3.2 S3 buckets should prohibit public read access",
        description="This AWS control checks whether your S3 buckets allow public read access.",
        resource_type="AwsS3Bucket",
        resource_id="arn:aws:s3:::my-public-bucket-123"
    )

    # Simulate a Security Group finding
    sg_payload = generate_security_hub_finding(
        title="EC2.2 VPC default security groups should not allow inbound or outbound traffic",
        description="This control checks that the default security group of a VPC does not allow inbound or outbound traffic.",
        resource_type="AwsEc2SecurityGroup",
        resource_id="arn:aws:ec2:us-east-1:123456789012:security-group/sg-0123456789abcdef0"
    )

    url = "http://localhost:8000/api/ingestion/mock/sqs/push"

    print("Sending S3 Finding...")
    try:
        response = requests.post(url, json=s3_payload)
        print(f"Status: {response.status_code}, Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print(f"Failed to connect to {url}. Is the FastAPI server running?")

    print("\nSending Security Group Finding...")
    try:
        response = requests.post(url, json=sg_payload)
        print(f"Status: {response.status_code}, Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print(f"Failed to connect to {url}. Is the FastAPI server running?")

if __name__ == "__main__":
    main()
