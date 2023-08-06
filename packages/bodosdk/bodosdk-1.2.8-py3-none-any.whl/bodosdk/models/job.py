import enum
from datetime import datetime
from typing import Optional, Dict, Union, List
from uuid import UUID

import pydantic
from pydantic import Field

from bodosdk.models.base import JobStatus, TaskStatus, CamelCaseBase


class JobClusterDefinition(CamelCaseBase):
    instance_type: str = Field(..., alias="instanceType")
    workers_quantity: int = Field(..., alias="workersQuantity")
    accelerated_networking: bool = Field(..., alias="acceleratedNetworking")
    image_id: Optional[str] = Field(None, alias="imageId")
    bodo_version: Optional[str] = Field(None, alias="bodoVersion")
    instance_role_uuid: Optional[str] = Field(None, alias="instanceRoleUUID")
    availability_zone: Optional[str] = Field(None, alias="availabilityZone")
    aws_deployment_subnet_id: Optional[str] = Field(None, alias="awsDeploymentSubnetId")
    custom_tags: Optional[Dict[str, str]] = Field(None, alias="customTags")


class JobCluster(pydantic.BaseModel):
    uuid: Union[str, UUID]


class JobSourceType(enum.Enum):
    GIT = "GIT"
    S3 = "S3"
    WORKSPACE = "WORKSPACE"


class GitRepoSource(CamelCaseBase):
    type: JobSourceType = Field(JobSourceType.GIT, const=True)
    repo_url: str = Field(..., alias="repoUrl")
    reference: Optional[str] = ""
    username: str
    token: str


class S3Source(CamelCaseBase):
    type: JobSourceType = Field(JobSourceType.S3, const=True)
    bucket_path: str = Field(..., alias="bucketPath")
    bucket_region: str = Field(..., alias="bucketRegion")


class WorkspaceSource(pydantic.BaseModel):
    type: JobSourceType = Field(JobSourceType.WORKSPACE, const=True)
    path: str


class JobDefinition(CamelCaseBase):
    name: str
    args: str
    source_config: Union[GitRepoSource, S3Source, WorkspaceSource] = Field(
        ..., alias="sourceConfig"
    )
    cluster_object: Union[JobClusterDefinition, JobCluster] = Field(
        ..., alias="clusterObject"
    )
    variables: Dict = Field(default_factory=dict)
    timeout: Optional[int] = 120
    retries: Optional[int] = 0
    retries_delay: Optional[int] = Field(0, alias="retriesDelay")
    retry_on_timeout: Optional[bool] = Field(False, alias="retryOnTimeout")


class JobClusterResponse(CamelCaseBase):
    uuid: Optional[str] = None
    name: str
    instance_type: str = Field(..., alias="instanceType")
    workers_quantity: int = Field(..., alias="workersQuantity")
    accelerated_networking: bool = Field(..., alias="acceleratedNetworking")
    bodo_version: Optional[str] = Field(None, alias="bodoVersion")
    image_id: str = Field(..., alias="imageId")


class JobResponse(CamelCaseBase):
    uuid: UUID
    name: str
    status: JobStatus
    schedule: datetime
    command: str
    variables: Dict
    workspace_path: Optional[str] = Field(None, alias="workspacePath")
    workspace_reference: Optional[str] = Field(None, alias="workspaceReference")
    cluster: Optional[JobClusterResponse] = None


class JobCreateResponse(CamelCaseBase):
    uuid: UUID
    status: JobStatus
    name: str
    args: str
    variables: Dict
    source_config: Union[GitRepoSource, S3Source, WorkspaceSource] = Field(
        ..., alias="sourceConfig"
    )
    cluster_config: Union[JobClusterDefinition, JobCluster] = Field(
        ..., alias="clusterConfig"
    )
    cluster: Optional[JobClusterResponse] = None
    variables: Dict = Field(default_factory=dict)
    timeout: Optional[int] = 120
    retries: Optional[int] = 0
    retries_delay: Optional[int] = Field(0, alias="retriesDelay")
    retry_on_timeout: Optional[bool] = Field(False, alias="retryOnTimeout")


class JobExecution(CamelCaseBase):
    uuid: UUID
    status: TaskStatus
    logs: str
    modify_date: datetime = Field(..., alias="modifyDate")
    created_at: datetime = Field(..., alias="createdAt")


# New source definitions per the new API.
class GitDef(CamelCaseBase):
    """
    Git repository source definition.

    ...

    Attributes
    ----------
    repo_url: str
        Git repository URL.

    reference: Optional[str]
        Git reference (branch, tag, commit hash). (Default: "")

    username: str
        Git username.

    token: str
        Git token.

    """

    repo_url: str = Field(..., alias="repoUrl")
    reference: Optional[str] = ""
    username: Optional[str]
    token: Optional[str]


class S3Def(CamelCaseBase):
    """
    S3 source definition.

    ...

    Attributes
    ----------
    bucket_path: str
        S3 bucket path.

    bucket_region: str
        S3 bucket region.

    """

    bucket_path: str = Field(..., alias="bucketPath")
    bucket_region: str = Field(..., alias="bucketRegion")


class WorkspaceDef(CamelCaseBase):
    """
    Workspace source definition.

    ...

    Attributes
    ----------
    path: str
        Workspace path.
    """

    path: str


class JobSource(CamelCaseBase):
    """
    Job source.

    ...

    Attributes
    ----------
    type: JobSourceType
        Job source type.

    definition: Union[GitDef, S3Def, WorkspaceDef]
        Job source definition.
    """

    type: JobSourceType
    definition: Union[GitDef, S3Def, WorkspaceDef] = Field(..., alias="def")


class RetryStrategy(CamelCaseBase):
    """
    Retry strategy for a job.

    ...

    Attributes
    ----------
    num_retries: int
        Number of retries for a job. (Default: 0)

    delay_between_retries: int
        Delay between retries in minutes. (Default: 1)

    retry_on_timeout: bool
        Retry on timeout. (Default: False)

    """

    num_retries: int = Field(0, alias="numRetries")
    delay_between_retries: int = Field(1, alias="delayBetweenRetries")  # in minutes
    retry_on_timeout: bool = Field(False, alias="retryOnTimeout")


class SourceCodeType(enum.Enum):
    PYTHON = "PYTHON"
    IPYNB = "IPYNB"
    SQL = "SQL"


class JobConfig(CamelCaseBase):
    """
    Job configuration.

    ...

    Attributes
    ----------
    source: JobSource
        Job source.

    source_code_type: SourceCodeType
        Job source code type.

    sourceLocation: str
        Job source location.

    args: Union[str, Dict]
        Job arguments. (Default: {})

    retry_strategy: RetryStrategy
        Job retry strategy. (Default: {num_retries: 0, delay_between_retries: 1, retry_on_timeout: False})

    timeout: int
        Job timeout in minutes. (Default: 60)

    env_vars: Dict
        Job environment variables. (Default: {})

    """

    source: JobSource
    source_code_type: SourceCodeType = Field(..., alias="type")
    sourceLocation: str
    args: Union[str, Dict] = Field(default_factory=dict)
    retry_strategy: RetryStrategy = Field(RetryStrategy(), alias="retryStrategy")
    timeout: int = 60
    env_vars: Dict = Field(default_factory=dict, alias="envVars")


class JobConfigOverride(CamelCaseBase):
    """
    Job configuration override.

    ...

    Attributes
    ----------
    source: Optional[JobSource]
        Job source.

    type: Optional[SourceCodeType]
        Job source code type.

    sourceLocation: Optional[str]
        Job source location.

    args: Optional[Union[str, Dict]]
        Job arguments. (Default: {})

    retry_strategy: Optional[RetryStrategy]
        Job retry strategy. (Default: {num_retries: 0, delay_between_retries: 1, retry_on_timeout: False})

    timeout: Optional[int]
        Job timeout in minutes. (Default: 60)

    env_vars: Optional[Dict]
        Job environment variables. (Default: {})
    """

    source: Optional[JobSource]
    type: Optional[SourceCodeType]
    sourceLocation: Optional[str]
    args: Optional[Union[str, Dict]] = Field(default_factory=dict)
    retry_strategy: Optional[RetryStrategy] = Field(
        RetryStrategy(), alias="retryStrategy"
    )
    timeout: Optional[int] = 60
    env_vars: Optional[Dict] = Field(default_factory=dict, alias="envVars")


class CreateBatchJobDefinition(CamelCaseBase):
    """
    Batch job definition.

    ...

    Attributes
    ----------
    description: str
        Job definition description.

    config: JobConfig
        Job configuration.

    cluster_config: JobClusterDefinition
        Job cluster configuration.

    clusterUUID: Optional[str]
        Job cluster.
    """

    name: str
    description: str
    config: JobConfig
    cluster_config: JobClusterDefinition = Field(..., alias="clusterConfig")
    clusterUUID: Optional[str] = None  # Todo(Ritwika): Confirm


class JobRunType(str, enum.Enum):
    BATCH = "BATCH"
    INTERACTIVE = "INTERACTIVE"


class JobRunStatus(enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    CANCELLING = "CANCELLING"


class JobRunResponse(CamelCaseBase):
    """
    Job run response.

    ...

    Attributes
    ----------
    uuid: UUID
        Job run ID.

    name: str
        Job run name.

    clusterUUID: UUID
        Job run cluster ID.

    type: JobRunType
        Job run type.

    config: JobConfig
        Job run configuration.

    submittedAt: datetime
        Job run submission time.

    finishedAt: datetime
        Job run finish time.

    startedAt: datetime
        Job run start time.

    status: JobRunStatus
        Job run status.

    batchJobDefinitionConfigOverrides: Optional[JobConfigOverride]
        Job run batch job definition configuration overrides.

    numRetriesUsed: int
        Number of retries used.

    lastHealthCheck: Optional[datetime]
        Job run last health check.

    lastKnownActivity: Optional[datetime]
        Job run last known activity.

    """

    uuid: UUID
    name: str
    clusterUUID: UUID = Field(..., alias="clusterUUID")
    type: JobRunType
    config: JobConfig
    submittedAt: datetime = Field(..., alias="submittedAt")
    finishedAt: datetime = Field(..., alias="finishedAt")
    startedAt: datetime = Field(..., alias="startedAt")
    status: JobRunStatus
    batchJobDefinitionConfigOverrides: Optional[JobConfigOverride]
    numRetriesUsed: int = Field(..., alias="numRetriesUsed")
    lastHealthCheck: Optional[datetime] = Field(..., alias="lastHealthCheck")
    lastKnownActivity: Optional[datetime] = Field(..., alias="lastknownActivity")


class BatchJobDefinitionResponse(CamelCaseBase):
    """
    Batch job definition response.

    ...

    Attributes
    ----------
    job_def_id: UUID
        Job definition ID.

    name: str
        Job definition name.

    description: str
        Job definition description.

    config: JobConfig
        Job configuration.

    clusterConfig: JobClusterDefinition
        Job cluster configuration.

    clusterUUID: Optional[str]
        Job cluster UUID.

    created_by: str
        Job definition creator.

    """

    job_def_id: UUID = Field(..., alias="uuid")
    name: str
    description: str
    config: JobConfig
    clusterConfig: JobClusterDefinition = Field(..., alias="clusterConfig")
    clusterUUID: Optional[str]  # Todo(Ritwika): Confirm
    created_by: str = Field(..., alias="createdBy")
    job_runs: List[JobRunResponse] = Field(default_factory=list, alias="jobRuns")
    # Run related fields
    # Rules related fields


class PaginationOrder(str, enum.Enum):
    ASC = "ASC"
    DESC = "DESC"


class PaginationDetails(CamelCaseBase):
    """
    Pagination details.

    ...

    Attributes
    ----------
    page_size: int
        Total number of items on page.

    page: int
        Offset of the current page.

    order: PaginationOrder
        order of the page.

    """

    page_size: int = Field(5, alias="pageSize")
    page: int = Field(1)
    order: PaginationOrder = Field(PaginationOrder.ASC)
