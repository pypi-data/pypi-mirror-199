"""
Type annotations for voice-id service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_voice_id/type_defs/)

Usage::

    ```python
    from mypy_boto3_voice_id.type_defs import AssociateFraudsterRequestRequestTypeDef

    data: AssociateFraudsterRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    AuthenticationDecisionType,
    DomainStatusType,
    DuplicateRegistrationActionType,
    ExistingEnrollmentActionType,
    FraudDetectionActionType,
    FraudDetectionDecisionType,
    FraudDetectionReasonType,
    FraudsterRegistrationJobStatusType,
    ServerSideEncryptionUpdateStatusType,
    SpeakerEnrollmentJobStatusType,
    SpeakerStatusType,
    StreamingStatusType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AssociateFraudsterRequestRequestTypeDef",
    "FraudsterTypeDef",
    "ResponseMetadataTypeDef",
    "AuthenticationConfigurationTypeDef",
    "ServerSideEncryptionConfigurationTypeDef",
    "TagTypeDef",
    "CreateWatchlistRequestRequestTypeDef",
    "WatchlistTypeDef",
    "DeleteDomainRequestRequestTypeDef",
    "DeleteFraudsterRequestRequestTypeDef",
    "DeleteSpeakerRequestRequestTypeDef",
    "DeleteWatchlistRequestRequestTypeDef",
    "DescribeDomainRequestRequestTypeDef",
    "DescribeFraudsterRegistrationJobRequestRequestTypeDef",
    "DescribeFraudsterRequestRequestTypeDef",
    "DescribeSpeakerEnrollmentJobRequestRequestTypeDef",
    "DescribeSpeakerRequestRequestTypeDef",
    "SpeakerTypeDef",
    "DescribeWatchlistRequestRequestTypeDef",
    "DisassociateFraudsterRequestRequestTypeDef",
    "ServerSideEncryptionUpdateDetailsTypeDef",
    "WatchlistDetailsTypeDef",
    "EnrollmentJobFraudDetectionConfigTypeDef",
    "EvaluateSessionRequestRequestTypeDef",
    "FailureDetailsTypeDef",
    "FraudDetectionConfigurationTypeDef",
    "KnownFraudsterRiskTypeDef",
    "VoiceSpoofingRiskTypeDef",
    "JobProgressTypeDef",
    "InputDataConfigTypeDef",
    "OutputDataConfigTypeDef",
    "RegistrationConfigTypeDef",
    "FraudsterSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "ListDomainsRequestRequestTypeDef",
    "ListFraudsterRegistrationJobsRequestRequestTypeDef",
    "ListFraudstersRequestRequestTypeDef",
    "ListSpeakerEnrollmentJobsRequestRequestTypeDef",
    "ListSpeakersRequestRequestTypeDef",
    "SpeakerSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListWatchlistsRequestRequestTypeDef",
    "WatchlistSummaryTypeDef",
    "OptOutSpeakerRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateWatchlistRequestRequestTypeDef",
    "AssociateFraudsterResponseTypeDef",
    "DescribeFraudsterResponseTypeDef",
    "DisassociateFraudsterResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "AuthenticationResultTypeDef",
    "UpdateDomainRequestRequestTypeDef",
    "CreateDomainRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateWatchlistResponseTypeDef",
    "DescribeWatchlistResponseTypeDef",
    "UpdateWatchlistResponseTypeDef",
    "DescribeSpeakerResponseTypeDef",
    "OptOutSpeakerResponseTypeDef",
    "DomainSummaryTypeDef",
    "DomainTypeDef",
    "EnrollmentConfigTypeDef",
    "FraudRiskDetailsTypeDef",
    "FraudsterRegistrationJobSummaryTypeDef",
    "SpeakerEnrollmentJobSummaryTypeDef",
    "FraudsterRegistrationJobTypeDef",
    "StartFraudsterRegistrationJobRequestRequestTypeDef",
    "ListFraudstersResponseTypeDef",
    "ListDomainsRequestListDomainsPaginateTypeDef",
    "ListFraudsterRegistrationJobsRequestListFraudsterRegistrationJobsPaginateTypeDef",
    "ListFraudstersRequestListFraudstersPaginateTypeDef",
    "ListSpeakerEnrollmentJobsRequestListSpeakerEnrollmentJobsPaginateTypeDef",
    "ListSpeakersRequestListSpeakersPaginateTypeDef",
    "ListWatchlistsRequestListWatchlistsPaginateTypeDef",
    "ListSpeakersResponseTypeDef",
    "ListWatchlistsResponseTypeDef",
    "ListDomainsResponseTypeDef",
    "CreateDomainResponseTypeDef",
    "DescribeDomainResponseTypeDef",
    "UpdateDomainResponseTypeDef",
    "SpeakerEnrollmentJobTypeDef",
    "StartSpeakerEnrollmentJobRequestRequestTypeDef",
    "FraudDetectionResultTypeDef",
    "ListFraudsterRegistrationJobsResponseTypeDef",
    "ListSpeakerEnrollmentJobsResponseTypeDef",
    "DescribeFraudsterRegistrationJobResponseTypeDef",
    "StartFraudsterRegistrationJobResponseTypeDef",
    "DescribeSpeakerEnrollmentJobResponseTypeDef",
    "StartSpeakerEnrollmentJobResponseTypeDef",
    "EvaluateSessionResponseTypeDef",
)

AssociateFraudsterRequestRequestTypeDef = TypedDict(
    "AssociateFraudsterRequestRequestTypeDef",
    {
        "DomainId": str,
        "FraudsterId": str,
        "WatchlistId": str,
    },
)

FraudsterTypeDef = TypedDict(
    "FraudsterTypeDef",
    {
        "CreatedAt": datetime,
        "DomainId": str,
        "GeneratedFraudsterId": str,
        "WatchlistIds": List[str],
    },
    total=False,
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

AuthenticationConfigurationTypeDef = TypedDict(
    "AuthenticationConfigurationTypeDef",
    {
        "AcceptanceThreshold": int,
    },
)

ServerSideEncryptionConfigurationTypeDef = TypedDict(
    "ServerSideEncryptionConfigurationTypeDef",
    {
        "KmsKeyId": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

_RequiredCreateWatchlistRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWatchlistRequestRequestTypeDef",
    {
        "DomainId": str,
        "Name": str,
    },
)
_OptionalCreateWatchlistRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWatchlistRequestRequestTypeDef",
    {
        "ClientToken": str,
        "Description": str,
    },
    total=False,
)

class CreateWatchlistRequestRequestTypeDef(
    _RequiredCreateWatchlistRequestRequestTypeDef, _OptionalCreateWatchlistRequestRequestTypeDef
):
    pass

WatchlistTypeDef = TypedDict(
    "WatchlistTypeDef",
    {
        "CreatedAt": datetime,
        "DefaultWatchlist": bool,
        "Description": str,
        "DomainId": str,
        "Name": str,
        "UpdatedAt": datetime,
        "WatchlistId": str,
    },
    total=False,
)

DeleteDomainRequestRequestTypeDef = TypedDict(
    "DeleteDomainRequestRequestTypeDef",
    {
        "DomainId": str,
    },
)

DeleteFraudsterRequestRequestTypeDef = TypedDict(
    "DeleteFraudsterRequestRequestTypeDef",
    {
        "DomainId": str,
        "FraudsterId": str,
    },
)

DeleteSpeakerRequestRequestTypeDef = TypedDict(
    "DeleteSpeakerRequestRequestTypeDef",
    {
        "DomainId": str,
        "SpeakerId": str,
    },
)

DeleteWatchlistRequestRequestTypeDef = TypedDict(
    "DeleteWatchlistRequestRequestTypeDef",
    {
        "DomainId": str,
        "WatchlistId": str,
    },
)

DescribeDomainRequestRequestTypeDef = TypedDict(
    "DescribeDomainRequestRequestTypeDef",
    {
        "DomainId": str,
    },
)

DescribeFraudsterRegistrationJobRequestRequestTypeDef = TypedDict(
    "DescribeFraudsterRegistrationJobRequestRequestTypeDef",
    {
        "DomainId": str,
        "JobId": str,
    },
)

DescribeFraudsterRequestRequestTypeDef = TypedDict(
    "DescribeFraudsterRequestRequestTypeDef",
    {
        "DomainId": str,
        "FraudsterId": str,
    },
)

DescribeSpeakerEnrollmentJobRequestRequestTypeDef = TypedDict(
    "DescribeSpeakerEnrollmentJobRequestRequestTypeDef",
    {
        "DomainId": str,
        "JobId": str,
    },
)

DescribeSpeakerRequestRequestTypeDef = TypedDict(
    "DescribeSpeakerRequestRequestTypeDef",
    {
        "DomainId": str,
        "SpeakerId": str,
    },
)

SpeakerTypeDef = TypedDict(
    "SpeakerTypeDef",
    {
        "CreatedAt": datetime,
        "CustomerSpeakerId": str,
        "DomainId": str,
        "GeneratedSpeakerId": str,
        "LastAccessedAt": datetime,
        "Status": SpeakerStatusType,
        "UpdatedAt": datetime,
    },
    total=False,
)

DescribeWatchlistRequestRequestTypeDef = TypedDict(
    "DescribeWatchlistRequestRequestTypeDef",
    {
        "DomainId": str,
        "WatchlistId": str,
    },
)

DisassociateFraudsterRequestRequestTypeDef = TypedDict(
    "DisassociateFraudsterRequestRequestTypeDef",
    {
        "DomainId": str,
        "FraudsterId": str,
        "WatchlistId": str,
    },
)

ServerSideEncryptionUpdateDetailsTypeDef = TypedDict(
    "ServerSideEncryptionUpdateDetailsTypeDef",
    {
        "Message": str,
        "OldKmsKeyId": str,
        "UpdateStatus": ServerSideEncryptionUpdateStatusType,
    },
    total=False,
)

WatchlistDetailsTypeDef = TypedDict(
    "WatchlistDetailsTypeDef",
    {
        "DefaultWatchlistId": str,
    },
)

EnrollmentJobFraudDetectionConfigTypeDef = TypedDict(
    "EnrollmentJobFraudDetectionConfigTypeDef",
    {
        "FraudDetectionAction": FraudDetectionActionType,
        "RiskThreshold": int,
        "WatchlistIds": List[str],
    },
    total=False,
)

EvaluateSessionRequestRequestTypeDef = TypedDict(
    "EvaluateSessionRequestRequestTypeDef",
    {
        "DomainId": str,
        "SessionNameOrId": str,
    },
)

FailureDetailsTypeDef = TypedDict(
    "FailureDetailsTypeDef",
    {
        "Message": str,
        "StatusCode": int,
    },
    total=False,
)

FraudDetectionConfigurationTypeDef = TypedDict(
    "FraudDetectionConfigurationTypeDef",
    {
        "RiskThreshold": int,
        "WatchlistId": str,
    },
    total=False,
)

_RequiredKnownFraudsterRiskTypeDef = TypedDict(
    "_RequiredKnownFraudsterRiskTypeDef",
    {
        "RiskScore": int,
    },
)
_OptionalKnownFraudsterRiskTypeDef = TypedDict(
    "_OptionalKnownFraudsterRiskTypeDef",
    {
        "GeneratedFraudsterId": str,
    },
    total=False,
)

class KnownFraudsterRiskTypeDef(
    _RequiredKnownFraudsterRiskTypeDef, _OptionalKnownFraudsterRiskTypeDef
):
    pass

VoiceSpoofingRiskTypeDef = TypedDict(
    "VoiceSpoofingRiskTypeDef",
    {
        "RiskScore": int,
    },
)

JobProgressTypeDef = TypedDict(
    "JobProgressTypeDef",
    {
        "PercentComplete": int,
    },
    total=False,
)

InputDataConfigTypeDef = TypedDict(
    "InputDataConfigTypeDef",
    {
        "S3Uri": str,
    },
)

_RequiredOutputDataConfigTypeDef = TypedDict(
    "_RequiredOutputDataConfigTypeDef",
    {
        "S3Uri": str,
    },
)
_OptionalOutputDataConfigTypeDef = TypedDict(
    "_OptionalOutputDataConfigTypeDef",
    {
        "KmsKeyId": str,
    },
    total=False,
)

class OutputDataConfigTypeDef(_RequiredOutputDataConfigTypeDef, _OptionalOutputDataConfigTypeDef):
    pass

RegistrationConfigTypeDef = TypedDict(
    "RegistrationConfigTypeDef",
    {
        "DuplicateRegistrationAction": DuplicateRegistrationActionType,
        "FraudsterSimilarityThreshold": int,
        "WatchlistIds": List[str],
    },
    total=False,
)

FraudsterSummaryTypeDef = TypedDict(
    "FraudsterSummaryTypeDef",
    {
        "CreatedAt": datetime,
        "DomainId": str,
        "GeneratedFraudsterId": str,
        "WatchlistIds": List[str],
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

ListDomainsRequestRequestTypeDef = TypedDict(
    "ListDomainsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListFraudsterRegistrationJobsRequestRequestTypeDef = TypedDict(
    "_RequiredListFraudsterRegistrationJobsRequestRequestTypeDef",
    {
        "DomainId": str,
    },
)
_OptionalListFraudsterRegistrationJobsRequestRequestTypeDef = TypedDict(
    "_OptionalListFraudsterRegistrationJobsRequestRequestTypeDef",
    {
        "JobStatus": FraudsterRegistrationJobStatusType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListFraudsterRegistrationJobsRequestRequestTypeDef(
    _RequiredListFraudsterRegistrationJobsRequestRequestTypeDef,
    _OptionalListFraudsterRegistrationJobsRequestRequestTypeDef,
):
    pass

_RequiredListFraudstersRequestRequestTypeDef = TypedDict(
    "_RequiredListFraudstersRequestRequestTypeDef",
    {
        "DomainId": str,
    },
)
_OptionalListFraudstersRequestRequestTypeDef = TypedDict(
    "_OptionalListFraudstersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "WatchlistId": str,
    },
    total=False,
)

class ListFraudstersRequestRequestTypeDef(
    _RequiredListFraudstersRequestRequestTypeDef, _OptionalListFraudstersRequestRequestTypeDef
):
    pass

_RequiredListSpeakerEnrollmentJobsRequestRequestTypeDef = TypedDict(
    "_RequiredListSpeakerEnrollmentJobsRequestRequestTypeDef",
    {
        "DomainId": str,
    },
)
_OptionalListSpeakerEnrollmentJobsRequestRequestTypeDef = TypedDict(
    "_OptionalListSpeakerEnrollmentJobsRequestRequestTypeDef",
    {
        "JobStatus": SpeakerEnrollmentJobStatusType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListSpeakerEnrollmentJobsRequestRequestTypeDef(
    _RequiredListSpeakerEnrollmentJobsRequestRequestTypeDef,
    _OptionalListSpeakerEnrollmentJobsRequestRequestTypeDef,
):
    pass

_RequiredListSpeakersRequestRequestTypeDef = TypedDict(
    "_RequiredListSpeakersRequestRequestTypeDef",
    {
        "DomainId": str,
    },
)
_OptionalListSpeakersRequestRequestTypeDef = TypedDict(
    "_OptionalListSpeakersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListSpeakersRequestRequestTypeDef(
    _RequiredListSpeakersRequestRequestTypeDef, _OptionalListSpeakersRequestRequestTypeDef
):
    pass

SpeakerSummaryTypeDef = TypedDict(
    "SpeakerSummaryTypeDef",
    {
        "CreatedAt": datetime,
        "CustomerSpeakerId": str,
        "DomainId": str,
        "GeneratedSpeakerId": str,
        "LastAccessedAt": datetime,
        "Status": SpeakerStatusType,
        "UpdatedAt": datetime,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

_RequiredListWatchlistsRequestRequestTypeDef = TypedDict(
    "_RequiredListWatchlistsRequestRequestTypeDef",
    {
        "DomainId": str,
    },
)
_OptionalListWatchlistsRequestRequestTypeDef = TypedDict(
    "_OptionalListWatchlistsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListWatchlistsRequestRequestTypeDef(
    _RequiredListWatchlistsRequestRequestTypeDef, _OptionalListWatchlistsRequestRequestTypeDef
):
    pass

WatchlistSummaryTypeDef = TypedDict(
    "WatchlistSummaryTypeDef",
    {
        "CreatedAt": datetime,
        "DefaultWatchlist": bool,
        "Description": str,
        "DomainId": str,
        "Name": str,
        "UpdatedAt": datetime,
        "WatchlistId": str,
    },
    total=False,
)

OptOutSpeakerRequestRequestTypeDef = TypedDict(
    "OptOutSpeakerRequestRequestTypeDef",
    {
        "DomainId": str,
        "SpeakerId": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateWatchlistRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWatchlistRequestRequestTypeDef",
    {
        "DomainId": str,
        "WatchlistId": str,
    },
)
_OptionalUpdateWatchlistRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWatchlistRequestRequestTypeDef",
    {
        "Description": str,
        "Name": str,
    },
    total=False,
)

class UpdateWatchlistRequestRequestTypeDef(
    _RequiredUpdateWatchlistRequestRequestTypeDef, _OptionalUpdateWatchlistRequestRequestTypeDef
):
    pass

AssociateFraudsterResponseTypeDef = TypedDict(
    "AssociateFraudsterResponseTypeDef",
    {
        "Fraudster": FraudsterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFraudsterResponseTypeDef = TypedDict(
    "DescribeFraudsterResponseTypeDef",
    {
        "Fraudster": FraudsterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateFraudsterResponseTypeDef = TypedDict(
    "DisassociateFraudsterResponseTypeDef",
    {
        "Fraudster": FraudsterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AuthenticationResultTypeDef = TypedDict(
    "AuthenticationResultTypeDef",
    {
        "AudioAggregationEndedAt": datetime,
        "AudioAggregationStartedAt": datetime,
        "AuthenticationResultId": str,
        "Configuration": AuthenticationConfigurationTypeDef,
        "CustomerSpeakerId": str,
        "Decision": AuthenticationDecisionType,
        "GeneratedSpeakerId": str,
        "Score": int,
    },
    total=False,
)

_RequiredUpdateDomainRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDomainRequestRequestTypeDef",
    {
        "DomainId": str,
        "Name": str,
        "ServerSideEncryptionConfiguration": ServerSideEncryptionConfigurationTypeDef,
    },
)
_OptionalUpdateDomainRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDomainRequestRequestTypeDef",
    {
        "Description": str,
    },
    total=False,
)

class UpdateDomainRequestRequestTypeDef(
    _RequiredUpdateDomainRequestRequestTypeDef, _OptionalUpdateDomainRequestRequestTypeDef
):
    pass

_RequiredCreateDomainRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDomainRequestRequestTypeDef",
    {
        "Name": str,
        "ServerSideEncryptionConfiguration": ServerSideEncryptionConfigurationTypeDef,
    },
)
_OptionalCreateDomainRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDomainRequestRequestTypeDef",
    {
        "ClientToken": str,
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateDomainRequestRequestTypeDef(
    _RequiredCreateDomainRequestRequestTypeDef, _OptionalCreateDomainRequestRequestTypeDef
):
    pass

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateWatchlistResponseTypeDef = TypedDict(
    "CreateWatchlistResponseTypeDef",
    {
        "Watchlist": WatchlistTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeWatchlistResponseTypeDef = TypedDict(
    "DescribeWatchlistResponseTypeDef",
    {
        "Watchlist": WatchlistTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateWatchlistResponseTypeDef = TypedDict(
    "UpdateWatchlistResponseTypeDef",
    {
        "Watchlist": WatchlistTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSpeakerResponseTypeDef = TypedDict(
    "DescribeSpeakerResponseTypeDef",
    {
        "Speaker": SpeakerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OptOutSpeakerResponseTypeDef = TypedDict(
    "OptOutSpeakerResponseTypeDef",
    {
        "Speaker": SpeakerTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DomainSummaryTypeDef = TypedDict(
    "DomainSummaryTypeDef",
    {
        "Arn": str,
        "CreatedAt": datetime,
        "Description": str,
        "DomainId": str,
        "DomainStatus": DomainStatusType,
        "Name": str,
        "ServerSideEncryptionConfiguration": ServerSideEncryptionConfigurationTypeDef,
        "ServerSideEncryptionUpdateDetails": ServerSideEncryptionUpdateDetailsTypeDef,
        "UpdatedAt": datetime,
        "WatchlistDetails": WatchlistDetailsTypeDef,
    },
    total=False,
)

DomainTypeDef = TypedDict(
    "DomainTypeDef",
    {
        "Arn": str,
        "CreatedAt": datetime,
        "Description": str,
        "DomainId": str,
        "DomainStatus": DomainStatusType,
        "Name": str,
        "ServerSideEncryptionConfiguration": ServerSideEncryptionConfigurationTypeDef,
        "ServerSideEncryptionUpdateDetails": ServerSideEncryptionUpdateDetailsTypeDef,
        "UpdatedAt": datetime,
        "WatchlistDetails": WatchlistDetailsTypeDef,
    },
    total=False,
)

EnrollmentConfigTypeDef = TypedDict(
    "EnrollmentConfigTypeDef",
    {
        "ExistingEnrollmentAction": ExistingEnrollmentActionType,
        "FraudDetectionConfig": EnrollmentJobFraudDetectionConfigTypeDef,
    },
    total=False,
)

FraudRiskDetailsTypeDef = TypedDict(
    "FraudRiskDetailsTypeDef",
    {
        "KnownFraudsterRisk": KnownFraudsterRiskTypeDef,
        "VoiceSpoofingRisk": VoiceSpoofingRiskTypeDef,
    },
)

FraudsterRegistrationJobSummaryTypeDef = TypedDict(
    "FraudsterRegistrationJobSummaryTypeDef",
    {
        "CreatedAt": datetime,
        "DomainId": str,
        "EndedAt": datetime,
        "FailureDetails": FailureDetailsTypeDef,
        "JobId": str,
        "JobName": str,
        "JobProgress": JobProgressTypeDef,
        "JobStatus": FraudsterRegistrationJobStatusType,
    },
    total=False,
)

SpeakerEnrollmentJobSummaryTypeDef = TypedDict(
    "SpeakerEnrollmentJobSummaryTypeDef",
    {
        "CreatedAt": datetime,
        "DomainId": str,
        "EndedAt": datetime,
        "FailureDetails": FailureDetailsTypeDef,
        "JobId": str,
        "JobName": str,
        "JobProgress": JobProgressTypeDef,
        "JobStatus": SpeakerEnrollmentJobStatusType,
    },
    total=False,
)

FraudsterRegistrationJobTypeDef = TypedDict(
    "FraudsterRegistrationJobTypeDef",
    {
        "CreatedAt": datetime,
        "DataAccessRoleArn": str,
        "DomainId": str,
        "EndedAt": datetime,
        "FailureDetails": FailureDetailsTypeDef,
        "InputDataConfig": InputDataConfigTypeDef,
        "JobId": str,
        "JobName": str,
        "JobProgress": JobProgressTypeDef,
        "JobStatus": FraudsterRegistrationJobStatusType,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "RegistrationConfig": RegistrationConfigTypeDef,
    },
    total=False,
)

_RequiredStartFraudsterRegistrationJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartFraudsterRegistrationJobRequestRequestTypeDef",
    {
        "DataAccessRoleArn": str,
        "DomainId": str,
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
    },
)
_OptionalStartFraudsterRegistrationJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartFraudsterRegistrationJobRequestRequestTypeDef",
    {
        "ClientToken": str,
        "JobName": str,
        "RegistrationConfig": RegistrationConfigTypeDef,
    },
    total=False,
)

class StartFraudsterRegistrationJobRequestRequestTypeDef(
    _RequiredStartFraudsterRegistrationJobRequestRequestTypeDef,
    _OptionalStartFraudsterRegistrationJobRequestRequestTypeDef,
):
    pass

ListFraudstersResponseTypeDef = TypedDict(
    "ListFraudstersResponseTypeDef",
    {
        "FraudsterSummaries": List[FraudsterSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDomainsRequestListDomainsPaginateTypeDef = TypedDict(
    "ListDomainsRequestListDomainsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListFraudsterRegistrationJobsRequestListFraudsterRegistrationJobsPaginateTypeDef = (
    TypedDict(
        "_RequiredListFraudsterRegistrationJobsRequestListFraudsterRegistrationJobsPaginateTypeDef",
        {
            "DomainId": str,
        },
    )
)
_OptionalListFraudsterRegistrationJobsRequestListFraudsterRegistrationJobsPaginateTypeDef = (
    TypedDict(
        "_OptionalListFraudsterRegistrationJobsRequestListFraudsterRegistrationJobsPaginateTypeDef",
        {
            "JobStatus": FraudsterRegistrationJobStatusType,
            "PaginationConfig": PaginatorConfigTypeDef,
        },
        total=False,
    )
)

class ListFraudsterRegistrationJobsRequestListFraudsterRegistrationJobsPaginateTypeDef(
    _RequiredListFraudsterRegistrationJobsRequestListFraudsterRegistrationJobsPaginateTypeDef,
    _OptionalListFraudsterRegistrationJobsRequestListFraudsterRegistrationJobsPaginateTypeDef,
):
    pass

_RequiredListFraudstersRequestListFraudstersPaginateTypeDef = TypedDict(
    "_RequiredListFraudstersRequestListFraudstersPaginateTypeDef",
    {
        "DomainId": str,
    },
)
_OptionalListFraudstersRequestListFraudstersPaginateTypeDef = TypedDict(
    "_OptionalListFraudstersRequestListFraudstersPaginateTypeDef",
    {
        "WatchlistId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListFraudstersRequestListFraudstersPaginateTypeDef(
    _RequiredListFraudstersRequestListFraudstersPaginateTypeDef,
    _OptionalListFraudstersRequestListFraudstersPaginateTypeDef,
):
    pass

_RequiredListSpeakerEnrollmentJobsRequestListSpeakerEnrollmentJobsPaginateTypeDef = TypedDict(
    "_RequiredListSpeakerEnrollmentJobsRequestListSpeakerEnrollmentJobsPaginateTypeDef",
    {
        "DomainId": str,
    },
)
_OptionalListSpeakerEnrollmentJobsRequestListSpeakerEnrollmentJobsPaginateTypeDef = TypedDict(
    "_OptionalListSpeakerEnrollmentJobsRequestListSpeakerEnrollmentJobsPaginateTypeDef",
    {
        "JobStatus": SpeakerEnrollmentJobStatusType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListSpeakerEnrollmentJobsRequestListSpeakerEnrollmentJobsPaginateTypeDef(
    _RequiredListSpeakerEnrollmentJobsRequestListSpeakerEnrollmentJobsPaginateTypeDef,
    _OptionalListSpeakerEnrollmentJobsRequestListSpeakerEnrollmentJobsPaginateTypeDef,
):
    pass

_RequiredListSpeakersRequestListSpeakersPaginateTypeDef = TypedDict(
    "_RequiredListSpeakersRequestListSpeakersPaginateTypeDef",
    {
        "DomainId": str,
    },
)
_OptionalListSpeakersRequestListSpeakersPaginateTypeDef = TypedDict(
    "_OptionalListSpeakersRequestListSpeakersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListSpeakersRequestListSpeakersPaginateTypeDef(
    _RequiredListSpeakersRequestListSpeakersPaginateTypeDef,
    _OptionalListSpeakersRequestListSpeakersPaginateTypeDef,
):
    pass

_RequiredListWatchlistsRequestListWatchlistsPaginateTypeDef = TypedDict(
    "_RequiredListWatchlistsRequestListWatchlistsPaginateTypeDef",
    {
        "DomainId": str,
    },
)
_OptionalListWatchlistsRequestListWatchlistsPaginateTypeDef = TypedDict(
    "_OptionalListWatchlistsRequestListWatchlistsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListWatchlistsRequestListWatchlistsPaginateTypeDef(
    _RequiredListWatchlistsRequestListWatchlistsPaginateTypeDef,
    _OptionalListWatchlistsRequestListWatchlistsPaginateTypeDef,
):
    pass

ListSpeakersResponseTypeDef = TypedDict(
    "ListSpeakersResponseTypeDef",
    {
        "NextToken": str,
        "SpeakerSummaries": List[SpeakerSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListWatchlistsResponseTypeDef = TypedDict(
    "ListWatchlistsResponseTypeDef",
    {
        "NextToken": str,
        "WatchlistSummaries": List[WatchlistSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDomainsResponseTypeDef = TypedDict(
    "ListDomainsResponseTypeDef",
    {
        "DomainSummaries": List[DomainSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDomainResponseTypeDef = TypedDict(
    "CreateDomainResponseTypeDef",
    {
        "Domain": DomainTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDomainResponseTypeDef = TypedDict(
    "DescribeDomainResponseTypeDef",
    {
        "Domain": DomainTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDomainResponseTypeDef = TypedDict(
    "UpdateDomainResponseTypeDef",
    {
        "Domain": DomainTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SpeakerEnrollmentJobTypeDef = TypedDict(
    "SpeakerEnrollmentJobTypeDef",
    {
        "CreatedAt": datetime,
        "DataAccessRoleArn": str,
        "DomainId": str,
        "EndedAt": datetime,
        "EnrollmentConfig": EnrollmentConfigTypeDef,
        "FailureDetails": FailureDetailsTypeDef,
        "InputDataConfig": InputDataConfigTypeDef,
        "JobId": str,
        "JobName": str,
        "JobProgress": JobProgressTypeDef,
        "JobStatus": SpeakerEnrollmentJobStatusType,
        "OutputDataConfig": OutputDataConfigTypeDef,
    },
    total=False,
)

_RequiredStartSpeakerEnrollmentJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartSpeakerEnrollmentJobRequestRequestTypeDef",
    {
        "DataAccessRoleArn": str,
        "DomainId": str,
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
    },
)
_OptionalStartSpeakerEnrollmentJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartSpeakerEnrollmentJobRequestRequestTypeDef",
    {
        "ClientToken": str,
        "EnrollmentConfig": EnrollmentConfigTypeDef,
        "JobName": str,
    },
    total=False,
)

class StartSpeakerEnrollmentJobRequestRequestTypeDef(
    _RequiredStartSpeakerEnrollmentJobRequestRequestTypeDef,
    _OptionalStartSpeakerEnrollmentJobRequestRequestTypeDef,
):
    pass

FraudDetectionResultTypeDef = TypedDict(
    "FraudDetectionResultTypeDef",
    {
        "AudioAggregationEndedAt": datetime,
        "AudioAggregationStartedAt": datetime,
        "Configuration": FraudDetectionConfigurationTypeDef,
        "Decision": FraudDetectionDecisionType,
        "FraudDetectionResultId": str,
        "Reasons": List[FraudDetectionReasonType],
        "RiskDetails": FraudRiskDetailsTypeDef,
    },
    total=False,
)

ListFraudsterRegistrationJobsResponseTypeDef = TypedDict(
    "ListFraudsterRegistrationJobsResponseTypeDef",
    {
        "JobSummaries": List[FraudsterRegistrationJobSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSpeakerEnrollmentJobsResponseTypeDef = TypedDict(
    "ListSpeakerEnrollmentJobsResponseTypeDef",
    {
        "JobSummaries": List[SpeakerEnrollmentJobSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFraudsterRegistrationJobResponseTypeDef = TypedDict(
    "DescribeFraudsterRegistrationJobResponseTypeDef",
    {
        "Job": FraudsterRegistrationJobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartFraudsterRegistrationJobResponseTypeDef = TypedDict(
    "StartFraudsterRegistrationJobResponseTypeDef",
    {
        "Job": FraudsterRegistrationJobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSpeakerEnrollmentJobResponseTypeDef = TypedDict(
    "DescribeSpeakerEnrollmentJobResponseTypeDef",
    {
        "Job": SpeakerEnrollmentJobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartSpeakerEnrollmentJobResponseTypeDef = TypedDict(
    "StartSpeakerEnrollmentJobResponseTypeDef",
    {
        "Job": SpeakerEnrollmentJobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EvaluateSessionResponseTypeDef = TypedDict(
    "EvaluateSessionResponseTypeDef",
    {
        "AuthenticationResult": AuthenticationResultTypeDef,
        "DomainId": str,
        "FraudDetectionResult": FraudDetectionResultTypeDef,
        "SessionId": str,
        "SessionName": str,
        "StreamingStatus": StreamingStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
