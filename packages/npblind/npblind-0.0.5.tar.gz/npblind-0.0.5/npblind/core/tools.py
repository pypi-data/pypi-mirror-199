import logging
import os
from typing import Optional, Union

import google.cloud.logging
from google.api_core import exceptions
from google.api_core.retry import Retry, if_exception_type
from google.cloud import datacatalog_v1, datacatalog_v1beta1
from google.cloud.bigquery import SchemaField, Table
from google.cloud.dlp_v2 import DlpServiceClient
from npgbq import NPGBQ

_MY_RETRIABLE_TYPES = (
    exceptions.TooManyRequests,  # 429
    exceptions.InternalServerError,  # 500
    exceptions.BadGateway,  # 502
    exceptions.ServiceUnavailable,  # 503
)


class NPBlind(object):
    def __init__(self, project_id, gcp_service_account_path: Union[str, None] = None):
        self.project_id = project_id
        self.resource_id = f"projects/{project_id}"
        self.path_json_key = gcp_service_account_path
        self.__add_environment()
        self.client = self.__get_client()
        self.client_ptc = self.___get_policy_tag_manager_client()
        self.client_ptc_beta = self.___get_policy_tag_manager_client_beta()
        self.client_gbq = NPGBQ(
            project_id=project_id, gcp_service_account_path=gcp_service_account_path
        )

    def __add_environment(self):
        if self.path_json_key:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.path_json_key

    def __get_client(self) -> DlpServiceClient:
        client = google.cloud.logging.Client(project=self.project_id)
        client.setup_logging(log_level=logging.INFO)
        dlp = DlpServiceClient()
        return dlp

    def ___get_policy_tag_manager_client(self):
        # todo try PolicyTagManagerClient in async version
        return datacatalog_v1.PolicyTagManagerClient()

    def ___get_policy_tag_manager_client_beta(self):
        # todo try PolicyTagManagerClient in async version
        return datacatalog_v1beta1.PolicyTagManagerClient()

    # ================================= methods =================================

    def create_taxonomy(
        self, taxonomy_id: str = "my-taxonomy", location_id: str = "asia-southeast1"
    ):
        parent = self.client_ptc.common_location_path(self.project_id, location_id)
        taxonomy = datacatalog_v1.Taxonomy()
        taxonomy.display_name = taxonomy_id  # type: ignore
        taxonomy.description = "This Taxonomy represents ..."  # type: ignore
        try:
            taxonomy = self.client_ptc.create_taxonomy(parent=parent, taxonomy=taxonomy)
        except Exception as e:
            print(f"The taxonomy_id={taxonomy_id} is already exists")
            return False
        else:
            print(f"Created taxonomy {taxonomy.name}")
            return True

    # create a policy tag under target taxonomy in Google Cloud Data Catalog
    # TODO[2023-03-27 14:57]: Make this method works
    def create_policy_tag(
        self,
        taxonomy_id: str,
        policy_tag_id: str,
        description: str = "This Policy Tag represents ...",
        location_id: str = "asia-southeast1",
    ):
        parent = self.client_ptc.common_location_path(self.project_id, location_id)
        # create a policy tag
        policy_tag = datacatalog_v1.PolicyTag()
        policy_tag.name = policy_tag_id # type: ignore
        policy_tag.display_name = f"description_{policy_tag_id}" # type: ignore
        policy_tag.description = description # type: ignore
        policy_tag2 = datacatalog_v1.PolicyTag(
            name=policy_tag_id,
            display_name=f"description_{policy_tag_id}",
            description=description,
        )
        if policy_tag == policy_tag2:
            print("hi")
        request = datacatalog_v1.CreatePolicyTagRequest(
            parent=parent, policy_tag=policy_tag
        )
        self.client_ptc.create_policy_tag(request=request)
        request = datacatalog_v1.CreatePolicyTagRequest()

    def get_taxonomy_data(self, taxonomy_id, location_id):
        full_parent_id = self.__get_taxonomy_parent(taxonomy_id, location_id)
        request = datacatalog_v1.ListPolicyTagsRequest(parent=full_parent_id)
        response = self.client_ptc.list_policy_tags(request=request)._response.policy_tags
        taxonomy_data = {}
        for i in response: # type: ignore
            taxonomy_data[i.display_name] = {
                "id": i.name,
                "description": i.description,
                "parent": i.parent_policy_tag,
                "child": i.child_policy_tags,
            }
        return taxonomy_data

    def __get_taxonomy_parent(self, taxonomy_id, location_id):
        return (
            f"projects/{self.project_id}/locations/{location_id}/taxonomies/{taxonomy_id}"
        )

    def find_policy_tag_id(self, taxonomy_data, policy_tag_id):
        # this may give you an error if the tree is too deep
        # TODO[2023-03-20 16:23]: Improve the logic of finding policy tag
        for k, v in taxonomy_data.items():
            if policy_tag_id in v["id"]:
                return v["id"]
        raise ValueError(f"policy_tag_id={policy_tag_id} is not found")

    def update_tag(self, col, tag_config, taxonomy_data):
        if isinstance(tag_config, str):
            policy_tag_id_full = self.find_policy_tag_id(taxonomy_data, tag_config)
            _col = self.client_gbq.get_schema_policy_tag(
                col.name,
                col.field_type,
                col.mode,
                policy_tag_id=policy_tag_id_full,
                desc=col.description,
            )
            return _col
        elif isinstance(tag_config, dict):
            fields = self.update_tag_recursive(col, tag_config, taxonomy_data)
            _col = SchemaField(
                name=col.name,
                field_type=col.field_type,
                mode=col.mode,
                fields=fields,
                description=col.description,
            )
            return _col

    def update_tag_recursive(self, col, tag_config, taxonomy_data):
        print(f"Working on field: {col.name}")
        output = []
        for field in col.fields:
            if field.name in tag_config.keys():
                field_config = tag_config[field.name]
                output.append(self.update_tag(field, field_config, taxonomy_data))
            else:
                output.append(field)
        return output

    def finalize(self, col, res, tag_config):
        if isinstance(tag_config, str):
            return res
        elif isinstance(tag_config, dict):
            res = self.client_gbq.get_schema_policy_tag(
                col_name=col.name, col_type=col.field_type, col_mode=col.mode, fields=res
            )
            return res
        else:
            raise NotImplementedError(f"tag_config={tag_config} is not supported")

    def tag_field(self, field, tag_configs, taxonomy_data):
        field_tag = tag_configs[field.name]
        _field = self.update_tag(field, field_tag, taxonomy_data)
        return _field

    def tag_table_by_config(self, table_id: str, taxonomy_data: dict, tag_configs: dict):
        table = self.client_gbq.client.get_table(table_id)
        _new_schema = []
        for field in table.schema:
            if field.name in tag_configs.keys():
                _field = self.tag_field(field, tag_configs, taxonomy_data)
                _new_schema.append(_field)
            else:
                _new_schema.append(field)
        table.schema = _new_schema
        self.client_gbq.client.update_table(table, ["schema"])
        return True

    def apply_policy_tag_2(self, table_id: str, taxonomy_data: dict, tag_configs: dict):
        table = self.client_gbq.client.get_table(table_id)
        _new_schema = []
        for col in table.schema:
            if col.name in tag_configs.keys():
                tag_config = tag_configs[col.name]
                res = self.update_tag(col, tag_config, taxonomy_data)
                res = self.finalize(col, res, tag_config)
                _new_schema.append(res)
            else:
                _new_schema.append(col)
        table.schema = _new_schema
        self.client_gbq.client.update_table(table, ["schema"])
        return True

    def apply_policy_tag(
        self, dataset_name, table_name, taxonomy_data, policy_tag_id, column_to_tag
    ):
        table_id = self.client_gbq.get_full_qualified_table_name(
            self.project_id, dataset_name, table_name
        )
        table = self.client_gbq.client.get_table(table_id)
        schema = table.schema
        _schema = []
        for col in schema:
            if col.name == column_to_tag:
                res = self.client_gbq.get_schema_policy_tag(
                    column_to_tag, col.field_type, col.mode, policy_tag_id=policy_tag_id
                )
                _schema.append(res)
            else:
                _schema.append(col)
        table.schema = _schema
        self.client_gbq.client.update_table(table, ["schema"])
        return True


if __name__ == "__main__":
    pass
