# -*- coding: utf-8 -*-
# Copyright 2021 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for the gcp module - cloudresourcemanager.py"""
import typing
import unittest

import mock

from tests.providers.gcp import gcp_mocks


class GoogleCloudResourceManagerTest(unittest.TestCase):
  """Test Google Cloud Resource Manager class."""
  # pylint: disable=line-too-long

  @typing.no_type_check
  @mock.patch('libcloudforensics.providers.gcp.internal.common.ExecuteRequest')
  @mock.patch('libcloudforensics.providers.gcp.internal.cloudresourcemanager.GoogleCloudResourceManager.GrmApi')
  def testGetResource(self, mock_grm_api, mock_execute_request):
    """Validates the GetResource function"""
    mock_execute_request.return_value = [gcp_mocks.MOCK_CLOUD_RESOURCE_PROJECT]
    mock_resource_client = mock_grm_api.return_value.projects.return_value
    response = gcp_mocks.FAKE_CLOUD_RESOURCE_MANAGER.GetResource(
        'projects/000000000000')
    mock_execute_request.assert_called_with(mock_resource_client,
        'get', {'name': 'projects/000000000000'})
    self.assertEqual(response,
        {
          "createTime": "2020-01-01T00:00:00.000Z",
          "displayName": "fake-project",
          "etag": "Tm90IGFuIGV0YWd4eHh4eA==",
          "name": "projects/000000000000",
          "parent": "folders/111111111111",
          "projectId": "fake-project",
          "state": "ACTIVE",
          "updateTime": "2020-01-01T00:00:00.000Z"
        })

  @typing.no_type_check
  @mock.patch('libcloudforensics.providers.gcp.internal.common.ExecuteRequest')
  @mock.patch('libcloudforensics.providers.gcp.internal.cloudresourcemanager.GoogleCloudResourceManager.GrmApi')
  def testGetResourceInvalidName(self, _, __):
    """Validates the GetResource function raises an exception for an invalid
    resource name."""
    with self.assertRaises(TypeError):
      gcp_mocks.FAKE_CLOUD_RESOURCE_MANAGER.GetResource(
          'badtype/000000000000')

  @typing.no_type_check
  @mock.patch('libcloudforensics.providers.gcp.internal.common.ExecuteRequest')
  @mock.patch('libcloudforensics.providers.gcp.internal.cloudresourcemanager.GoogleCloudResourceManager.GrmApi')
  def testGetProjectAncestry(self, _, mock_execute_request):
    """Validates the GetProjectAncestry function"""
    mock_execute_request.side_effect = [
        [gcp_mocks.MOCK_CLOUD_RESOURCE_PROJECT],
        [gcp_mocks.MOCK_CLOUD_RESOURCE_FOLDER],
        [gcp_mocks.MOCK_CLOUD_RESOURCE_ORGANIZATION]
    ]
    response = gcp_mocks.FAKE_CLOUD_RESOURCE_MANAGER.ProjectAncestry()
    self.assertListEqual(response,
        [
          {
            'createTime': '2020-01-01T00:00:00.000Z',
            'displayName': 'fake-project',
            'etag': 'Tm90IGFuIGV0YWd4eHh4eA==',
            'name': 'projects/000000000000',
            'parent': 'folders/111111111111',
            'projectId': 'fake-project',
            'state': 'ACTIVE', 'updateTime': '2020-01-01T00:00:00.000Z'
          },
          {
            'createTime': '2020-01-01T00:00:00.000Z',
            'displayName': 'fake-folder',
            'etag': 'Tm90IGFuIGV0YWd4eHh4eA==',
            'name': 'folders/111111111111',
            'parent': 'organizations/222222222222',
            'state': 'ACTIVE',
            'updateTime': '2020-01-01T00:00:00.000Z'
          },
          {
            'createTime': '2020-01-01T00:00:00.000Z',
            'directoryCustomerId': 'bm9jdXN0',
            'displayName': 'fake-organization.com',
            'etag': 'Tm90IGFuIGV0YWd4eHh4eA==',
            'name': 'organizations/222222222222',
            'state': 'ACTIVE',
            'updateTime': '2020-01-01T00:00:00.000Z'
          }
        ])

  @typing.no_type_check
  @mock.patch('libcloudforensics.providers.gcp.internal.common.ExecuteRequest')
  @mock.patch('libcloudforensics.providers.gcp.internal.cloudresourcemanager.GoogleCloudResourceManager.GrmApi')
  def testGetIamPolicy(self, mock_grm_api, mock_execute_request):
    """Validates the GetIamPolicy function"""
    mock_execute_request.return_value = [gcp_mocks.MOCK_IAM_POLICY]
    mock_resource_client = mock_grm_api.return_value.projects.return_value
    response = gcp_mocks.FAKE_CLOUD_RESOURCE_MANAGER.GetIamPolicy(
        'projects/000000000000')
    mock_execute_request.assert_called_with(mock_resource_client,
        'getIamPolicy', {'resource': 'projects/000000000000'})
    self.assertEqual(response, {
        "version": 1,
        "etag": "bm90X2V0YWc=",
        "bindings": [
          {
            "role": "roles/cloudbuild.builds.builder",
            "members": [
              "serviceAccount:012345678901@cloudbuild.gserviceaccount.com"
            ]
          },
          {
            "role": "roles/owner",
            "members": [
              "serviceAccount:fake_sa@fake-project.iam.gserviceaccount.com",
              "user:fakeaccount@fakedomain.com"
            ]
          }
        ]
      })

  @typing.no_type_check
  @mock.patch('libcloudforensics.providers.gcp.internal.cloudresourcemanager.GoogleCloudResourceManager.GrmApi')
  def testGetOrgPolicy(self, mock_grm_api):
    """Validates the GetOrgPolicy function"""
    api_get_org_policy = mock_grm_api.return_value.projects.return_value.getOrgPolicy
    api_get_org_policy.return_value.execute.return_value = gcp_mocks.MOCK_ORG_POLICY
    response = gcp_mocks.FAKE_CLOUD_RESOURCE_MANAGER.GetOrgPolicy(
        'projects/000000000000', 'fake-policy')
    api_get_org_policy.assert_called_with(
        resource='projects/000000000000',
        body={'constraint': 'constraints/fake-policy'})
    self.assertEqual(response, {
    'constraint': 'constraints/testpolicy',
    'etag': 'abcdefghijk='
    })


  @typing.no_type_check
  @mock.patch('libcloudforensics.providers.gcp.internal.cloudresourcemanager.GoogleCloudResourceManager.GrmApi')
  def testListOrgPolicy(self, mock_grm_api):
    """Validates the ListOrgPolicy function"""
    api_list_org_policy = mock_grm_api.return_value.projects.return_value.listOrgPolicies
    api_list_org_policy.return_value.execute.return_value = gcp_mocks.MOCK_ORG_POLICIES
    response = gcp_mocks.FAKE_CLOUD_RESOURCE_MANAGER.ListOrgPolicy(
        'projects/000000000000'
    )
    api_list_org_policy.assert_called_with(
        resource='projects/000000000000')
    self.assertEqual(len(response.get('policies', [])), 2)

  @typing.no_type_check
  @mock.patch('libcloudforensics.providers.gcp.internal.cloudresourcemanager.GoogleCloudResourceManager.GrmApi')
  def testSetOrgPolicy(self, mock_grm_api):
    """Validates the SetOrgPolicy function"""
    api_set_org_policy = mock_grm_api.return_value.projects.return_value.setOrgPolicy
    api_set_org_policy.return_value.execute.return_value = gcp_mocks.MOCK_ORG_POLICY
    gcp_mocks.FAKE_CLOUD_RESOURCE_MANAGER.SetOrgPolicy(
        'projects/000000000000',
        {
            'constraint': 'constraints/compute.storageResourceUseRestrictions',
            'listPolicy': {
                'inheritFromParent': False, 'allValues': 'ALLOW'
            }
        },
        'abc123')
    api_set_org_policy.assert_called_with(
        resource='projects/000000000000',
        body={
          'policy': {
            'constraint': 'constraints/compute.storageResourceUseRestrictions',
            'listPolicy': {
                'inheritFromParent': False, 'allValues': 'ALLOW'
            },
            'etag': 'abc123'
          }
        })

  @typing.no_type_check
  @mock.patch('libcloudforensics.providers.gcp.internal.cloudresourcemanager.GoogleCloudResourceManager.GrmApi')
  def testDeleteOrgPolicy(self, mock_grm_api):
    """Validates the DeleteOrgPolicy function"""
    api_delete_org_policy = mock_grm_api.return_value.projects.return_value.clearOrgPolicy
    api_delete_org_policy.return_value.execute.return_value = True
    gcp_mocks.FAKE_CLOUD_RESOURCE_MANAGER.DeleteOrgPolicy(
        'projects/000000000000',
        'fake-policy',
        'abc123'
    )
    api_delete_org_policy.assert_called_with(
        resource='projects/000000000000',
        body={'constraint': 'constraints/fake-policy', 'etag': 'abc123'}
        )
