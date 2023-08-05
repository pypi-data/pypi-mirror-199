"""
Type annotations for chime-sdk-voice service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_chime_sdk_voice.client import ChimeSDKVoiceClient

    session = Session()
    client: ChimeSDKVoiceClient = session.client("chime-sdk-voice")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    CapabilityType,
    GeoMatchLevelType,
    NumberSelectionBehaviorType,
    PhoneNumberAssociationNameType,
    PhoneNumberProductTypeType,
    PhoneNumberTypeType,
    ProxySessionStatusType,
    SipRuleTriggerTypeType,
    VoiceConnectorAwsRegionType,
)
from .paginator import ListSipMediaApplicationsPaginator, ListSipRulesPaginator
from .type_defs import (
    AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef,
    AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef,
    BatchDeletePhoneNumberResponseTypeDef,
    BatchUpdatePhoneNumberResponseTypeDef,
    CreatePhoneNumberOrderResponseTypeDef,
    CreateProxySessionResponseTypeDef,
    CreateSipMediaApplicationCallResponseTypeDef,
    CreateSipMediaApplicationResponseTypeDef,
    CreateSipRuleResponseTypeDef,
    CreateVoiceConnectorGroupResponseTypeDef,
    CreateVoiceConnectorResponseTypeDef,
    CreateVoiceProfileDomainResponseTypeDef,
    CreateVoiceProfileResponseTypeDef,
    CredentialTypeDef,
    DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef,
    DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef,
    EmergencyCallingConfigurationTypeDef,
    EmptyResponseMetadataTypeDef,
    GeoMatchParamsTypeDef,
    GetGlobalSettingsResponseTypeDef,
    GetPhoneNumberOrderResponseTypeDef,
    GetPhoneNumberResponseTypeDef,
    GetPhoneNumberSettingsResponseTypeDef,
    GetProxySessionResponseTypeDef,
    GetSipMediaApplicationAlexaSkillConfigurationResponseTypeDef,
    GetSipMediaApplicationLoggingConfigurationResponseTypeDef,
    GetSipMediaApplicationResponseTypeDef,
    GetSipRuleResponseTypeDef,
    GetSpeakerSearchTaskResponseTypeDef,
    GetVoiceConnectorEmergencyCallingConfigurationResponseTypeDef,
    GetVoiceConnectorGroupResponseTypeDef,
    GetVoiceConnectorLoggingConfigurationResponseTypeDef,
    GetVoiceConnectorOriginationResponseTypeDef,
    GetVoiceConnectorProxyResponseTypeDef,
    GetVoiceConnectorResponseTypeDef,
    GetVoiceConnectorStreamingConfigurationResponseTypeDef,
    GetVoiceConnectorTerminationHealthResponseTypeDef,
    GetVoiceConnectorTerminationResponseTypeDef,
    GetVoiceProfileDomainResponseTypeDef,
    GetVoiceProfileResponseTypeDef,
    GetVoiceToneAnalysisTaskResponseTypeDef,
    ListAvailableVoiceConnectorRegionsResponseTypeDef,
    ListPhoneNumberOrdersResponseTypeDef,
    ListPhoneNumbersResponseTypeDef,
    ListProxySessionsResponseTypeDef,
    ListSipMediaApplicationsResponseTypeDef,
    ListSipRulesResponseTypeDef,
    ListSupportedPhoneNumberCountriesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListVoiceConnectorGroupsResponseTypeDef,
    ListVoiceConnectorsResponseTypeDef,
    ListVoiceConnectorTerminationCredentialsResponseTypeDef,
    ListVoiceProfileDomainsResponseTypeDef,
    ListVoiceProfilesResponseTypeDef,
    LoggingConfigurationTypeDef,
    OriginationTypeDef,
    PutSipMediaApplicationAlexaSkillConfigurationResponseTypeDef,
    PutSipMediaApplicationLoggingConfigurationResponseTypeDef,
    PutVoiceConnectorEmergencyCallingConfigurationResponseTypeDef,
    PutVoiceConnectorLoggingConfigurationResponseTypeDef,
    PutVoiceConnectorOriginationResponseTypeDef,
    PutVoiceConnectorProxyResponseTypeDef,
    PutVoiceConnectorStreamingConfigurationResponseTypeDef,
    PutVoiceConnectorTerminationResponseTypeDef,
    RestorePhoneNumberResponseTypeDef,
    SearchAvailablePhoneNumbersResponseTypeDef,
    ServerSideEncryptionConfigurationTypeDef,
    SipMediaApplicationAlexaSkillConfigurationTypeDef,
    SipMediaApplicationEndpointTypeDef,
    SipMediaApplicationLoggingConfigurationTypeDef,
    SipRuleTargetApplicationTypeDef,
    StartSpeakerSearchTaskResponseTypeDef,
    StartVoiceToneAnalysisTaskResponseTypeDef,
    StreamingConfigurationTypeDef,
    TagTypeDef,
    TerminationTypeDef,
    UpdatePhoneNumberRequestItemTypeDef,
    UpdatePhoneNumberResponseTypeDef,
    UpdateProxySessionResponseTypeDef,
    UpdateSipMediaApplicationCallResponseTypeDef,
    UpdateSipMediaApplicationResponseTypeDef,
    UpdateSipRuleResponseTypeDef,
    UpdateVoiceConnectorGroupResponseTypeDef,
    UpdateVoiceConnectorResponseTypeDef,
    UpdateVoiceProfileDomainResponseTypeDef,
    UpdateVoiceProfileResponseTypeDef,
    ValidateE911AddressResponseTypeDef,
    VoiceConnectorItemTypeDef,
    VoiceConnectorSettingsTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ChimeSDKVoiceClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    GoneException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ServiceFailureException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottledClientException: Type[BotocoreClientError]
    UnauthorizedClientException: Type[BotocoreClientError]
    UnprocessableEntityException: Type[BotocoreClientError]


class ChimeSDKVoiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ChimeSDKVoiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#exceptions)
        """

    def associate_phone_numbers_with_voice_connector(
        self, *, VoiceConnectorId: str, E164PhoneNumbers: Sequence[str], ForceAssociate: bool = ...
    ) -> AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/AssociatePhoneNumbersWithVoiceConnector).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.associate_phone_numbers_with_voice_connector)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#associate_phone_numbers_with_voice_connector)
        """

    def associate_phone_numbers_with_voice_connector_group(
        self,
        *,
        VoiceConnectorGroupId: str,
        E164PhoneNumbers: Sequence[str],
        ForceAssociate: bool = ...
    ) -> AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/AssociatePhoneNumbersWithVoiceConnectorGroup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.associate_phone_numbers_with_voice_connector_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#associate_phone_numbers_with_voice_connector_group)
        """

    def batch_delete_phone_number(
        self, *, PhoneNumberIds: Sequence[str]
    ) -> BatchDeletePhoneNumberResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/BatchDeletePhoneNumber).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.batch_delete_phone_number)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#batch_delete_phone_number)
        """

    def batch_update_phone_number(
        self, *, UpdatePhoneNumberRequestItems: Sequence[UpdatePhoneNumberRequestItemTypeDef]
    ) -> BatchUpdatePhoneNumberResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/BatchUpdatePhoneNumber).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.batch_update_phone_number)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#batch_update_phone_number)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#close)
        """

    def create_phone_number_order(
        self, *, ProductType: PhoneNumberProductTypeType, E164PhoneNumbers: Sequence[str]
    ) -> CreatePhoneNumberOrderResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/CreatePhoneNumberOrder).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.create_phone_number_order)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#create_phone_number_order)
        """

    def create_proxy_session(
        self,
        *,
        VoiceConnectorId: str,
        ParticipantPhoneNumbers: Sequence[str],
        Capabilities: Sequence[CapabilityType],
        Name: str = ...,
        ExpiryMinutes: int = ...,
        NumberSelectionBehavior: NumberSelectionBehaviorType = ...,
        GeoMatchLevel: GeoMatchLevelType = ...,
        GeoMatchParams: GeoMatchParamsTypeDef = ...
    ) -> CreateProxySessionResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/CreateProxySession).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.create_proxy_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#create_proxy_session)
        """

    def create_sip_media_application(
        self, *, AwsRegion: str, Name: str, Endpoints: Sequence[SipMediaApplicationEndpointTypeDef]
    ) -> CreateSipMediaApplicationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/CreateSipMediaApplication).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.create_sip_media_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#create_sip_media_application)
        """

    def create_sip_media_application_call(
        self,
        *,
        FromPhoneNumber: str,
        ToPhoneNumber: str,
        SipMediaApplicationId: str,
        SipHeaders: Mapping[str, str] = ...,
        ArgumentsMap: Mapping[str, str] = ...
    ) -> CreateSipMediaApplicationCallResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/CreateSipMediaApplicationCall).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.create_sip_media_application_call)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#create_sip_media_application_call)
        """

    def create_sip_rule(
        self,
        *,
        Name: str,
        TriggerType: SipRuleTriggerTypeType,
        TriggerValue: str,
        Disabled: bool = ...,
        TargetApplications: Sequence[SipRuleTargetApplicationTypeDef] = ...
    ) -> CreateSipRuleResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/CreateSipRule).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.create_sip_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#create_sip_rule)
        """

    def create_voice_connector(
        self, *, Name: str, RequireEncryption: bool, AwsRegion: VoiceConnectorAwsRegionType = ...
    ) -> CreateVoiceConnectorResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/CreateVoiceConnector).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.create_voice_connector)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#create_voice_connector)
        """

    def create_voice_connector_group(
        self, *, Name: str, VoiceConnectorItems: Sequence[VoiceConnectorItemTypeDef] = ...
    ) -> CreateVoiceConnectorGroupResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/CreateVoiceConnectorGroup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.create_voice_connector_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#create_voice_connector_group)
        """

    def create_voice_profile(
        self, *, SpeakerSearchTaskId: str
    ) -> CreateVoiceProfileResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/CreateVoiceProfile).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.create_voice_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#create_voice_profile)
        """

    def create_voice_profile_domain(
        self,
        *,
        Name: str,
        ServerSideEncryptionConfiguration: ServerSideEncryptionConfigurationTypeDef,
        Description: str = ...,
        ClientRequestToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreateVoiceProfileDomainResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/CreateVoiceProfileDomain).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.create_voice_profile_domain)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#create_voice_profile_domain)
        """

    def delete_phone_number(self, *, PhoneNumberId: str) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeletePhoneNumber).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_phone_number)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#delete_phone_number)
        """

    def delete_proxy_session(
        self, *, VoiceConnectorId: str, ProxySessionId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteProxySession).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_proxy_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#delete_proxy_session)
        """

    def delete_sip_media_application(
        self, *, SipMediaApplicationId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteSipMediaApplication).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_sip_media_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#delete_sip_media_application)
        """

    def delete_sip_rule(self, *, SipRuleId: str) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteSipRule).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_sip_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#delete_sip_rule)
        """

    def delete_voice_connector(self, *, VoiceConnectorId: str) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteVoiceConnector).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_voice_connector)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#delete_voice_connector)
        """

    def delete_voice_connector_emergency_calling_configuration(
        self, *, VoiceConnectorId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteVoiceConnectorEmergencyCallingConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_voice_connector_emergency_calling_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#delete_voice_connector_emergency_calling_configuration)
        """

    def delete_voice_connector_group(
        self, *, VoiceConnectorGroupId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteVoiceConnectorGroup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_voice_connector_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#delete_voice_connector_group)
        """

    def delete_voice_connector_origination(
        self, *, VoiceConnectorId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteVoiceConnectorOrigination).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_voice_connector_origination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#delete_voice_connector_origination)
        """

    def delete_voice_connector_proxy(
        self, *, VoiceConnectorId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteVoiceConnectorProxy).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_voice_connector_proxy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#delete_voice_connector_proxy)
        """

    def delete_voice_connector_streaming_configuration(
        self, *, VoiceConnectorId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteVoiceConnectorStreamingConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_voice_connector_streaming_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#delete_voice_connector_streaming_configuration)
        """

    def delete_voice_connector_termination(
        self, *, VoiceConnectorId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteVoiceConnectorTermination).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_voice_connector_termination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#delete_voice_connector_termination)
        """

    def delete_voice_connector_termination_credentials(
        self, *, VoiceConnectorId: str, Usernames: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteVoiceConnectorTerminationCredentials).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_voice_connector_termination_credentials)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#delete_voice_connector_termination_credentials)
        """

    def delete_voice_profile(self, *, VoiceProfileId: str) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteVoiceProfile).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_voice_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#delete_voice_profile)
        """

    def delete_voice_profile_domain(
        self, *, VoiceProfileDomainId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DeleteVoiceProfileDomain).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.delete_voice_profile_domain)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#delete_voice_profile_domain)
        """

    def disassociate_phone_numbers_from_voice_connector(
        self, *, VoiceConnectorId: str, E164PhoneNumbers: Sequence[str]
    ) -> DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DisassociatePhoneNumbersFromVoiceConnector).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.disassociate_phone_numbers_from_voice_connector)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#disassociate_phone_numbers_from_voice_connector)
        """

    def disassociate_phone_numbers_from_voice_connector_group(
        self, *, VoiceConnectorGroupId: str, E164PhoneNumbers: Sequence[str]
    ) -> DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/DisassociatePhoneNumbersFromVoiceConnectorGroup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.disassociate_phone_numbers_from_voice_connector_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#disassociate_phone_numbers_from_voice_connector_group)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#generate_presigned_url)
        """

    def get_global_settings(self) -> GetGlobalSettingsResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetGlobalSettings).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_global_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_global_settings)
        """

    def get_phone_number(self, *, PhoneNumberId: str) -> GetPhoneNumberResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetPhoneNumber).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_phone_number)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_phone_number)
        """

    def get_phone_number_order(
        self, *, PhoneNumberOrderId: str
    ) -> GetPhoneNumberOrderResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetPhoneNumberOrder).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_phone_number_order)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_phone_number_order)
        """

    def get_phone_number_settings(self) -> GetPhoneNumberSettingsResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetPhoneNumberSettings).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_phone_number_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_phone_number_settings)
        """

    def get_proxy_session(
        self, *, VoiceConnectorId: str, ProxySessionId: str
    ) -> GetProxySessionResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetProxySession).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_proxy_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_proxy_session)
        """

    def get_sip_media_application(
        self, *, SipMediaApplicationId: str
    ) -> GetSipMediaApplicationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetSipMediaApplication).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_sip_media_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_sip_media_application)
        """

    def get_sip_media_application_alexa_skill_configuration(
        self, *, SipMediaApplicationId: str
    ) -> GetSipMediaApplicationAlexaSkillConfigurationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetSipMediaApplicationAlexaSkillConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_sip_media_application_alexa_skill_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_sip_media_application_alexa_skill_configuration)
        """

    def get_sip_media_application_logging_configuration(
        self, *, SipMediaApplicationId: str
    ) -> GetSipMediaApplicationLoggingConfigurationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetSipMediaApplicationLoggingConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_sip_media_application_logging_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_sip_media_application_logging_configuration)
        """

    def get_sip_rule(self, *, SipRuleId: str) -> GetSipRuleResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetSipRule).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_sip_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_sip_rule)
        """

    def get_speaker_search_task(
        self, *, VoiceConnectorId: str, SpeakerSearchTaskId: str
    ) -> GetSpeakerSearchTaskResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetSpeakerSearchTask).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_speaker_search_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_speaker_search_task)
        """

    def get_voice_connector(self, *, VoiceConnectorId: str) -> GetVoiceConnectorResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceConnector).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_connector)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_voice_connector)
        """

    def get_voice_connector_emergency_calling_configuration(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorEmergencyCallingConfigurationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceConnectorEmergencyCallingConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_connector_emergency_calling_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_voice_connector_emergency_calling_configuration)
        """

    def get_voice_connector_group(
        self, *, VoiceConnectorGroupId: str
    ) -> GetVoiceConnectorGroupResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceConnectorGroup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_connector_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_voice_connector_group)
        """

    def get_voice_connector_logging_configuration(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorLoggingConfigurationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceConnectorLoggingConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_connector_logging_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_voice_connector_logging_configuration)
        """

    def get_voice_connector_origination(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorOriginationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceConnectorOrigination).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_connector_origination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_voice_connector_origination)
        """

    def get_voice_connector_proxy(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorProxyResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceConnectorProxy).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_connector_proxy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_voice_connector_proxy)
        """

    def get_voice_connector_streaming_configuration(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorStreamingConfigurationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceConnectorStreamingConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_connector_streaming_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_voice_connector_streaming_configuration)
        """

    def get_voice_connector_termination(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorTerminationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceConnectorTermination).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_connector_termination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_voice_connector_termination)
        """

    def get_voice_connector_termination_health(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorTerminationHealthResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceConnectorTerminationHealth).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_connector_termination_health)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_voice_connector_termination_health)
        """

    def get_voice_profile(self, *, VoiceProfileId: str) -> GetVoiceProfileResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceProfile).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_voice_profile)
        """

    def get_voice_profile_domain(
        self, *, VoiceProfileDomainId: str
    ) -> GetVoiceProfileDomainResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceProfileDomain).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_profile_domain)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_voice_profile_domain)
        """

    def get_voice_tone_analysis_task(
        self, *, VoiceConnectorId: str, VoiceToneAnalysisTaskId: str, IsCaller: bool
    ) -> GetVoiceToneAnalysisTaskResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/GetVoiceToneAnalysisTask).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_voice_tone_analysis_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_voice_tone_analysis_task)
        """

    def list_available_voice_connector_regions(
        self,
    ) -> ListAvailableVoiceConnectorRegionsResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListAvailableVoiceConnectorRegions).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_available_voice_connector_regions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#list_available_voice_connector_regions)
        """

    def list_phone_number_orders(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListPhoneNumberOrdersResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListPhoneNumberOrders).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_phone_number_orders)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#list_phone_number_orders)
        """

    def list_phone_numbers(
        self,
        *,
        Status: str = ...,
        ProductType: PhoneNumberProductTypeType = ...,
        FilterName: PhoneNumberAssociationNameType = ...,
        FilterValue: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListPhoneNumbersResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListPhoneNumbers).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_phone_numbers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#list_phone_numbers)
        """

    def list_proxy_sessions(
        self,
        *,
        VoiceConnectorId: str,
        Status: ProxySessionStatusType = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListProxySessionsResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListProxySessions).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_proxy_sessions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#list_proxy_sessions)
        """

    def list_sip_media_applications(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListSipMediaApplicationsResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListSipMediaApplications).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_sip_media_applications)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#list_sip_media_applications)
        """

    def list_sip_rules(
        self, *, SipMediaApplicationId: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> ListSipRulesResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListSipRules).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_sip_rules)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#list_sip_rules)
        """

    def list_supported_phone_number_countries(
        self, *, ProductType: PhoneNumberProductTypeType
    ) -> ListSupportedPhoneNumberCountriesResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListSupportedPhoneNumberCountries).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_supported_phone_number_countries)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#list_supported_phone_number_countries)
        """

    def list_tags_for_resource(self, *, ResourceARN: str) -> ListTagsForResourceResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListTagsForResource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#list_tags_for_resource)
        """

    def list_voice_connector_groups(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListVoiceConnectorGroupsResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListVoiceConnectorGroups).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_voice_connector_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#list_voice_connector_groups)
        """

    def list_voice_connector_termination_credentials(
        self, *, VoiceConnectorId: str
    ) -> ListVoiceConnectorTerminationCredentialsResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListVoiceConnectorTerminationCredentials).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_voice_connector_termination_credentials)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#list_voice_connector_termination_credentials)
        """

    def list_voice_connectors(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListVoiceConnectorsResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListVoiceConnectors).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_voice_connectors)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#list_voice_connectors)
        """

    def list_voice_profile_domains(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListVoiceProfileDomainsResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListVoiceProfileDomains).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_voice_profile_domains)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#list_voice_profile_domains)
        """

    def list_voice_profiles(
        self, *, VoiceProfileDomainId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListVoiceProfilesResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ListVoiceProfiles).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.list_voice_profiles)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#list_voice_profiles)
        """

    def put_sip_media_application_alexa_skill_configuration(
        self,
        *,
        SipMediaApplicationId: str,
        SipMediaApplicationAlexaSkillConfiguration: SipMediaApplicationAlexaSkillConfigurationTypeDef = ...
    ) -> PutSipMediaApplicationAlexaSkillConfigurationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/PutSipMediaApplicationAlexaSkillConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.put_sip_media_application_alexa_skill_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#put_sip_media_application_alexa_skill_configuration)
        """

    def put_sip_media_application_logging_configuration(
        self,
        *,
        SipMediaApplicationId: str,
        SipMediaApplicationLoggingConfiguration: SipMediaApplicationLoggingConfigurationTypeDef = ...
    ) -> PutSipMediaApplicationLoggingConfigurationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/PutSipMediaApplicationLoggingConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.put_sip_media_application_logging_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#put_sip_media_application_logging_configuration)
        """

    def put_voice_connector_emergency_calling_configuration(
        self,
        *,
        VoiceConnectorId: str,
        EmergencyCallingConfiguration: EmergencyCallingConfigurationTypeDef
    ) -> PutVoiceConnectorEmergencyCallingConfigurationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/PutVoiceConnectorEmergencyCallingConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.put_voice_connector_emergency_calling_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#put_voice_connector_emergency_calling_configuration)
        """

    def put_voice_connector_logging_configuration(
        self, *, VoiceConnectorId: str, LoggingConfiguration: LoggingConfigurationTypeDef
    ) -> PutVoiceConnectorLoggingConfigurationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/PutVoiceConnectorLoggingConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.put_voice_connector_logging_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#put_voice_connector_logging_configuration)
        """

    def put_voice_connector_origination(
        self, *, VoiceConnectorId: str, Origination: OriginationTypeDef
    ) -> PutVoiceConnectorOriginationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/PutVoiceConnectorOrigination).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.put_voice_connector_origination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#put_voice_connector_origination)
        """

    def put_voice_connector_proxy(
        self,
        *,
        VoiceConnectorId: str,
        DefaultSessionExpiryMinutes: int,
        PhoneNumberPoolCountries: Sequence[str],
        FallBackPhoneNumber: str = ...,
        Disabled: bool = ...
    ) -> PutVoiceConnectorProxyResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/PutVoiceConnectorProxy).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.put_voice_connector_proxy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#put_voice_connector_proxy)
        """

    def put_voice_connector_streaming_configuration(
        self, *, VoiceConnectorId: str, StreamingConfiguration: StreamingConfigurationTypeDef
    ) -> PutVoiceConnectorStreamingConfigurationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/PutVoiceConnectorStreamingConfiguration).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.put_voice_connector_streaming_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#put_voice_connector_streaming_configuration)
        """

    def put_voice_connector_termination(
        self, *, VoiceConnectorId: str, Termination: TerminationTypeDef
    ) -> PutVoiceConnectorTerminationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/PutVoiceConnectorTermination).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.put_voice_connector_termination)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#put_voice_connector_termination)
        """

    def put_voice_connector_termination_credentials(
        self, *, VoiceConnectorId: str, Credentials: Sequence[CredentialTypeDef] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/PutVoiceConnectorTerminationCredentials).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.put_voice_connector_termination_credentials)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#put_voice_connector_termination_credentials)
        """

    def restore_phone_number(self, *, PhoneNumberId: str) -> RestorePhoneNumberResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/RestorePhoneNumber).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.restore_phone_number)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#restore_phone_number)
        """

    def search_available_phone_numbers(
        self,
        *,
        AreaCode: str = ...,
        City: str = ...,
        Country: str = ...,
        State: str = ...,
        TollFreePrefix: str = ...,
        PhoneNumberType: PhoneNumberTypeType = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> SearchAvailablePhoneNumbersResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/SearchAvailablePhoneNumbers).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.search_available_phone_numbers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#search_available_phone_numbers)
        """

    def start_speaker_search_task(
        self,
        *,
        VoiceConnectorId: str,
        TransactionId: str,
        VoiceProfileDomainId: str,
        ClientRequestToken: str = ...
    ) -> StartSpeakerSearchTaskResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/StartSpeakerSearchTask).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.start_speaker_search_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#start_speaker_search_task)
        """

    def start_voice_tone_analysis_task(
        self,
        *,
        VoiceConnectorId: str,
        TransactionId: str,
        LanguageCode: Literal["en-US"],
        ClientRequestToken: str = ...
    ) -> StartVoiceToneAnalysisTaskResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/StartVoiceToneAnalysisTask).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.start_voice_tone_analysis_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#start_voice_tone_analysis_task)
        """

    def stop_speaker_search_task(
        self, *, VoiceConnectorId: str, SpeakerSearchTaskId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/StopSpeakerSearchTask).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.stop_speaker_search_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#stop_speaker_search_task)
        """

    def stop_voice_tone_analysis_task(
        self, *, VoiceConnectorId: str, VoiceToneAnalysisTaskId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/StopVoiceToneAnalysisTask).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.stop_voice_tone_analysis_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#stop_voice_tone_analysis_task)
        """

    def tag_resource(
        self, *, ResourceARN: str, Tags: Sequence[TagTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/TagResource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#tag_resource)
        """

    def untag_resource(
        self, *, ResourceARN: str, TagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UntagResource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#untag_resource)
        """

    def update_global_settings(
        self, *, VoiceConnector: VoiceConnectorSettingsTypeDef = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UpdateGlobalSettings).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.update_global_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#update_global_settings)
        """

    def update_phone_number(
        self,
        *,
        PhoneNumberId: str,
        ProductType: PhoneNumberProductTypeType = ...,
        CallingName: str = ...
    ) -> UpdatePhoneNumberResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UpdatePhoneNumber).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.update_phone_number)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#update_phone_number)
        """

    def update_phone_number_settings(self, *, CallingName: str) -> EmptyResponseMetadataTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UpdatePhoneNumberSettings).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.update_phone_number_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#update_phone_number_settings)
        """

    def update_proxy_session(
        self,
        *,
        VoiceConnectorId: str,
        ProxySessionId: str,
        Capabilities: Sequence[CapabilityType],
        ExpiryMinutes: int = ...
    ) -> UpdateProxySessionResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UpdateProxySession).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.update_proxy_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#update_proxy_session)
        """

    def update_sip_media_application(
        self,
        *,
        SipMediaApplicationId: str,
        Name: str = ...,
        Endpoints: Sequence[SipMediaApplicationEndpointTypeDef] = ...
    ) -> UpdateSipMediaApplicationResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UpdateSipMediaApplication).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.update_sip_media_application)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#update_sip_media_application)
        """

    def update_sip_media_application_call(
        self, *, SipMediaApplicationId: str, TransactionId: str, Arguments: Mapping[str, str]
    ) -> UpdateSipMediaApplicationCallResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UpdateSipMediaApplicationCall).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.update_sip_media_application_call)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#update_sip_media_application_call)
        """

    def update_sip_rule(
        self,
        *,
        SipRuleId: str,
        Name: str,
        Disabled: bool = ...,
        TargetApplications: Sequence[SipRuleTargetApplicationTypeDef] = ...
    ) -> UpdateSipRuleResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UpdateSipRule).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.update_sip_rule)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#update_sip_rule)
        """

    def update_voice_connector(
        self, *, VoiceConnectorId: str, Name: str, RequireEncryption: bool
    ) -> UpdateVoiceConnectorResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UpdateVoiceConnector).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.update_voice_connector)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#update_voice_connector)
        """

    def update_voice_connector_group(
        self,
        *,
        VoiceConnectorGroupId: str,
        Name: str,
        VoiceConnectorItems: Sequence[VoiceConnectorItemTypeDef]
    ) -> UpdateVoiceConnectorGroupResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UpdateVoiceConnectorGroup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.update_voice_connector_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#update_voice_connector_group)
        """

    def update_voice_profile(
        self, *, VoiceProfileId: str, SpeakerSearchTaskId: str
    ) -> UpdateVoiceProfileResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UpdateVoiceProfile).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.update_voice_profile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#update_voice_profile)
        """

    def update_voice_profile_domain(
        self, *, VoiceProfileDomainId: str, Name: str = ..., Description: str = ...
    ) -> UpdateVoiceProfileDomainResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/UpdateVoiceProfileDomain).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.update_voice_profile_domain)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#update_voice_profile_domain)
        """

    def validate_e911_address(
        self,
        *,
        AwsAccountId: str,
        StreetNumber: str,
        StreetInfo: str,
        City: str,
        State: str,
        Country: str,
        PostalCode: str
    ) -> ValidateE911AddressResponseTypeDef:
        """
        See also: [AWS API Documentation](https://docs.aws.amazon.com/goto/WebAPI/chime-
        sdk-voice-2022-08-03/ValidateE911Address).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.validate_e911_address)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#validate_e911_address)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_sip_media_applications"]
    ) -> ListSipMediaApplicationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_sip_rules"]) -> ListSipRulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice.html#ChimeSDKVoice.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_chime_sdk_voice/client/#get_paginator)
        """
