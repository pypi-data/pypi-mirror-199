"""
Type annotations for ssm-contacts service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ssm_contacts/type_defs/)

Usage::

    ```python
    from mypy_boto3_ssm_contacts.type_defs import AcceptPageRequestRequestTypeDef

    data: AcceptPageRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AcceptCodeValidationType,
    AcceptTypeType,
    ActivationStatusType,
    ChannelTypeType,
    ContactTypeType,
    DayOfWeekType,
    ReceiptTypeType,
    ShiftTypeType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AcceptPageRequestRequestTypeDef",
    "ActivateContactChannelRequestRequestTypeDef",
    "ChannelTargetInfoTypeDef",
    "ContactChannelAddressTypeDef",
    "ContactTargetInfoTypeDef",
    "ContactTypeDef",
    "HandOffTimeTypeDef",
    "ResponseMetadataTypeDef",
    "TagTypeDef",
    "CreateRotationOverrideRequestRequestTypeDef",
    "DeactivateContactChannelRequestRequestTypeDef",
    "DeleteContactChannelRequestRequestTypeDef",
    "DeleteContactRequestRequestTypeDef",
    "DeleteRotationOverrideRequestRequestTypeDef",
    "DeleteRotationRequestRequestTypeDef",
    "DescribeEngagementRequestRequestTypeDef",
    "DescribePageRequestRequestTypeDef",
    "EngagementTypeDef",
    "GetContactChannelRequestRequestTypeDef",
    "GetContactPolicyRequestRequestTypeDef",
    "GetContactRequestRequestTypeDef",
    "GetRotationOverrideRequestRequestTypeDef",
    "GetRotationRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListContactChannelsRequestRequestTypeDef",
    "ListContactsRequestRequestTypeDef",
    "TimeRangeTypeDef",
    "ListPageReceiptsRequestRequestTypeDef",
    "ReceiptTypeDef",
    "ListPageResolutionsRequestRequestTypeDef",
    "ResolutionContactTypeDef",
    "ListPagesByContactRequestRequestTypeDef",
    "PageTypeDef",
    "ListPagesByEngagementRequestRequestTypeDef",
    "PreviewOverrideTypeDef",
    "ListRotationOverridesRequestRequestTypeDef",
    "RotationOverrideTypeDef",
    "ListRotationShiftsRequestRequestTypeDef",
    "ListRotationsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PutContactPolicyRequestRequestTypeDef",
    "ShiftDetailsTypeDef",
    "SendActivationCodeRequestRequestTypeDef",
    "StartEngagementRequestRequestTypeDef",
    "StopEngagementRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "ContactChannelTypeDef",
    "CreateContactChannelRequestRequestTypeDef",
    "UpdateContactChannelRequestRequestTypeDef",
    "TargetTypeDef",
    "CoverageTimeTypeDef",
    "MonthlySettingTypeDef",
    "WeeklySettingTypeDef",
    "CreateContactChannelResultTypeDef",
    "CreateContactResultTypeDef",
    "CreateRotationOverrideResultTypeDef",
    "CreateRotationResultTypeDef",
    "DescribeEngagementResultTypeDef",
    "DescribePageResultTypeDef",
    "GetContactChannelResultTypeDef",
    "GetContactPolicyResultTypeDef",
    "GetRotationOverrideResultTypeDef",
    "ListContactsResultTypeDef",
    "StartEngagementResultTypeDef",
    "ListTagsForResourceResultTypeDef",
    "TagResourceRequestRequestTypeDef",
    "ListEngagementsResultTypeDef",
    "ListContactChannelsRequestListContactChannelsPaginateTypeDef",
    "ListContactsRequestListContactsPaginateTypeDef",
    "ListPageReceiptsRequestListPageReceiptsPaginateTypeDef",
    "ListPageResolutionsRequestListPageResolutionsPaginateTypeDef",
    "ListPagesByContactRequestListPagesByContactPaginateTypeDef",
    "ListPagesByEngagementRequestListPagesByEngagementPaginateTypeDef",
    "ListRotationOverridesRequestListRotationOverridesPaginateTypeDef",
    "ListRotationShiftsRequestListRotationShiftsPaginateTypeDef",
    "ListRotationsRequestListRotationsPaginateTypeDef",
    "ListEngagementsRequestListEngagementsPaginateTypeDef",
    "ListEngagementsRequestRequestTypeDef",
    "ListPageReceiptsResultTypeDef",
    "ListPageResolutionsResultTypeDef",
    "ListPagesByContactResultTypeDef",
    "ListPagesByEngagementResultTypeDef",
    "ListRotationOverridesResultTypeDef",
    "RotationShiftTypeDef",
    "ListContactChannelsResultTypeDef",
    "StageTypeDef",
    "RecurrenceSettingsTypeDef",
    "ListPreviewRotationShiftsResultTypeDef",
    "ListRotationShiftsResultTypeDef",
    "PlanTypeDef",
    "CreateRotationRequestRequestTypeDef",
    "GetRotationResultTypeDef",
    "ListPreviewRotationShiftsRequestListPreviewRotationShiftsPaginateTypeDef",
    "ListPreviewRotationShiftsRequestRequestTypeDef",
    "RotationTypeDef",
    "UpdateRotationRequestRequestTypeDef",
    "CreateContactRequestRequestTypeDef",
    "GetContactResultTypeDef",
    "UpdateContactRequestRequestTypeDef",
    "ListRotationsResultTypeDef",
)

_RequiredAcceptPageRequestRequestTypeDef = TypedDict(
    "_RequiredAcceptPageRequestRequestTypeDef",
    {
        "PageId": str,
        "AcceptType": AcceptTypeType,
        "AcceptCode": str,
    },
)
_OptionalAcceptPageRequestRequestTypeDef = TypedDict(
    "_OptionalAcceptPageRequestRequestTypeDef",
    {
        "ContactChannelId": str,
        "Note": str,
        "AcceptCodeValidation": AcceptCodeValidationType,
    },
    total=False,
)

class AcceptPageRequestRequestTypeDef(
    _RequiredAcceptPageRequestRequestTypeDef, _OptionalAcceptPageRequestRequestTypeDef
):
    pass

ActivateContactChannelRequestRequestTypeDef = TypedDict(
    "ActivateContactChannelRequestRequestTypeDef",
    {
        "ContactChannelId": str,
        "ActivationCode": str,
    },
)

_RequiredChannelTargetInfoTypeDef = TypedDict(
    "_RequiredChannelTargetInfoTypeDef",
    {
        "ContactChannelId": str,
    },
)
_OptionalChannelTargetInfoTypeDef = TypedDict(
    "_OptionalChannelTargetInfoTypeDef",
    {
        "RetryIntervalInMinutes": int,
    },
    total=False,
)

class ChannelTargetInfoTypeDef(
    _RequiredChannelTargetInfoTypeDef, _OptionalChannelTargetInfoTypeDef
):
    pass

ContactChannelAddressTypeDef = TypedDict(
    "ContactChannelAddressTypeDef",
    {
        "SimpleAddress": str,
    },
    total=False,
)

_RequiredContactTargetInfoTypeDef = TypedDict(
    "_RequiredContactTargetInfoTypeDef",
    {
        "IsEssential": bool,
    },
)
_OptionalContactTargetInfoTypeDef = TypedDict(
    "_OptionalContactTargetInfoTypeDef",
    {
        "ContactId": str,
    },
    total=False,
)

class ContactTargetInfoTypeDef(
    _RequiredContactTargetInfoTypeDef, _OptionalContactTargetInfoTypeDef
):
    pass

_RequiredContactTypeDef = TypedDict(
    "_RequiredContactTypeDef",
    {
        "ContactArn": str,
        "Alias": str,
        "Type": ContactTypeType,
    },
)
_OptionalContactTypeDef = TypedDict(
    "_OptionalContactTypeDef",
    {
        "DisplayName": str,
    },
    total=False,
)

class ContactTypeDef(_RequiredContactTypeDef, _OptionalContactTypeDef):
    pass

HandOffTimeTypeDef = TypedDict(
    "HandOffTimeTypeDef",
    {
        "HourOfDay": int,
        "MinuteOfHour": int,
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

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

_RequiredCreateRotationOverrideRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRotationOverrideRequestRequestTypeDef",
    {
        "RotationId": str,
        "NewContactIds": Sequence[str],
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
)
_OptionalCreateRotationOverrideRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRotationOverrideRequestRequestTypeDef",
    {
        "IdempotencyToken": str,
    },
    total=False,
)

class CreateRotationOverrideRequestRequestTypeDef(
    _RequiredCreateRotationOverrideRequestRequestTypeDef,
    _OptionalCreateRotationOverrideRequestRequestTypeDef,
):
    pass

DeactivateContactChannelRequestRequestTypeDef = TypedDict(
    "DeactivateContactChannelRequestRequestTypeDef",
    {
        "ContactChannelId": str,
    },
)

DeleteContactChannelRequestRequestTypeDef = TypedDict(
    "DeleteContactChannelRequestRequestTypeDef",
    {
        "ContactChannelId": str,
    },
)

DeleteContactRequestRequestTypeDef = TypedDict(
    "DeleteContactRequestRequestTypeDef",
    {
        "ContactId": str,
    },
)

DeleteRotationOverrideRequestRequestTypeDef = TypedDict(
    "DeleteRotationOverrideRequestRequestTypeDef",
    {
        "RotationId": str,
        "RotationOverrideId": str,
    },
)

DeleteRotationRequestRequestTypeDef = TypedDict(
    "DeleteRotationRequestRequestTypeDef",
    {
        "RotationId": str,
    },
)

DescribeEngagementRequestRequestTypeDef = TypedDict(
    "DescribeEngagementRequestRequestTypeDef",
    {
        "EngagementId": str,
    },
)

DescribePageRequestRequestTypeDef = TypedDict(
    "DescribePageRequestRequestTypeDef",
    {
        "PageId": str,
    },
)

_RequiredEngagementTypeDef = TypedDict(
    "_RequiredEngagementTypeDef",
    {
        "EngagementArn": str,
        "ContactArn": str,
        "Sender": str,
    },
)
_OptionalEngagementTypeDef = TypedDict(
    "_OptionalEngagementTypeDef",
    {
        "IncidentId": str,
        "StartTime": datetime,
        "StopTime": datetime,
    },
    total=False,
)

class EngagementTypeDef(_RequiredEngagementTypeDef, _OptionalEngagementTypeDef):
    pass

GetContactChannelRequestRequestTypeDef = TypedDict(
    "GetContactChannelRequestRequestTypeDef",
    {
        "ContactChannelId": str,
    },
)

GetContactPolicyRequestRequestTypeDef = TypedDict(
    "GetContactPolicyRequestRequestTypeDef",
    {
        "ContactArn": str,
    },
)

GetContactRequestRequestTypeDef = TypedDict(
    "GetContactRequestRequestTypeDef",
    {
        "ContactId": str,
    },
)

GetRotationOverrideRequestRequestTypeDef = TypedDict(
    "GetRotationOverrideRequestRequestTypeDef",
    {
        "RotationId": str,
        "RotationOverrideId": str,
    },
)

GetRotationRequestRequestTypeDef = TypedDict(
    "GetRotationRequestRequestTypeDef",
    {
        "RotationId": str,
    },
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

_RequiredListContactChannelsRequestRequestTypeDef = TypedDict(
    "_RequiredListContactChannelsRequestRequestTypeDef",
    {
        "ContactId": str,
    },
)
_OptionalListContactChannelsRequestRequestTypeDef = TypedDict(
    "_OptionalListContactChannelsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListContactChannelsRequestRequestTypeDef(
    _RequiredListContactChannelsRequestRequestTypeDef,
    _OptionalListContactChannelsRequestRequestTypeDef,
):
    pass

ListContactsRequestRequestTypeDef = TypedDict(
    "ListContactsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "AliasPrefix": str,
        "Type": ContactTypeType,
    },
    total=False,
)

TimeRangeTypeDef = TypedDict(
    "TimeRangeTypeDef",
    {
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
    total=False,
)

_RequiredListPageReceiptsRequestRequestTypeDef = TypedDict(
    "_RequiredListPageReceiptsRequestRequestTypeDef",
    {
        "PageId": str,
    },
)
_OptionalListPageReceiptsRequestRequestTypeDef = TypedDict(
    "_OptionalListPageReceiptsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListPageReceiptsRequestRequestTypeDef(
    _RequiredListPageReceiptsRequestRequestTypeDef, _OptionalListPageReceiptsRequestRequestTypeDef
):
    pass

_RequiredReceiptTypeDef = TypedDict(
    "_RequiredReceiptTypeDef",
    {
        "ReceiptType": ReceiptTypeType,
        "ReceiptTime": datetime,
    },
)
_OptionalReceiptTypeDef = TypedDict(
    "_OptionalReceiptTypeDef",
    {
        "ContactChannelArn": str,
        "ReceiptInfo": str,
    },
    total=False,
)

class ReceiptTypeDef(_RequiredReceiptTypeDef, _OptionalReceiptTypeDef):
    pass

_RequiredListPageResolutionsRequestRequestTypeDef = TypedDict(
    "_RequiredListPageResolutionsRequestRequestTypeDef",
    {
        "PageId": str,
    },
)
_OptionalListPageResolutionsRequestRequestTypeDef = TypedDict(
    "_OptionalListPageResolutionsRequestRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

class ListPageResolutionsRequestRequestTypeDef(
    _RequiredListPageResolutionsRequestRequestTypeDef,
    _OptionalListPageResolutionsRequestRequestTypeDef,
):
    pass

_RequiredResolutionContactTypeDef = TypedDict(
    "_RequiredResolutionContactTypeDef",
    {
        "ContactArn": str,
        "Type": ContactTypeType,
    },
)
_OptionalResolutionContactTypeDef = TypedDict(
    "_OptionalResolutionContactTypeDef",
    {
        "StageIndex": int,
    },
    total=False,
)

class ResolutionContactTypeDef(
    _RequiredResolutionContactTypeDef, _OptionalResolutionContactTypeDef
):
    pass

_RequiredListPagesByContactRequestRequestTypeDef = TypedDict(
    "_RequiredListPagesByContactRequestRequestTypeDef",
    {
        "ContactId": str,
    },
)
_OptionalListPagesByContactRequestRequestTypeDef = TypedDict(
    "_OptionalListPagesByContactRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListPagesByContactRequestRequestTypeDef(
    _RequiredListPagesByContactRequestRequestTypeDef,
    _OptionalListPagesByContactRequestRequestTypeDef,
):
    pass

_RequiredPageTypeDef = TypedDict(
    "_RequiredPageTypeDef",
    {
        "PageArn": str,
        "EngagementArn": str,
        "ContactArn": str,
        "Sender": str,
    },
)
_OptionalPageTypeDef = TypedDict(
    "_OptionalPageTypeDef",
    {
        "IncidentId": str,
        "SentTime": datetime,
        "DeliveryTime": datetime,
        "ReadTime": datetime,
    },
    total=False,
)

class PageTypeDef(_RequiredPageTypeDef, _OptionalPageTypeDef):
    pass

_RequiredListPagesByEngagementRequestRequestTypeDef = TypedDict(
    "_RequiredListPagesByEngagementRequestRequestTypeDef",
    {
        "EngagementId": str,
    },
)
_OptionalListPagesByEngagementRequestRequestTypeDef = TypedDict(
    "_OptionalListPagesByEngagementRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListPagesByEngagementRequestRequestTypeDef(
    _RequiredListPagesByEngagementRequestRequestTypeDef,
    _OptionalListPagesByEngagementRequestRequestTypeDef,
):
    pass

PreviewOverrideTypeDef = TypedDict(
    "PreviewOverrideTypeDef",
    {
        "NewMembers": Sequence[str],
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
    total=False,
)

_RequiredListRotationOverridesRequestRequestTypeDef = TypedDict(
    "_RequiredListRotationOverridesRequestRequestTypeDef",
    {
        "RotationId": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
)
_OptionalListRotationOverridesRequestRequestTypeDef = TypedDict(
    "_OptionalListRotationOverridesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListRotationOverridesRequestRequestTypeDef(
    _RequiredListRotationOverridesRequestRequestTypeDef,
    _OptionalListRotationOverridesRequestRequestTypeDef,
):
    pass

RotationOverrideTypeDef = TypedDict(
    "RotationOverrideTypeDef",
    {
        "RotationOverrideId": str,
        "NewContactIds": List[str],
        "StartTime": datetime,
        "EndTime": datetime,
        "CreateTime": datetime,
    },
)

_RequiredListRotationShiftsRequestRequestTypeDef = TypedDict(
    "_RequiredListRotationShiftsRequestRequestTypeDef",
    {
        "RotationId": str,
        "EndTime": Union[datetime, str],
    },
)
_OptionalListRotationShiftsRequestRequestTypeDef = TypedDict(
    "_OptionalListRotationShiftsRequestRequestTypeDef",
    {
        "StartTime": Union[datetime, str],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListRotationShiftsRequestRequestTypeDef(
    _RequiredListRotationShiftsRequestRequestTypeDef,
    _OptionalListRotationShiftsRequestRequestTypeDef,
):
    pass

ListRotationsRequestRequestTypeDef = TypedDict(
    "ListRotationsRequestRequestTypeDef",
    {
        "RotationNamePrefix": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
    },
)

PutContactPolicyRequestRequestTypeDef = TypedDict(
    "PutContactPolicyRequestRequestTypeDef",
    {
        "ContactArn": str,
        "Policy": str,
    },
)

ShiftDetailsTypeDef = TypedDict(
    "ShiftDetailsTypeDef",
    {
        "OverriddenContactIds": List[str],
    },
)

SendActivationCodeRequestRequestTypeDef = TypedDict(
    "SendActivationCodeRequestRequestTypeDef",
    {
        "ContactChannelId": str,
    },
)

_RequiredStartEngagementRequestRequestTypeDef = TypedDict(
    "_RequiredStartEngagementRequestRequestTypeDef",
    {
        "ContactId": str,
        "Sender": str,
        "Subject": str,
        "Content": str,
    },
)
_OptionalStartEngagementRequestRequestTypeDef = TypedDict(
    "_OptionalStartEngagementRequestRequestTypeDef",
    {
        "PublicSubject": str,
        "PublicContent": str,
        "IncidentId": str,
        "IdempotencyToken": str,
    },
    total=False,
)

class StartEngagementRequestRequestTypeDef(
    _RequiredStartEngagementRequestRequestTypeDef, _OptionalStartEngagementRequestRequestTypeDef
):
    pass

_RequiredStopEngagementRequestRequestTypeDef = TypedDict(
    "_RequiredStopEngagementRequestRequestTypeDef",
    {
        "EngagementId": str,
    },
)
_OptionalStopEngagementRequestRequestTypeDef = TypedDict(
    "_OptionalStopEngagementRequestRequestTypeDef",
    {
        "Reason": str,
    },
    total=False,
)

class StopEngagementRequestRequestTypeDef(
    _RequiredStopEngagementRequestRequestTypeDef, _OptionalStopEngagementRequestRequestTypeDef
):
    pass

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredContactChannelTypeDef = TypedDict(
    "_RequiredContactChannelTypeDef",
    {
        "ContactChannelArn": str,
        "ContactArn": str,
        "Name": str,
        "DeliveryAddress": ContactChannelAddressTypeDef,
        "ActivationStatus": ActivationStatusType,
    },
)
_OptionalContactChannelTypeDef = TypedDict(
    "_OptionalContactChannelTypeDef",
    {
        "Type": ChannelTypeType,
    },
    total=False,
)

class ContactChannelTypeDef(_RequiredContactChannelTypeDef, _OptionalContactChannelTypeDef):
    pass

_RequiredCreateContactChannelRequestRequestTypeDef = TypedDict(
    "_RequiredCreateContactChannelRequestRequestTypeDef",
    {
        "ContactId": str,
        "Name": str,
        "Type": ChannelTypeType,
        "DeliveryAddress": ContactChannelAddressTypeDef,
    },
)
_OptionalCreateContactChannelRequestRequestTypeDef = TypedDict(
    "_OptionalCreateContactChannelRequestRequestTypeDef",
    {
        "DeferActivation": bool,
        "IdempotencyToken": str,
    },
    total=False,
)

class CreateContactChannelRequestRequestTypeDef(
    _RequiredCreateContactChannelRequestRequestTypeDef,
    _OptionalCreateContactChannelRequestRequestTypeDef,
):
    pass

_RequiredUpdateContactChannelRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateContactChannelRequestRequestTypeDef",
    {
        "ContactChannelId": str,
    },
)
_OptionalUpdateContactChannelRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateContactChannelRequestRequestTypeDef",
    {
        "Name": str,
        "DeliveryAddress": ContactChannelAddressTypeDef,
    },
    total=False,
)

class UpdateContactChannelRequestRequestTypeDef(
    _RequiredUpdateContactChannelRequestRequestTypeDef,
    _OptionalUpdateContactChannelRequestRequestTypeDef,
):
    pass

TargetTypeDef = TypedDict(
    "TargetTypeDef",
    {
        "ChannelTargetInfo": ChannelTargetInfoTypeDef,
        "ContactTargetInfo": ContactTargetInfoTypeDef,
    },
    total=False,
)

CoverageTimeTypeDef = TypedDict(
    "CoverageTimeTypeDef",
    {
        "Start": HandOffTimeTypeDef,
        "End": HandOffTimeTypeDef,
    },
    total=False,
)

MonthlySettingTypeDef = TypedDict(
    "MonthlySettingTypeDef",
    {
        "DayOfMonth": int,
        "HandOffTime": HandOffTimeTypeDef,
    },
)

WeeklySettingTypeDef = TypedDict(
    "WeeklySettingTypeDef",
    {
        "DayOfWeek": DayOfWeekType,
        "HandOffTime": HandOffTimeTypeDef,
    },
)

CreateContactChannelResultTypeDef = TypedDict(
    "CreateContactChannelResultTypeDef",
    {
        "ContactChannelArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateContactResultTypeDef = TypedDict(
    "CreateContactResultTypeDef",
    {
        "ContactArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRotationOverrideResultTypeDef = TypedDict(
    "CreateRotationOverrideResultTypeDef",
    {
        "RotationOverrideId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRotationResultTypeDef = TypedDict(
    "CreateRotationResultTypeDef",
    {
        "RotationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEngagementResultTypeDef = TypedDict(
    "DescribeEngagementResultTypeDef",
    {
        "ContactArn": str,
        "EngagementArn": str,
        "Sender": str,
        "Subject": str,
        "Content": str,
        "PublicSubject": str,
        "PublicContent": str,
        "IncidentId": str,
        "StartTime": datetime,
        "StopTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePageResultTypeDef = TypedDict(
    "DescribePageResultTypeDef",
    {
        "PageArn": str,
        "EngagementArn": str,
        "ContactArn": str,
        "Sender": str,
        "Subject": str,
        "Content": str,
        "PublicSubject": str,
        "PublicContent": str,
        "IncidentId": str,
        "SentTime": datetime,
        "ReadTime": datetime,
        "DeliveryTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetContactChannelResultTypeDef = TypedDict(
    "GetContactChannelResultTypeDef",
    {
        "ContactArn": str,
        "ContactChannelArn": str,
        "Name": str,
        "Type": ChannelTypeType,
        "DeliveryAddress": ContactChannelAddressTypeDef,
        "ActivationStatus": ActivationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetContactPolicyResultTypeDef = TypedDict(
    "GetContactPolicyResultTypeDef",
    {
        "ContactArn": str,
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRotationOverrideResultTypeDef = TypedDict(
    "GetRotationOverrideResultTypeDef",
    {
        "RotationOverrideId": str,
        "RotationArn": str,
        "NewContactIds": List[str],
        "StartTime": datetime,
        "EndTime": datetime,
        "CreateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListContactsResultTypeDef = TypedDict(
    "ListContactsResultTypeDef",
    {
        "NextToken": str,
        "Contacts": List[ContactTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartEngagementResultTypeDef = TypedDict(
    "StartEngagementResultTypeDef",
    {
        "EngagementArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResultTypeDef = TypedDict(
    "ListTagsForResourceResultTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

ListEngagementsResultTypeDef = TypedDict(
    "ListEngagementsResultTypeDef",
    {
        "NextToken": str,
        "Engagements": List[EngagementTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListContactChannelsRequestListContactChannelsPaginateTypeDef = TypedDict(
    "_RequiredListContactChannelsRequestListContactChannelsPaginateTypeDef",
    {
        "ContactId": str,
    },
)
_OptionalListContactChannelsRequestListContactChannelsPaginateTypeDef = TypedDict(
    "_OptionalListContactChannelsRequestListContactChannelsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListContactChannelsRequestListContactChannelsPaginateTypeDef(
    _RequiredListContactChannelsRequestListContactChannelsPaginateTypeDef,
    _OptionalListContactChannelsRequestListContactChannelsPaginateTypeDef,
):
    pass

ListContactsRequestListContactsPaginateTypeDef = TypedDict(
    "ListContactsRequestListContactsPaginateTypeDef",
    {
        "AliasPrefix": str,
        "Type": ContactTypeType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListPageReceiptsRequestListPageReceiptsPaginateTypeDef = TypedDict(
    "_RequiredListPageReceiptsRequestListPageReceiptsPaginateTypeDef",
    {
        "PageId": str,
    },
)
_OptionalListPageReceiptsRequestListPageReceiptsPaginateTypeDef = TypedDict(
    "_OptionalListPageReceiptsRequestListPageReceiptsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListPageReceiptsRequestListPageReceiptsPaginateTypeDef(
    _RequiredListPageReceiptsRequestListPageReceiptsPaginateTypeDef,
    _OptionalListPageReceiptsRequestListPageReceiptsPaginateTypeDef,
):
    pass

_RequiredListPageResolutionsRequestListPageResolutionsPaginateTypeDef = TypedDict(
    "_RequiredListPageResolutionsRequestListPageResolutionsPaginateTypeDef",
    {
        "PageId": str,
    },
)
_OptionalListPageResolutionsRequestListPageResolutionsPaginateTypeDef = TypedDict(
    "_OptionalListPageResolutionsRequestListPageResolutionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListPageResolutionsRequestListPageResolutionsPaginateTypeDef(
    _RequiredListPageResolutionsRequestListPageResolutionsPaginateTypeDef,
    _OptionalListPageResolutionsRequestListPageResolutionsPaginateTypeDef,
):
    pass

_RequiredListPagesByContactRequestListPagesByContactPaginateTypeDef = TypedDict(
    "_RequiredListPagesByContactRequestListPagesByContactPaginateTypeDef",
    {
        "ContactId": str,
    },
)
_OptionalListPagesByContactRequestListPagesByContactPaginateTypeDef = TypedDict(
    "_OptionalListPagesByContactRequestListPagesByContactPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListPagesByContactRequestListPagesByContactPaginateTypeDef(
    _RequiredListPagesByContactRequestListPagesByContactPaginateTypeDef,
    _OptionalListPagesByContactRequestListPagesByContactPaginateTypeDef,
):
    pass

_RequiredListPagesByEngagementRequestListPagesByEngagementPaginateTypeDef = TypedDict(
    "_RequiredListPagesByEngagementRequestListPagesByEngagementPaginateTypeDef",
    {
        "EngagementId": str,
    },
)
_OptionalListPagesByEngagementRequestListPagesByEngagementPaginateTypeDef = TypedDict(
    "_OptionalListPagesByEngagementRequestListPagesByEngagementPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListPagesByEngagementRequestListPagesByEngagementPaginateTypeDef(
    _RequiredListPagesByEngagementRequestListPagesByEngagementPaginateTypeDef,
    _OptionalListPagesByEngagementRequestListPagesByEngagementPaginateTypeDef,
):
    pass

_RequiredListRotationOverridesRequestListRotationOverridesPaginateTypeDef = TypedDict(
    "_RequiredListRotationOverridesRequestListRotationOverridesPaginateTypeDef",
    {
        "RotationId": str,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
    },
)
_OptionalListRotationOverridesRequestListRotationOverridesPaginateTypeDef = TypedDict(
    "_OptionalListRotationOverridesRequestListRotationOverridesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListRotationOverridesRequestListRotationOverridesPaginateTypeDef(
    _RequiredListRotationOverridesRequestListRotationOverridesPaginateTypeDef,
    _OptionalListRotationOverridesRequestListRotationOverridesPaginateTypeDef,
):
    pass

_RequiredListRotationShiftsRequestListRotationShiftsPaginateTypeDef = TypedDict(
    "_RequiredListRotationShiftsRequestListRotationShiftsPaginateTypeDef",
    {
        "RotationId": str,
        "EndTime": Union[datetime, str],
    },
)
_OptionalListRotationShiftsRequestListRotationShiftsPaginateTypeDef = TypedDict(
    "_OptionalListRotationShiftsRequestListRotationShiftsPaginateTypeDef",
    {
        "StartTime": Union[datetime, str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListRotationShiftsRequestListRotationShiftsPaginateTypeDef(
    _RequiredListRotationShiftsRequestListRotationShiftsPaginateTypeDef,
    _OptionalListRotationShiftsRequestListRotationShiftsPaginateTypeDef,
):
    pass

ListRotationsRequestListRotationsPaginateTypeDef = TypedDict(
    "ListRotationsRequestListRotationsPaginateTypeDef",
    {
        "RotationNamePrefix": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListEngagementsRequestListEngagementsPaginateTypeDef = TypedDict(
    "ListEngagementsRequestListEngagementsPaginateTypeDef",
    {
        "IncidentId": str,
        "TimeRangeValue": TimeRangeTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListEngagementsRequestRequestTypeDef = TypedDict(
    "ListEngagementsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "IncidentId": str,
        "TimeRangeValue": TimeRangeTypeDef,
    },
    total=False,
)

ListPageReceiptsResultTypeDef = TypedDict(
    "ListPageReceiptsResultTypeDef",
    {
        "NextToken": str,
        "Receipts": List[ReceiptTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPageResolutionsResultTypeDef = TypedDict(
    "ListPageResolutionsResultTypeDef",
    {
        "NextToken": str,
        "PageResolutions": List[ResolutionContactTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPagesByContactResultTypeDef = TypedDict(
    "ListPagesByContactResultTypeDef",
    {
        "NextToken": str,
        "Pages": List[PageTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPagesByEngagementResultTypeDef = TypedDict(
    "ListPagesByEngagementResultTypeDef",
    {
        "NextToken": str,
        "Pages": List[PageTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRotationOverridesResultTypeDef = TypedDict(
    "ListRotationOverridesResultTypeDef",
    {
        "RotationOverrides": List[RotationOverrideTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRotationShiftTypeDef = TypedDict(
    "_RequiredRotationShiftTypeDef",
    {
        "StartTime": datetime,
        "EndTime": datetime,
    },
)
_OptionalRotationShiftTypeDef = TypedDict(
    "_OptionalRotationShiftTypeDef",
    {
        "ContactIds": List[str],
        "Type": ShiftTypeType,
        "ShiftDetails": ShiftDetailsTypeDef,
    },
    total=False,
)

class RotationShiftTypeDef(_RequiredRotationShiftTypeDef, _OptionalRotationShiftTypeDef):
    pass

ListContactChannelsResultTypeDef = TypedDict(
    "ListContactChannelsResultTypeDef",
    {
        "NextToken": str,
        "ContactChannels": List[ContactChannelTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StageTypeDef = TypedDict(
    "StageTypeDef",
    {
        "DurationInMinutes": int,
        "Targets": Sequence[TargetTypeDef],
    },
)

_RequiredRecurrenceSettingsTypeDef = TypedDict(
    "_RequiredRecurrenceSettingsTypeDef",
    {
        "NumberOfOnCalls": int,
        "RecurrenceMultiplier": int,
    },
)
_OptionalRecurrenceSettingsTypeDef = TypedDict(
    "_OptionalRecurrenceSettingsTypeDef",
    {
        "MonthlySettings": Sequence[MonthlySettingTypeDef],
        "WeeklySettings": Sequence[WeeklySettingTypeDef],
        "DailySettings": Sequence[HandOffTimeTypeDef],
        "ShiftCoverages": Mapping[DayOfWeekType, Sequence[CoverageTimeTypeDef]],
    },
    total=False,
)

class RecurrenceSettingsTypeDef(
    _RequiredRecurrenceSettingsTypeDef, _OptionalRecurrenceSettingsTypeDef
):
    pass

ListPreviewRotationShiftsResultTypeDef = TypedDict(
    "ListPreviewRotationShiftsResultTypeDef",
    {
        "RotationShifts": List[RotationShiftTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRotationShiftsResultTypeDef = TypedDict(
    "ListRotationShiftsResultTypeDef",
    {
        "RotationShifts": List[RotationShiftTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PlanTypeDef = TypedDict(
    "PlanTypeDef",
    {
        "Stages": Sequence[StageTypeDef],
        "RotationIds": Sequence[str],
    },
    total=False,
)

_RequiredCreateRotationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRotationRequestRequestTypeDef",
    {
        "Name": str,
        "ContactIds": Sequence[str],
        "TimeZoneId": str,
        "Recurrence": RecurrenceSettingsTypeDef,
    },
)
_OptionalCreateRotationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRotationRequestRequestTypeDef",
    {
        "StartTime": Union[datetime, str],
        "Tags": Sequence[TagTypeDef],
        "IdempotencyToken": str,
    },
    total=False,
)

class CreateRotationRequestRequestTypeDef(
    _RequiredCreateRotationRequestRequestTypeDef, _OptionalCreateRotationRequestRequestTypeDef
):
    pass

GetRotationResultTypeDef = TypedDict(
    "GetRotationResultTypeDef",
    {
        "RotationArn": str,
        "Name": str,
        "ContactIds": List[str],
        "StartTime": datetime,
        "TimeZoneId": str,
        "Recurrence": RecurrenceSettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListPreviewRotationShiftsRequestListPreviewRotationShiftsPaginateTypeDef = TypedDict(
    "_RequiredListPreviewRotationShiftsRequestListPreviewRotationShiftsPaginateTypeDef",
    {
        "EndTime": Union[datetime, str],
        "Members": Sequence[str],
        "TimeZoneId": str,
        "Recurrence": RecurrenceSettingsTypeDef,
    },
)
_OptionalListPreviewRotationShiftsRequestListPreviewRotationShiftsPaginateTypeDef = TypedDict(
    "_OptionalListPreviewRotationShiftsRequestListPreviewRotationShiftsPaginateTypeDef",
    {
        "RotationStartTime": Union[datetime, str],
        "StartTime": Union[datetime, str],
        "Overrides": Sequence[PreviewOverrideTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListPreviewRotationShiftsRequestListPreviewRotationShiftsPaginateTypeDef(
    _RequiredListPreviewRotationShiftsRequestListPreviewRotationShiftsPaginateTypeDef,
    _OptionalListPreviewRotationShiftsRequestListPreviewRotationShiftsPaginateTypeDef,
):
    pass

_RequiredListPreviewRotationShiftsRequestRequestTypeDef = TypedDict(
    "_RequiredListPreviewRotationShiftsRequestRequestTypeDef",
    {
        "EndTime": Union[datetime, str],
        "Members": Sequence[str],
        "TimeZoneId": str,
        "Recurrence": RecurrenceSettingsTypeDef,
    },
)
_OptionalListPreviewRotationShiftsRequestRequestTypeDef = TypedDict(
    "_OptionalListPreviewRotationShiftsRequestRequestTypeDef",
    {
        "RotationStartTime": Union[datetime, str],
        "StartTime": Union[datetime, str],
        "Overrides": Sequence[PreviewOverrideTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

class ListPreviewRotationShiftsRequestRequestTypeDef(
    _RequiredListPreviewRotationShiftsRequestRequestTypeDef,
    _OptionalListPreviewRotationShiftsRequestRequestTypeDef,
):
    pass

_RequiredRotationTypeDef = TypedDict(
    "_RequiredRotationTypeDef",
    {
        "RotationArn": str,
        "Name": str,
    },
)
_OptionalRotationTypeDef = TypedDict(
    "_OptionalRotationTypeDef",
    {
        "ContactIds": List[str],
        "StartTime": datetime,
        "TimeZoneId": str,
        "Recurrence": RecurrenceSettingsTypeDef,
    },
    total=False,
)

class RotationTypeDef(_RequiredRotationTypeDef, _OptionalRotationTypeDef):
    pass

_RequiredUpdateRotationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRotationRequestRequestTypeDef",
    {
        "RotationId": str,
        "Recurrence": RecurrenceSettingsTypeDef,
    },
)
_OptionalUpdateRotationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRotationRequestRequestTypeDef",
    {
        "ContactIds": Sequence[str],
        "StartTime": Union[datetime, str],
        "TimeZoneId": str,
    },
    total=False,
)

class UpdateRotationRequestRequestTypeDef(
    _RequiredUpdateRotationRequestRequestTypeDef, _OptionalUpdateRotationRequestRequestTypeDef
):
    pass

_RequiredCreateContactRequestRequestTypeDef = TypedDict(
    "_RequiredCreateContactRequestRequestTypeDef",
    {
        "Alias": str,
        "Type": ContactTypeType,
        "Plan": PlanTypeDef,
    },
)
_OptionalCreateContactRequestRequestTypeDef = TypedDict(
    "_OptionalCreateContactRequestRequestTypeDef",
    {
        "DisplayName": str,
        "Tags": Sequence[TagTypeDef],
        "IdempotencyToken": str,
    },
    total=False,
)

class CreateContactRequestRequestTypeDef(
    _RequiredCreateContactRequestRequestTypeDef, _OptionalCreateContactRequestRequestTypeDef
):
    pass

GetContactResultTypeDef = TypedDict(
    "GetContactResultTypeDef",
    {
        "ContactArn": str,
        "Alias": str,
        "DisplayName": str,
        "Type": ContactTypeType,
        "Plan": PlanTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateContactRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateContactRequestRequestTypeDef",
    {
        "ContactId": str,
    },
)
_OptionalUpdateContactRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateContactRequestRequestTypeDef",
    {
        "DisplayName": str,
        "Plan": PlanTypeDef,
    },
    total=False,
)

class UpdateContactRequestRequestTypeDef(
    _RequiredUpdateContactRequestRequestTypeDef, _OptionalUpdateContactRequestRequestTypeDef
):
    pass

ListRotationsResultTypeDef = TypedDict(
    "ListRotationsResultTypeDef",
    {
        "NextToken": str,
        "Rotations": List[RotationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
