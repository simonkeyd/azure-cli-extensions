# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

import datetime
from typing import Dict, List, Optional, Union

from azure.core.exceptions import HttpResponseError
import msrest.serialization

from ._confidential_ledger_enums import *


class AadBasedSecurityPrincipal(msrest.serialization.Model):
    """AAD based security principal with associated Ledger RoleName.

    :param principal_id: UUID/GUID based Principal Id of the Security Principal.
    :type principal_id: str
    :param tenant_id: UUID/GUID based Tenant Id of the Security Principal.
    :type tenant_id: str
    :param ledger_role_name: LedgerRole associated with the Security Principal of Ledger. Possible
     values include: "Reader", "Contributor", "Administrator".
    :type ledger_role_name: str or ~confidential_ledger.models.LedgerRoleName
    """

    _attribute_map = {
        'principal_id': {'key': 'principalId', 'type': 'str'},
        'tenant_id': {'key': 'tenantId', 'type': 'str'},
        'ledger_role_name': {'key': 'ledgerRoleName', 'type': 'str'},
    }

    def __init__(
        self,
        *,
        principal_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        ledger_role_name: Optional[Union[str, "LedgerRoleName"]] = None,
        **kwargs
    ):
        super(AadBasedSecurityPrincipal, self).__init__(**kwargs)
        self.principal_id = principal_id
        self.tenant_id = tenant_id
        self.ledger_role_name = ledger_role_name


class CertBasedSecurityPrincipal(msrest.serialization.Model):
    """Cert based security principal with Ledger RoleName.

    :param cert: Public key of the user cert (.pem or .cer).
    :type cert: str
    :param ledger_role_name: LedgerRole associated with the Security Principal of Ledger. Possible
     values include: "Reader", "Contributor", "Administrator".
    :type ledger_role_name: str or ~confidential_ledger.models.LedgerRoleName
    """

    _attribute_map = {
        'cert': {'key': 'cert', 'type': 'str'},
        'ledger_role_name': {'key': 'ledgerRoleName', 'type': 'str'},
    }

    def __init__(
        self,
        *,
        cert: Optional[str] = None,
        ledger_role_name: Optional[Union[str, "LedgerRoleName"]] = None,
        **kwargs
    ):
        super(CertBasedSecurityPrincipal, self).__init__(**kwargs)
        self.cert = cert
        self.ledger_role_name = ledger_role_name


class CheckNameAvailabilityRequest(msrest.serialization.Model):
    """The check availability request body.

    :param name: The name of the resource for which availability needs to be checked.
    :type name: str
    :param type: The resource type.
    :type type: str
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
    }

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        type: Optional[str] = None,
        **kwargs
    ):
        super(CheckNameAvailabilityRequest, self).__init__(**kwargs)
        self.name = name
        self.type = type


class CheckNameAvailabilityResponse(msrest.serialization.Model):
    """The check availability result.

    :param name_available: Indicates if the resource name is available.
    :type name_available: bool
    :param reason: The reason why the given name is not available. Possible values include:
     "Invalid", "AlreadyExists".
    :type reason: str or ~confidential_ledger.models.CheckNameAvailabilityReason
    :param message: Detailed reason why the given name is available.
    :type message: str
    """

    _attribute_map = {
        'name_available': {'key': 'nameAvailable', 'type': 'bool'},
        'reason': {'key': 'reason', 'type': 'str'},
        'message': {'key': 'message', 'type': 'str'},
    }

    def __init__(
        self,
        *,
        name_available: Optional[bool] = None,
        reason: Optional[Union[str, "CheckNameAvailabilityReason"]] = None,
        message: Optional[str] = None,
        **kwargs
    ):
        super(CheckNameAvailabilityResponse, self).__init__(**kwargs)
        self.name_available = name_available
        self.reason = reason
        self.message = message


class Tags(msrest.serialization.Model):
    """Tags for Confidential Ledger Resource.

    :param tags: A set of tags. Additional tags for Confidential Ledger.
    :type tags: dict[str, str]
    """

    _attribute_map = {
        'tags': {'key': 'tags', 'type': '{str}'},
    }

    def __init__(
        self,
        *,
        tags: Optional[Dict[str, str]] = None,
        **kwargs
    ):
        super(Tags, self).__init__(**kwargs)
        self.tags = tags


class ResourceLocation(msrest.serialization.Model):
    """Location of the ARM Resource.

    :param location: The Azure location where the Confidential Ledger is running.
    :type location: str
    """

    _attribute_map = {
        'location': {'key': 'location', 'type': 'str'},
    }

    def __init__(
        self,
        *,
        location: Optional[str] = None,
        **kwargs
    ):
        super(ResourceLocation, self).__init__(**kwargs)
        self.location = location


class Resource(msrest.serialization.Model):
    """An Azure resource.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar name: Name of the Resource.
    :vartype name: str
    :ivar id: Fully qualified resource Id for the resource.
    :vartype id: str
    :ivar type: The type of the resource.
    :vartype type: str
    :ivar system_data: Metadata pertaining to creation and last modification of the resource.
    :vartype system_data: ~confidential_ledger.models.SystemData
    """

    _validation = {
        'name': {'readonly': True},
        'id': {'readonly': True},
        'type': {'readonly': True},
        'system_data': {'readonly': True},
    }

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'id': {'key': 'id', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'system_data': {'key': 'systemData', 'type': 'SystemData'},
    }

    def __init__(
        self,
        **kwargs
    ):
        super(Resource, self).__init__(**kwargs)
        self.name = None
        self.id = None
        self.type = None
        self.system_data = None


class ConfidentialLedger(Resource, ResourceLocation, Tags):
    """Confidential Ledger. Contains the properties of Confidential Ledger Resource.

    Variables are only populated by the server, and will be ignored when sending a request.

    :param tags: A set of tags. Additional tags for Confidential Ledger.
    :type tags: dict[str, str]
    :param location: The Azure location where the Confidential Ledger is running.
    :type location: str
    :ivar name: Name of the Resource.
    :vartype name: str
    :ivar id: Fully qualified resource Id for the resource.
    :vartype id: str
    :ivar type: The type of the resource.
    :vartype type: str
    :ivar system_data: Metadata pertaining to creation and last modification of the resource.
    :vartype system_data: ~confidential_ledger.models.SystemData
    :param properties: Properties of Confidential Ledger Resource.
    :type properties: ~confidential_ledger.models.LedgerProperties
    """

    _validation = {
        'name': {'readonly': True},
        'id': {'readonly': True},
        'type': {'readonly': True},
        'system_data': {'readonly': True},
    }

    _attribute_map = {
        'tags': {'key': 'tags', 'type': '{str}'},
        'location': {'key': 'location', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'id': {'key': 'id', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'system_data': {'key': 'systemData', 'type': 'SystemData'},
        'properties': {'key': 'properties', 'type': 'LedgerProperties'},
    }

    def __init__(
        self,
        *,
        tags: Optional[Dict[str, str]] = None,
        location: Optional[str] = None,
        properties: Optional["LedgerProperties"] = None,
        **kwargs
    ):
        super(ConfidentialLedger, self).__init__(location=location, tags=tags, **kwargs)
        self.tags = tags
        self.location = location
        self.properties = properties
        self.tags = tags
        self.name = None
        self.id = None
        self.type = None
        self.system_data = None
        self.properties = properties
        self.location = location
        self.name = None
        self.id = None
        self.type = None
        self.system_data = None
        self.properties = properties


class ConfidentialLedgerList(msrest.serialization.Model):
    """Object that includes an array of Confidential Ledgers and a possible link for next set.

    :param value: List of Confidential Ledgers.
    :type value: list[~confidential_ledger.models.ConfidentialLedger]
    :param next_link: The URL the client should use to fetch the next page (per server side
     paging).
    :type next_link: str
    """

    _attribute_map = {
        'value': {'key': 'value', 'type': '[ConfidentialLedger]'},
        'next_link': {'key': 'nextLink', 'type': 'str'},
    }

    def __init__(
        self,
        *,
        value: Optional[List["ConfidentialLedger"]] = None,
        next_link: Optional[str] = None,
        **kwargs
    ):
        super(ConfidentialLedgerList, self).__init__(**kwargs)
        self.value = value
        self.next_link = next_link


class ErrorAdditionalInfo(msrest.serialization.Model):
    """The resource management error additional info.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar type: The additional info type.
    :vartype type: str
    :ivar info: The additional info.
    :vartype info: object
    """

    _validation = {
        'type': {'readonly': True},
        'info': {'readonly': True},
    }

    _attribute_map = {
        'type': {'key': 'type', 'type': 'str'},
        'info': {'key': 'info', 'type': 'object'},
    }

    def __init__(
        self,
        **kwargs
    ):
        super(ErrorAdditionalInfo, self).__init__(**kwargs)
        self.type = None
        self.info = None


class ErrorDetail(msrest.serialization.Model):
    """The error detail.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar code: The error code.
    :vartype code: str
    :ivar message: The error message.
    :vartype message: str
    :ivar target: The error target.
    :vartype target: str
    :ivar details: The error details.
    :vartype details: list[~confidential_ledger.models.ErrorDetail]
    :ivar additional_info: The error additional info.
    :vartype additional_info: list[~confidential_ledger.models.ErrorAdditionalInfo]
    """

    _validation = {
        'code': {'readonly': True},
        'message': {'readonly': True},
        'target': {'readonly': True},
        'details': {'readonly': True},
        'additional_info': {'readonly': True},
    }

    _attribute_map = {
        'code': {'key': 'code', 'type': 'str'},
        'message': {'key': 'message', 'type': 'str'},
        'target': {'key': 'target', 'type': 'str'},
        'details': {'key': 'details', 'type': '[ErrorDetail]'},
        'additional_info': {'key': 'additionalInfo', 'type': '[ErrorAdditionalInfo]'},
    }

    def __init__(
        self,
        **kwargs
    ):
        super(ErrorDetail, self).__init__(**kwargs)
        self.code = None
        self.message = None
        self.target = None
        self.details = None
        self.additional_info = None


class ErrorResponse(msrest.serialization.Model):
    """Common error response for all Azure Resource Manager APIs to return error details for failed operations. (This also follows the OData error response format.).

    :param error: The error object.
    :type error: ~confidential_ledger.models.ErrorDetail
    """

    _attribute_map = {
        'error': {'key': 'error', 'type': 'ErrorDetail'},
    }

    def __init__(
        self,
        *,
        error: Optional["ErrorDetail"] = None,
        **kwargs
    ):
        super(ErrorResponse, self).__init__(**kwargs)
        self.error = error


class LedgerProperties(msrest.serialization.Model):
    """Additional Confidential Ledger properties.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar ledger_name: Unique name for the Confidential Ledger.
    :vartype ledger_name: str
    :ivar ledger_uri: Endpoint for calling Ledger Service.
    :vartype ledger_uri: str
    :ivar identity_service_uri: Endpoint for accessing network identity.
    :vartype identity_service_uri: str
    :ivar ledger_internal_namespace: Internal namespace for the Ledger.
    :vartype ledger_internal_namespace: str
    :param ledger_type: Type of Confidential Ledger. Possible values include: "Unknown", "Public",
     "Private".
    :type ledger_type: str or ~confidential_ledger.models.LedgerType
    :ivar provisioning_state: Provisioning state of Ledger Resource. Possible values include:
     "Unknown", "Succeeded", "Failed", "Canceled", "Creating", "Deleting", "Updating".
    :vartype provisioning_state: str or ~confidential_ledger.models.ProvisioningState
    :param aad_based_security_principals: Array of all AAD based Security Principals.
    :type aad_based_security_principals:
     list[~confidential_ledger.models.AadBasedSecurityPrincipal]
    :param cert_based_security_principals: Array of all cert based Security Principals.
    :type cert_based_security_principals:
     list[~confidential_ledger.models.CertBasedSecurityPrincipal]
    """

    _validation = {
        'ledger_name': {'readonly': True},
        'ledger_uri': {'readonly': True},
        'identity_service_uri': {'readonly': True},
        'ledger_internal_namespace': {'readonly': True},
        'provisioning_state': {'readonly': True},
    }

    _attribute_map = {
        'ledger_name': {'key': 'ledgerName', 'type': 'str'},
        'ledger_uri': {'key': 'ledgerUri', 'type': 'str'},
        'identity_service_uri': {'key': 'identityServiceUri', 'type': 'str'},
        'ledger_internal_namespace': {'key': 'ledgerInternalNamespace', 'type': 'str'},
        'ledger_type': {'key': 'ledgerType', 'type': 'str'},
        'provisioning_state': {'key': 'provisioningState', 'type': 'str'},
        'aad_based_security_principals': {'key': 'aadBasedSecurityPrincipals', 'type': '[AadBasedSecurityPrincipal]'},
        'cert_based_security_principals': {'key': 'certBasedSecurityPrincipals', 'type': '[CertBasedSecurityPrincipal]'},
    }

    def __init__(
        self,
        *,
        ledger_type: Optional[Union[str, "LedgerType"]] = None,
        aad_based_security_principals: Optional[List["AadBasedSecurityPrincipal"]] = None,
        cert_based_security_principals: Optional[List["CertBasedSecurityPrincipal"]] = None,
        **kwargs
    ):
        super(LedgerProperties, self).__init__(**kwargs)
        self.ledger_name = None
        self.ledger_uri = None
        self.identity_service_uri = None
        self.ledger_internal_namespace = None
        self.ledger_type = ledger_type
        self.provisioning_state = None
        self.aad_based_security_principals = aad_based_security_principals
        self.cert_based_security_principals = cert_based_security_principals


class ResourceProviderOperationDefinition(msrest.serialization.Model):
    """Describes the Resource Provider Operation.

    :param name: Resource provider operation name.
    :type name: str
    :param is_data_action: Indicates whether the operation is data action or not.
    :type is_data_action: bool
    :param display: Details about the operations.
    :type display: ~confidential_ledger.models.ResourceProviderOperationDisplay
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'is_data_action': {'key': 'isDataAction', 'type': 'bool'},
        'display': {'key': 'display', 'type': 'ResourceProviderOperationDisplay'},
    }

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        is_data_action: Optional[bool] = None,
        display: Optional["ResourceProviderOperationDisplay"] = None,
        **kwargs
    ):
        super(ResourceProviderOperationDefinition, self).__init__(**kwargs)
        self.name = name
        self.is_data_action = is_data_action
        self.display = display


class ResourceProviderOperationDisplay(msrest.serialization.Model):
    """Describes the properties of the Operation.

    :param provider: Name of the resource provider.
    :type provider: str
    :param resource: Name of the resource type.
    :type resource: str
    :param operation: Name of the resource provider operation.
    :type operation: str
    :param description: Description of the resource provider operation.
    :type description: str
    """

    _attribute_map = {
        'provider': {'key': 'provider', 'type': 'str'},
        'resource': {'key': 'resource', 'type': 'str'},
        'operation': {'key': 'operation', 'type': 'str'},
        'description': {'key': 'description', 'type': 'str'},
    }

    def __init__(
        self,
        *,
        provider: Optional[str] = None,
        resource: Optional[str] = None,
        operation: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ):
        super(ResourceProviderOperationDisplay, self).__init__(**kwargs)
        self.provider = provider
        self.resource = resource
        self.operation = operation
        self.description = description


class ResourceProviderOperationList(msrest.serialization.Model):
    """List containing this Resource Provider's available operations.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar value: Resource provider operations list.
    :vartype value: list[~confidential_ledger.models.ResourceProviderOperationDefinition]
    :ivar next_link: The URI that can be used to request the next page for list of Azure
     operations.
    :vartype next_link: str
    """

    _validation = {
        'value': {'readonly': True},
        'next_link': {'readonly': True},
    }

    _attribute_map = {
        'value': {'key': 'value', 'type': '[ResourceProviderOperationDefinition]'},
        'next_link': {'key': 'nextLink', 'type': 'str'},
    }

    def __init__(
        self,
        **kwargs
    ):
        super(ResourceProviderOperationList, self).__init__(**kwargs)
        self.value = None
        self.next_link = None


class SystemData(msrest.serialization.Model):
    """Metadata pertaining to creation and last modification of the resource.

    :param created_by: The identity that created the resource.
    :type created_by: str
    :param created_by_type: The type of identity that created the resource. Possible values
     include: "User", "Application", "ManagedIdentity", "Key".
    :type created_by_type: str or ~confidential_ledger.models.CreatedByType
    :param created_at: The timestamp of resource creation (UTC).
    :type created_at: ~datetime.datetime
    :param last_modified_by: The identity that last modified the resource.
    :type last_modified_by: str
    :param last_modified_by_type: The type of identity that last modified the resource. Possible
     values include: "User", "Application", "ManagedIdentity", "Key".
    :type last_modified_by_type: str or ~confidential_ledger.models.CreatedByType
    :param last_modified_at: The timestamp of resource last modification (UTC).
    :type last_modified_at: ~datetime.datetime
    """

    _attribute_map = {
        'created_by': {'key': 'createdBy', 'type': 'str'},
        'created_by_type': {'key': 'createdByType', 'type': 'str'},
        'created_at': {'key': 'createdAt', 'type': 'iso-8601'},
        'last_modified_by': {'key': 'lastModifiedBy', 'type': 'str'},
        'last_modified_by_type': {'key': 'lastModifiedByType', 'type': 'str'},
        'last_modified_at': {'key': 'lastModifiedAt', 'type': 'iso-8601'},
    }

    def __init__(
        self,
        *,
        created_by: Optional[str] = None,
        created_by_type: Optional[Union[str, "CreatedByType"]] = None,
        created_at: Optional[datetime.datetime] = None,
        last_modified_by: Optional[str] = None,
        last_modified_by_type: Optional[Union[str, "CreatedByType"]] = None,
        last_modified_at: Optional[datetime.datetime] = None,
        **kwargs
    ):
        super(SystemData, self).__init__(**kwargs)
        self.created_by = created_by
        self.created_by_type = created_by_type
        self.created_at = created_at
        self.last_modified_by = last_modified_by
        self.last_modified_by_type = last_modified_by_type
        self.last_modified_at = last_modified_at
