from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class AwsSecurityHubResourceDetails(BaseModel):
    AwsS3Bucket: Optional[Dict[str, Any]] = None
    AwsEc2SecurityGroup: Optional[Dict[str, Any]] = None
    # Add other resources as needed
    
class AwsSecurityHubResource(BaseModel):
    Type: str
    Id: str
    Partition: str
    Region: str
    Details: Optional[AwsSecurityHubResourceDetails] = None

class AwsSecurityHubSeverity(BaseModel):
    Label: str
    Normalized: int

class AwsSecurityHubFinding(BaseModel):
    SchemaVersion: str
    Id: str
    ProductArn: str
    GeneratorId: str
    AwsAccountId: str
    Types: List[str]
    FirstObservedAt: str
    LastObservedAt: str
    CreatedAt: str
    UpdatedAt: str
    Severity: AwsSecurityHubSeverity
    Title: str
    Description: str
    Remediation: Optional[Dict[str, Any]] = None
    ProductFields: Optional[Dict[str, str]] = None
    Resources: List[AwsSecurityHubResource]
    Compliance: Optional[Dict[str, Any]] = None
    WorkflowState: str
    RecordState: str

class EventBridgeDetail(BaseModel):
    findings: List[AwsSecurityHubFinding]

class EventBridgeEvent(BaseModel):
    version: str
    id: str
    detail_type: str = Field(alias="detail-type")
    source: str
    account: str
    time: datetime
    region: str
    resources: List[str]
    detail: EventBridgeDetail
    
    class Config:
        populate_by_name = True
