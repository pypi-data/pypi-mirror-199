from typing import List
from uuid import UUID

from pydantic import validate_arguments

from bodosdk.api.base import BackendApi
from bodosdk.exc import (
    ResourceNotFound,
    ServiceUnavailable,
    UnknownError,
    ValidationError,
)
from bodosdk.models.job import (
    JobDefinition,
    JobResponse,
    JobExecution,
    JobCreateResponse,
    CreateBatchJobDefinition,
    BatchJobDefinitionResponse,
    JobConfigOverride,
    JobRunResponse,
    PaginationDetails,
    JobRunType,
)


# helper function to compose query string from query parameters
def build_query_string(args):
    if len(args) == 0:
        return ""
    query_string = "?"
    for k, v in args.items():
        if v is not None:
            query_string += f"{k}={v}&"

    return query_string


class JobApi(BackendApi):
    def __init__(self, *args, **kwargs):
        super(JobApi, self).__init__(*args, **kwargs)
        self._resource_url = "job"

    def create_job(self, job_definition: JobDefinition) -> JobCreateResponse:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            self.get_resource_url("v2"),
            data=job_definition.json(by_alias=True),
            headers=headers,
        )
        if str(resp.status_code).startswith("2"):
            # remap list of variables to dict
            json_data = resp.json()
            if isinstance(json_data["variables"], list):
                json_data["variables"] = {
                    k[0].strip(): k[1].strip()
                    for k in (item.split("=", 1) for item in json_data["variables"])
                }
            return JobCreateResponse(**json_data)
        if resp.status_code == 404:
            raise ResourceNotFound("Probably wrong workspace keys")
        if resp.status_code in (400, 422):
            raise ValidationError(resp.json())
        if resp.status_code == 503:
            raise ServiceUnavailable
        if resp.status_code == 409:
            raise ServiceUnavailable(
                "There is probably a job running on the cluster. \
                Please wait for the existing job to finish and retry again later."
            )
        raise UnknownError

    def delete_job(self, job_uuid) -> None:
        headers = self.get_auth_header()
        resp = self._requests.delete(
            f"{self.get_resource_url()}/{job_uuid}", headers=headers
        )
        if resp.status_code == 200:
            return
        if resp.status_code == 404:
            raise ResourceNotFound
        if resp.status_code == 503:
            raise ServiceUnavailable
        raise UnknownError(resp.content)

    def list_jobs(self) -> List[JobResponse]:
        headers = self.get_auth_header()
        resp = self._requests.get(
            f"{self.get_resource_url()}?withTasks=false", headers=headers
        )
        if resp.status_code == 503:
            raise ServiceUnavailable
        result = []
        for json_data in resp.json():
            # remap list of variables to dict
            if isinstance(json_data["variables"], list):
                json_data["variables"] = {
                    k[0]: k[1]
                    for k in (item.split("=", 1) for item in json_data["variables"])
                }
            result.append(JobResponse(**json_data))
        return result

    def get_job(self, uuid) -> JobResponse:
        headers = self.get_auth_header()
        resp = self._requests.get(f"{self.get_resource_url()}/{uuid}", headers=headers)
        if resp.status_code == 404:
            raise ResourceNotFound
        if resp.status_code == 503:
            raise ServiceUnavailable
        json_data = resp.json()
        if isinstance(json_data["variables"], list):
            # remap list of variables to dict
            json_data["variables"] = {
                k[0]: k[1]
                for k in (item.split("=", 1) for item in json_data["variables"])
            }
        return JobResponse(**json_data)

    def get_tasks(self, uuid) -> List[JobExecution]:
        headers = self.get_auth_header()
        resp = self._requests.get(
            f"{self.get_resource_url()}/{uuid}/tasks", headers=headers
        )
        if resp.status_code == 404:
            raise ResourceNotFound
        if resp.status_code == 503:
            raise ServiceUnavailable
        return [JobExecution(**data) for data in resp.json()]

    @validate_arguments
    def create_batch_job_definition(
        self, job_definition: CreateBatchJobDefinition
    ) -> BatchJobDefinitionResponse:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            f"{self.get_resource_url()}/batch_job_def",
            data=job_definition.json(by_alias=True),
            headers=headers,
        )
        if str(resp.status_code).startswith("2"):
            return BatchJobDefinitionResponse(**resp.json())
        # variables and args are already dicts
        if resp.status_code == 409:
            raise ResourceNotFound(
                "May have specified a default cluster which doesn't belong the workspace"
            )
        if str(resp.status_code).startswith("5"):
            raise ServiceUnavailable
        raise UnknownError(resp.content)

    @validate_arguments
    def delete_batch_job_definition(self, batch_job_definition_uuid: UUID) -> None:
        headers = self.get_auth_header()
        resp = self._requests.delete(
            f"{self.get_resource_url()}/batch_job_def/{batch_job_definition_uuid}",
            headers=headers,
        )
        if str(resp.status_code).startswith("2"):
            return
        if resp.status_code == 404:
            raise ResourceNotFound
        if str(resp.status_code).startswith("5"):
            raise ServiceUnavailable
        raise UnknownError(resp.content)

    # Todo: add query semantics for filtering
    @validate_arguments
    def list_batch_job_definitions(
        self,
        pagination_details: PaginationDetails = None,
    ) -> List[BatchJobDefinitionResponse]:
        args = locals()
        args.pop("self")
        headers = self.get_auth_header()
        resource_url = (
            f"{self.get_resource_url()}/batch_job_def{build_query_string(args)}"
        )
        resp = self._requests.get(resource_url, headers=headers)
        if str(resp.status_code).startswith("5"):
            raise ServiceUnavailable
        result = []
        for json_data in resp.json():
            result.append(BatchJobDefinitionResponse(**json_data))
        return result

    @validate_arguments
    def get_batch_job_definition(self, uuid: UUID) -> BatchJobDefinitionResponse:
        headers = self.get_auth_header()
        resp = self._requests.get(
            f"{self.get_resource_url()}/batch_job_def/{uuid}", headers=headers
        )
        if resp.status_code == 404:
            raise ResourceNotFound
        if str(resp.status_code).startswith("5"):
            raise ServiceUnavailable
        json_data = resp.json()
        return BatchJobDefinitionResponse(**json_data)

    @validate_arguments
    def update_batch_job_definition(
        self, uuid: UUID, config_override: JobConfigOverride
    ) -> BatchJobDefinitionResponse:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.patch(
            f"{self.get_resource_url()}/batch_job_def/{uuid}",
            data=config_override.json(by_alias=True),
            headers=headers,
        )
        if str(resp.status_code).startswith("2"):
            return BatchJobDefinitionResponse(**resp.json())
        if resp.status_code == 404:
            raise ResourceNotFound("Batch job definition not found")
        if resp.status_code == 409:
            raise ResourceNotFound(
                "May have specified a default cluster which doesn't belong the workspace"
            )
        if str(resp.status_code).startswith("5"):
            raise ServiceUnavailable
        raise UnknownError(resp.content)

    # Job Run APIs
    @validate_arguments
    def create_batch_job_run(self, job_definition: JobDefinition) -> JobRunResponse:
        headers = {"Content-type": "application/json"}
        headers.update(self.get_auth_header())
        resp = self._requests.post(
            f"{self.get_resource_url()}/run/batch",
            data=job_definition.json(by_alias=True),
            headers=headers,
        )
        if str(resp.status_code).startswith("2"):
            return JobRunResponse(**resp.json())
            # TODO (Ritwika) : confirm action for environment variables etc.
        if resp.status_code == 404:
            raise ResourceNotFound("Batch job definition not found")
        if resp.status_code == 409:
            raise ResourceNotFound(
                "May have specified a default cluster which doesn't belong the workspace"
            )
        if str(resp.status_code).startswith("5"):
            raise ServiceUnavailable
        raise UnknownError(resp.content)

    @validate_arguments
    def get_job_run(self, uuid: UUID, job_type: JobRunType = "BATCH") -> JobRunResponse:
        job_type_url_suffix = job_type.lower()
        headers = self.get_auth_header()
        resp = self._requests.get(
            f"{self.get_resource_url()}/run/{job_type_url_suffix}/{uuid}",
            headers=headers,
        )
        if resp.status_code == 404:
            raise ResourceNotFound
        if str(resp.status_code).startswith("5"):
            raise ServiceUnavailable
        json_data = resp.json()
        return JobRunResponse(**json_data)

    def cancel_batch_job_run(self, uuid) -> None:
        headers = self.get_auth_header()
        resp = self._requests.delete(
            f"{self.get_resource_url()}/run/batch/{uuid}", headers=headers
        )
        if resp.status_code == 404:
            raise ResourceNotFound
        if str(resp.status_code).startswith("5"):
            raise ServiceUnavailable
        return

    @validate_arguments
    def list_job_runs(
        self,
        job_type: JobRunType = None,
        batch_job_id=None,
        status=None,
        cluster_id=None,
        started_at=None,
        finished_at=None,
        pagination_details=None,
    ) -> List[JobRunResponse]:
        args = locals()
        args.pop("self")
        args.pop("job_type")
        query_string_args = dict(
            (key, args[key]) for key in list(args.keys()) if args[key]
        )
        headers = self.get_auth_header()
        job_type_url_suffix = None
        if job_type:
            job_type_url_suffix = job_type.lower()
        headers = self.get_auth_header()
        if job_type_url_suffix:
            resp = self._requests.get(
                f"{self.get_resource_url()}/run/{job_type_url_suffix}{build_query_string(query_string_args)}",
                headers=headers,
            )
        else:
            resp = self._requests.get(f"{self.get_resource_url()}/run", headers=headers)

        if str(resp.status_code).startswith("5"):
            raise ServiceUnavailable
        result = []
        for json_data in resp.json():
            result.append(JobRunResponse(**json_data))
        return result
