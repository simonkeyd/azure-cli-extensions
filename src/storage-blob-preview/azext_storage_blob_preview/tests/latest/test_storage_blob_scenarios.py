# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import re
import unittest
from datetime import datetime, timedelta
from azure.cli.testsdk import (ScenarioTest, ResourceGroupPreparer, StorageAccountPreparer,
                               JMESPathCheck, JMESPathCheckExists, NoneCheck, api_version_constraint)
from knack.util import CLIError
from azure.cli.core.profiles import ResourceType
from azure.cli.testsdk.scenario_tests import AllowLargeResponse

from ..storage_test_util import StorageScenarioMixin


@api_version_constraint(ResourceType.MGMT_STORAGE, min_api='2016-12-01')
class StorageBlobUploadTests(StorageScenarioMixin, ScenarioTest):
    @ResourceGroupPreparer()
    @StorageAccountPreparer(parameter_name='source_account')
    @StorageAccountPreparer(parameter_name='target_account')
    def test_storage_blob_incremental_copy(self, resource_group, source_account_info, target_account_info):
        source_file = self.create_temp_file(16)
        source_container = self.create_container(source_account_info)
        self.storage_cmd('storage blob upload -c {} -n src -f "{}" -t page', source_account_info,
                         source_container, source_file)

        snapshot = self.storage_cmd('storage blob snapshot -c {} -n src', source_account_info,
                                    source_container).get_output_in_json()['snapshot']

        target_container = self.create_container(target_account_info)
        self.storage_cmd('storage blob incremental-copy start --source-container {} --source-blob '
                         'src --source-account-name {} --source-account-key {} --source-snapshot '
                         '{} --destination-container {} --destination-blob backup '
                         '--destination-if-modified-since "2020-06-29T06:32Z" ',
                         target_account_info, source_container, source_account_info[0],
                         source_account_info[1], snapshot, target_container)

    @AllowLargeResponse()
    def test_storage_blob_no_credentials_scenario(self):
        source_file = self.create_temp_file(1)
        self.cmd('storage blob upload -c foo -n bar -f "' + source_file + '"', expect_failure=CLIError)

    @ResourceGroupPreparer()
    @StorageAccountPreparer()
    def test_storage_blob_upload_small_file(self, resource_group, storage_account_info):
        for blob_type in ['block', 'page']:
            self.verify_blob_upload_and_download(resource_group, storage_account_info, 1, blob_type, 0)

    @ResourceGroupPreparer()
    @StorageAccountPreparer()
    def test_storage_blob_upload_midsize_file(self, resource_group, storage_account_info):
        for blob_type in ['block', 'page']:
            self.verify_blob_upload_and_download(resource_group, storage_account_info, 4096, 'block', 0)

    def verify_blob_upload_and_download(self, group, account_info, file_size_kb, blob_type,
                                        block_count=0, skip_download=False):
        local_dir = self.create_temp_dir()
        local_file = self.create_temp_file(file_size_kb)
        blob_name = self.create_random_name(prefix='blob', length=24)

        container = self.create_container(account_info)
        self.storage_cmd('storage blob exists -n {} -c {}', account_info, blob_name, container) \
            .assert_with_checks(JMESPathCheck('exists', False))

        self.storage_cmd('storage blob upload -c {} -f "{}" -n {} --type {} ', account_info,
                         container, local_file, blob_name, blob_type)
        self.storage_cmd('storage blob exists -n {} -c {}', account_info, blob_name, container) \
            .assert_with_checks(JMESPathCheck('exists', True))
        self.storage_cmd('storage blob list -c {} -otable --num-results 1', account_info, container)

        show_result = self.storage_cmd('storage blob show -n {} -c {}', account_info, blob_name,
                                       container).get_output_in_json()
        self.assertEqual(show_result.get('name'), blob_name)
        if blob_type == 'block':
            self.assertIsNotNone(show_result['properties']['contentSettings']['contentMd5'])
            md5 = show_result['properties']['contentSettings']['contentMd5']
            self.storage_cmd('storage blob upload -c {} -f "{}" -n {} --type {} --content-md5 {} --overwrite', account_info,
                             container, local_file, blob_name, blob_type, md5)
        if blob_type == 'page':
            self.assertEqual(type(show_result.get('properties').get('pageRanges')), list)
        else:
            self.assertEqual(show_result.get('properties').get('pageRanges'), None)

        expiry = (datetime.utcnow() + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%MZ')
        sas = self.storage_cmd('storage blob generate-sas -n {} -c {} --expiry {} --permissions '
                               'r --https-only', account_info, blob_name, container, expiry).output
        self.assertTrue(sas)
        self.assertIn('&sig=', sas)

        self.storage_cmd('storage blob update -n {} -c {} --content-type application/test-content',
                         account_info, blob_name, container)

        self.storage_cmd('storage blob show -n {} -c {}', account_info, blob_name, container) \
            .assert_with_checks(
            [JMESPathCheck('properties.contentSettings.contentType', 'application/test-content'),
             JMESPathCheck('properties.contentLength', file_size_kb * 1024)])

        # check that blob properties can be set back to null
        self.storage_cmd('storage blob update -n {} -c {} --content-type ""',
                         account_info, blob_name, container)

        self.storage_cmd('storage blob show -n {} -c {}', account_info, blob_name, container) \
            .assert_with_checks(JMESPathCheck('properties.contentSettings.contentType', None))

        self.storage_cmd('storage blob service-properties show', account_info) \
            .assert_with_checks(JMESPathCheck('hourMetrics.enabled', True))

        if not skip_download:
            downloaded = os.path.join(local_dir, 'test.file')

            self.storage_cmd('storage blob download -n {} -c {} --file "{}"',
                             account_info, blob_name, container, downloaded)
            self.assertTrue(os.path.isfile(downloaded), 'The file is not downloaded.')
            self.assertEqual(file_size_kb * 1024, os.stat(downloaded).st_size,
                             'The download file size is not right.')
            self.storage_cmd('storage blob download -n {} -c {} --file "{}" --start-range 10 --end-range 499',
                             account_info, blob_name, container, downloaded)
            self.assertEqual(490, os.stat(downloaded).st_size,
                             'The download file size is not right.')

        # Verify the requests in cassette to ensure the count of the block requests is expected
        # This portion of validation doesn't verify anything during playback because the recording
        # is fixed.

        def is_block_put_req(request):
            if request.method != 'PUT':
                return False

            if not re.search('/cont[0-9]+/blob[0-9]+', request.path):
                return False

            comp_block = False
            has_blockid = False
            for key, value in request.query:
                if key == 'comp' and value == 'block':
                    comp_block = True
                elif key == 'blockid':
                    has_blockid = True

            return comp_block and has_blockid

        requests = self.cassette.requests
        put_blocks = [request for request in requests if is_block_put_req(request)]
        self.assertEqual(block_count, len(put_blocks),
                         'The expected number of block put requests is {} but the actual '
                         'number is {}.'.format(block_count, len(put_blocks)))

    @ResourceGroupPreparer()
    @StorageAccountPreparer(kind='StorageV2')
    def test_storage_blob_soft_delete(self, resource_group, storage_account_info):
        account_info = storage_account_info
        container = self.create_container(account_info)
        import time

        # create a blob
        local_file = self.create_temp_file(1)
        blob_name = self.create_random_name(prefix='blob', length=24)

        self.storage_cmd('storage blob upload -c {} -f "{}" -n {} --type block', account_info,
                         container, local_file, blob_name)
        self.assertEqual(len(self.storage_cmd('storage blob list -c {}',
                                              account_info, container).get_output_in_json()), 1)

        # set delete-policy to enable soft-delete
        self.storage_cmd('storage blob service-properties delete-policy update --enable true --days-retained 2',
                         account_info)
        self.storage_cmd('storage blob service-properties delete-policy show',
                         account_info).assert_with_checks(JMESPathCheck('enabled', True),
                                                          JMESPathCheck('days', 2))
        time.sleep(10)
        # soft-delete and check
        self.storage_cmd('storage blob delete -c {} -n {}', account_info, container, blob_name)
        self.assertEqual(len(self.storage_cmd('storage blob list -c {}',
                                              account_info, container).get_output_in_json()), 0)

        # undelete and check
        time.sleep(60)
        self.storage_cmd('storage blob undelete -c {} -n {}', account_info, container, blob_name)
        self.assertEqual(len(self.storage_cmd('storage blob list -c {}',
                                              account_info, container).get_output_in_json()), 1)

    @ResourceGroupPreparer()
    @StorageAccountPreparer(kind='StorageV2')
    def test_storage_blob_update_service_properties(self, resource_group, storage_account_info):
        account_info = storage_account_info

        self.storage_cmd('storage blob service-properties show', account_info) \
            .assert_with_checks(JMESPathCheck('staticWebsite.enabled', False),
                                JMESPathCheck('hourMetrics.enabled', True),
                                JMESPathCheck('minuteMetrics.enabled', False),
                                JMESPathCheck('minuteMetrics.includeApis', None),
                                JMESPathCheck('logging.delete', False))

        self.storage_cmd('storage blob service-properties update --static-website --index-document index.html '
                         '--404-document error.html', account_info) \
            .assert_with_checks(JMESPathCheck('staticWebsite.enabled', True),
                                JMESPathCheck('staticWebsite.errorDocument_404Path', 'error.html'),
                                JMESPathCheck('staticWebsite.indexDocument', 'index.html'))

        self.storage_cmd('storage blob service-properties update --delete-retention --delete-retention-period 1',
                         account_info) \
            .assert_with_checks(JMESPathCheck('staticWebsite.enabled', True),
                                JMESPathCheck('staticWebsite.errorDocument_404Path', 'error.html'),
                                JMESPathCheck('staticWebsite.indexDocument', 'index.html'),
                                JMESPathCheck('deleteRetentionPolicy.enabled', True),
                                JMESPathCheck('deleteRetentionPolicy.days', 1))

        self.storage_cmd('storage blob service-properties show', account_info) \
            .assert_with_checks(JMESPathCheck('staticWebsite.enabled', True),
                                JMESPathCheck('staticWebsite.errorDocument_404Path', 'error.html'),
                                JMESPathCheck('staticWebsite.indexDocument', 'index.html'),
                                JMESPathCheck('deleteRetentionPolicy.enabled', True),
                                JMESPathCheck('deleteRetentionPolicy.days', 1))


if __name__ == '__main__':
    unittest.main()
