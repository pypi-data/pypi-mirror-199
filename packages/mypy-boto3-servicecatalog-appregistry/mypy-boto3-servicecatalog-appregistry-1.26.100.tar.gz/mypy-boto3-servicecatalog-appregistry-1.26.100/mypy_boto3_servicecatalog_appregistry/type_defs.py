"""
Type annotations for servicecatalog-appregistry service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_servicecatalog_appregistry/type_defs/)

Usage::

    ```python
    from mypy_boto3_servicecatalog_appregistry.type_defs import TagQueryConfigurationTypeDef

    data: TagQueryConfigurationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import ResourceGroupStateType, ResourceTypeType, SyncActionType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "TagQueryConfigurationTypeDef",
    "ApplicationSummaryTypeDef",
    "ApplicationTypeDef",
    "AssociateAttributeGroupRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "AssociateResourceRequestRequestTypeDef",
    "AttributeGroupDetailsTypeDef",
    "AttributeGroupSummaryTypeDef",
    "AttributeGroupTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "CreateAttributeGroupRequestRequestTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteAttributeGroupRequestRequestTypeDef",
    "DisassociateAttributeGroupRequestRequestTypeDef",
    "DisassociateResourceRequestRequestTypeDef",
    "GetApplicationRequestRequestTypeDef",
    "GetAssociatedResourceRequestRequestTypeDef",
    "GetAttributeGroupRequestRequestTypeDef",
    "ResourceGroupTypeDef",
    "PaginatorConfigTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListAssociatedAttributeGroupsRequestRequestTypeDef",
    "ListAssociatedResourcesRequestRequestTypeDef",
    "ListAttributeGroupsForApplicationRequestRequestTypeDef",
    "ListAttributeGroupsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ResourceDetailsTypeDef",
    "SyncResourceRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "UpdateAttributeGroupRequestRequestTypeDef",
    "AppRegistryConfigurationTypeDef",
    "AssociateAttributeGroupResponseTypeDef",
    "AssociateResourceResponseTypeDef",
    "CreateApplicationResponseTypeDef",
    "DeleteApplicationResponseTypeDef",
    "DisassociateAttributeGroupResponseTypeDef",
    "DisassociateResourceResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetAttributeGroupResponseTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListAssociatedAttributeGroupsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "SyncResourceResponseTypeDef",
    "UpdateApplicationResponseTypeDef",
    "ListAttributeGroupsForApplicationResponseTypeDef",
    "DeleteAttributeGroupResponseTypeDef",
    "ListAttributeGroupsResponseTypeDef",
    "CreateAttributeGroupResponseTypeDef",
    "UpdateAttributeGroupResponseTypeDef",
    "IntegrationsTypeDef",
    "ResourceIntegrationsTypeDef",
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    "ListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef",
    "ListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef",
    "ListAttributeGroupsForApplicationRequestListAttributeGroupsForApplicationPaginateTypeDef",
    "ListAttributeGroupsRequestListAttributeGroupsPaginateTypeDef",
    "ResourceInfoTypeDef",
    "GetConfigurationResponseTypeDef",
    "PutConfigurationRequestRequestTypeDef",
    "GetApplicationResponseTypeDef",
    "ResourceTypeDef",
    "ListAssociatedResourcesResponseTypeDef",
    "GetAssociatedResourceResponseTypeDef",
)

TagQueryConfigurationTypeDef = TypedDict(
    "TagQueryConfigurationTypeDef",
    {
        "tagKey": str,
    },
    total=False,
)

ApplicationSummaryTypeDef = TypedDict(
    "ApplicationSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
    },
    total=False,
)

ApplicationTypeDef = TypedDict(
    "ApplicationTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "tags": Dict[str, str],
    },
    total=False,
)

AssociateAttributeGroupRequestRequestTypeDef = TypedDict(
    "AssociateAttributeGroupRequestRequestTypeDef",
    {
        "application": str,
        "attributeGroup": str,
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

AssociateResourceRequestRequestTypeDef = TypedDict(
    "AssociateResourceRequestRequestTypeDef",
    {
        "application": str,
        "resourceType": ResourceTypeType,
        "resource": str,
    },
)

AttributeGroupDetailsTypeDef = TypedDict(
    "AttributeGroupDetailsTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "createdBy": str,
    },
    total=False,
)

AttributeGroupSummaryTypeDef = TypedDict(
    "AttributeGroupSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "createdBy": str,
    },
    total=False,
)

AttributeGroupTypeDef = TypedDict(
    "AttributeGroupTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "tags": Dict[str, str],
    },
    total=False,
)

_RequiredCreateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateApplicationRequestRequestTypeDef",
    {
        "name": str,
        "clientToken": str,
    },
)
_OptionalCreateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateApplicationRequestRequestTypeDef",
    {
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateApplicationRequestRequestTypeDef(
    _RequiredCreateApplicationRequestRequestTypeDef, _OptionalCreateApplicationRequestRequestTypeDef
):
    pass


_RequiredCreateAttributeGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAttributeGroupRequestRequestTypeDef",
    {
        "name": str,
        "attributes": str,
        "clientToken": str,
    },
)
_OptionalCreateAttributeGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAttributeGroupRequestRequestTypeDef",
    {
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateAttributeGroupRequestRequestTypeDef(
    _RequiredCreateAttributeGroupRequestRequestTypeDef,
    _OptionalCreateAttributeGroupRequestRequestTypeDef,
):
    pass


DeleteApplicationRequestRequestTypeDef = TypedDict(
    "DeleteApplicationRequestRequestTypeDef",
    {
        "application": str,
    },
)

DeleteAttributeGroupRequestRequestTypeDef = TypedDict(
    "DeleteAttributeGroupRequestRequestTypeDef",
    {
        "attributeGroup": str,
    },
)

DisassociateAttributeGroupRequestRequestTypeDef = TypedDict(
    "DisassociateAttributeGroupRequestRequestTypeDef",
    {
        "application": str,
        "attributeGroup": str,
    },
)

DisassociateResourceRequestRequestTypeDef = TypedDict(
    "DisassociateResourceRequestRequestTypeDef",
    {
        "application": str,
        "resourceType": ResourceTypeType,
        "resource": str,
    },
)

GetApplicationRequestRequestTypeDef = TypedDict(
    "GetApplicationRequestRequestTypeDef",
    {
        "application": str,
    },
)

GetAssociatedResourceRequestRequestTypeDef = TypedDict(
    "GetAssociatedResourceRequestRequestTypeDef",
    {
        "application": str,
        "resourceType": ResourceTypeType,
        "resource": str,
    },
)

GetAttributeGroupRequestRequestTypeDef = TypedDict(
    "GetAttributeGroupRequestRequestTypeDef",
    {
        "attributeGroup": str,
    },
)

ResourceGroupTypeDef = TypedDict(
    "ResourceGroupTypeDef",
    {
        "state": ResourceGroupStateType,
        "arn": str,
        "errorMessage": str,
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

ListApplicationsRequestRequestTypeDef = TypedDict(
    "ListApplicationsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

_RequiredListAssociatedAttributeGroupsRequestRequestTypeDef = TypedDict(
    "_RequiredListAssociatedAttributeGroupsRequestRequestTypeDef",
    {
        "application": str,
    },
)
_OptionalListAssociatedAttributeGroupsRequestRequestTypeDef = TypedDict(
    "_OptionalListAssociatedAttributeGroupsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListAssociatedAttributeGroupsRequestRequestTypeDef(
    _RequiredListAssociatedAttributeGroupsRequestRequestTypeDef,
    _OptionalListAssociatedAttributeGroupsRequestRequestTypeDef,
):
    pass


_RequiredListAssociatedResourcesRequestRequestTypeDef = TypedDict(
    "_RequiredListAssociatedResourcesRequestRequestTypeDef",
    {
        "application": str,
    },
)
_OptionalListAssociatedResourcesRequestRequestTypeDef = TypedDict(
    "_OptionalListAssociatedResourcesRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListAssociatedResourcesRequestRequestTypeDef(
    _RequiredListAssociatedResourcesRequestRequestTypeDef,
    _OptionalListAssociatedResourcesRequestRequestTypeDef,
):
    pass


_RequiredListAttributeGroupsForApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredListAttributeGroupsForApplicationRequestRequestTypeDef",
    {
        "application": str,
    },
)
_OptionalListAttributeGroupsForApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalListAttributeGroupsForApplicationRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)


class ListAttributeGroupsForApplicationRequestRequestTypeDef(
    _RequiredListAttributeGroupsForApplicationRequestRequestTypeDef,
    _OptionalListAttributeGroupsForApplicationRequestRequestTypeDef,
):
    pass


ListAttributeGroupsRequestRequestTypeDef = TypedDict(
    "ListAttributeGroupsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ResourceDetailsTypeDef = TypedDict(
    "ResourceDetailsTypeDef",
    {
        "tagValue": str,
    },
    total=False,
)

SyncResourceRequestRequestTypeDef = TypedDict(
    "SyncResourceRequestRequestTypeDef",
    {
        "resourceType": ResourceTypeType,
        "resource": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateApplicationRequestRequestTypeDef",
    {
        "application": str,
    },
)
_OptionalUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateApplicationRequestRequestTypeDef",
    {
        "name": str,
        "description": str,
    },
    total=False,
)


class UpdateApplicationRequestRequestTypeDef(
    _RequiredUpdateApplicationRequestRequestTypeDef, _OptionalUpdateApplicationRequestRequestTypeDef
):
    pass


_RequiredUpdateAttributeGroupRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAttributeGroupRequestRequestTypeDef",
    {
        "attributeGroup": str,
    },
)
_OptionalUpdateAttributeGroupRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAttributeGroupRequestRequestTypeDef",
    {
        "name": str,
        "description": str,
        "attributes": str,
    },
    total=False,
)


class UpdateAttributeGroupRequestRequestTypeDef(
    _RequiredUpdateAttributeGroupRequestRequestTypeDef,
    _OptionalUpdateAttributeGroupRequestRequestTypeDef,
):
    pass


AppRegistryConfigurationTypeDef = TypedDict(
    "AppRegistryConfigurationTypeDef",
    {
        "tagQueryConfiguration": TagQueryConfigurationTypeDef,
    },
    total=False,
)

AssociateAttributeGroupResponseTypeDef = TypedDict(
    "AssociateAttributeGroupResponseTypeDef",
    {
        "applicationArn": str,
        "attributeGroupArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateResourceResponseTypeDef = TypedDict(
    "AssociateResourceResponseTypeDef",
    {
        "applicationArn": str,
        "resourceArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateApplicationResponseTypeDef = TypedDict(
    "CreateApplicationResponseTypeDef",
    {
        "application": ApplicationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteApplicationResponseTypeDef = TypedDict(
    "DeleteApplicationResponseTypeDef",
    {
        "application": ApplicationSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateAttributeGroupResponseTypeDef = TypedDict(
    "DisassociateAttributeGroupResponseTypeDef",
    {
        "applicationArn": str,
        "attributeGroupArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateResourceResponseTypeDef = TypedDict(
    "DisassociateResourceResponseTypeDef",
    {
        "applicationArn": str,
        "resourceArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAttributeGroupResponseTypeDef = TypedDict(
    "GetAttributeGroupResponseTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "attributes": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "tags": Dict[str, str],
        "createdBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListApplicationsResponseTypeDef = TypedDict(
    "ListApplicationsResponseTypeDef",
    {
        "applications": List[ApplicationSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssociatedAttributeGroupsResponseTypeDef = TypedDict(
    "ListAssociatedAttributeGroupsResponseTypeDef",
    {
        "attributeGroups": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SyncResourceResponseTypeDef = TypedDict(
    "SyncResourceResponseTypeDef",
    {
        "applicationArn": str,
        "resourceArn": str,
        "actionTaken": SyncActionType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateApplicationResponseTypeDef = TypedDict(
    "UpdateApplicationResponseTypeDef",
    {
        "application": ApplicationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAttributeGroupsForApplicationResponseTypeDef = TypedDict(
    "ListAttributeGroupsForApplicationResponseTypeDef",
    {
        "attributeGroupsDetails": List[AttributeGroupDetailsTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAttributeGroupResponseTypeDef = TypedDict(
    "DeleteAttributeGroupResponseTypeDef",
    {
        "attributeGroup": AttributeGroupSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAttributeGroupsResponseTypeDef = TypedDict(
    "ListAttributeGroupsResponseTypeDef",
    {
        "attributeGroups": List[AttributeGroupSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAttributeGroupResponseTypeDef = TypedDict(
    "CreateAttributeGroupResponseTypeDef",
    {
        "attributeGroup": AttributeGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAttributeGroupResponseTypeDef = TypedDict(
    "UpdateAttributeGroupResponseTypeDef",
    {
        "attributeGroup": AttributeGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

IntegrationsTypeDef = TypedDict(
    "IntegrationsTypeDef",
    {
        "resourceGroup": ResourceGroupTypeDef,
    },
    total=False,
)

ResourceIntegrationsTypeDef = TypedDict(
    "ResourceIntegrationsTypeDef",
    {
        "resourceGroup": ResourceGroupTypeDef,
    },
    total=False,
)

ListApplicationsRequestListApplicationsPaginateTypeDef = TypedDict(
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef = (
    TypedDict(
        "_RequiredListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef",
        {
            "application": str,
        },
    )
)
_OptionalListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef = (
    TypedDict(
        "_OptionalListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef",
        {
            "PaginationConfig": PaginatorConfigTypeDef,
        },
        total=False,
    )
)


class ListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef(
    _RequiredListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef,
    _OptionalListAssociatedAttributeGroupsRequestListAssociatedAttributeGroupsPaginateTypeDef,
):
    pass


_RequiredListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef = TypedDict(
    "_RequiredListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef",
    {
        "application": str,
    },
)
_OptionalListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef = TypedDict(
    "_OptionalListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef(
    _RequiredListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef,
    _OptionalListAssociatedResourcesRequestListAssociatedResourcesPaginateTypeDef,
):
    pass


_RequiredListAttributeGroupsForApplicationRequestListAttributeGroupsForApplicationPaginateTypeDef = TypedDict(
    "_RequiredListAttributeGroupsForApplicationRequestListAttributeGroupsForApplicationPaginateTypeDef",
    {
        "application": str,
    },
)
_OptionalListAttributeGroupsForApplicationRequestListAttributeGroupsForApplicationPaginateTypeDef = TypedDict(
    "_OptionalListAttributeGroupsForApplicationRequestListAttributeGroupsForApplicationPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAttributeGroupsForApplicationRequestListAttributeGroupsForApplicationPaginateTypeDef(
    _RequiredListAttributeGroupsForApplicationRequestListAttributeGroupsForApplicationPaginateTypeDef,
    _OptionalListAttributeGroupsForApplicationRequestListAttributeGroupsForApplicationPaginateTypeDef,
):
    pass


ListAttributeGroupsRequestListAttributeGroupsPaginateTypeDef = TypedDict(
    "ListAttributeGroupsRequestListAttributeGroupsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ResourceInfoTypeDef = TypedDict(
    "ResourceInfoTypeDef",
    {
        "name": str,
        "arn": str,
        "resourceType": ResourceTypeType,
        "resourceDetails": ResourceDetailsTypeDef,
    },
    total=False,
)

GetConfigurationResponseTypeDef = TypedDict(
    "GetConfigurationResponseTypeDef",
    {
        "configuration": AppRegistryConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutConfigurationRequestRequestTypeDef = TypedDict(
    "PutConfigurationRequestRequestTypeDef",
    {
        "configuration": AppRegistryConfigurationTypeDef,
    },
)

GetApplicationResponseTypeDef = TypedDict(
    "GetApplicationResponseTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "creationTime": datetime,
        "lastUpdateTime": datetime,
        "associatedResourceCount": int,
        "tags": Dict[str, str],
        "integrations": IntegrationsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "name": str,
        "arn": str,
        "associationTime": datetime,
        "integrations": ResourceIntegrationsTypeDef,
    },
    total=False,
)

ListAssociatedResourcesResponseTypeDef = TypedDict(
    "ListAssociatedResourcesResponseTypeDef",
    {
        "resources": List[ResourceInfoTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAssociatedResourceResponseTypeDef = TypedDict(
    "GetAssociatedResourceResponseTypeDef",
    {
        "resource": ResourceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
