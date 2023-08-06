'''
# dynatrace-environment-syntheticlocation

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Dynatrace::Environment::SyntheticLocation` v1.2.0.

## Description

Manage a synthetic location (V1) in Dynatrace.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-dynatrace-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Dynatrace::Environment::SyntheticLocation \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Dynatrace-Environment-SyntheticLocation \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Dynatrace::Environment::SyntheticLocation`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fdynatrace-environment-syntheticlocation+v1.2.0).
* Issues related to `Dynatrace::Environment::SyntheticLocation` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-dynatrace-resource-providers).

## License

Distributed under the Apache-2.0 License.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import constructs as _constructs_77d1e7e8


class CfnSyntheticLocation(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticlocation.CfnSyntheticLocation",
):
    '''A CloudFormation ``Dynatrace::Environment::SyntheticLocation``.

    :cloudformationResource: Dynatrace::Environment::SyntheticLocation
    :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        city: builtins.str,
        country_code: builtins.str,
        latitude: jsii.Number,
        longitude: jsii.Number,
        name: builtins.str,
        region_code: builtins.str,
        auto_update_chromium: typing.Optional[builtins.bool] = None,
        availability_location_outage: typing.Optional[builtins.bool] = None,
        availability_node_outage: typing.Optional[builtins.bool] = None,
        availability_notifications_enabled: typing.Optional[builtins.bool] = None,
        location_node_outage_delay_in_minutes: typing.Optional[jsii.Number] = None,
        nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional["CfnSyntheticLocationPropsStatus"] = None,
        type: typing.Optional["CfnSyntheticLocationPropsType"] = None,
    ) -> None:
        '''Create a new ``Dynatrace::Environment::SyntheticLocation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param city: The city of the location.
        :param country_code: The country code of the location. Use the alpha-2 code of the ISO 3166-2 standard (https://dt-url.net/iso3166-2), (for example, AT for Austria or PL for Poland).
        :param latitude: The latitude of the location in DDD.dddd format.
        :param longitude: The latitude of the location in DDD.dddd format.
        :param name: The name of the location.
        :param region_code: The region code of the location. For the USA or Canada use ISO 3166-2 state codes (without US- or CA- prefix), for example, VA for Virginia or OR for Oregon. For the rest of the world use FIPS 10-4 codes (https://dt-url.net/fipscodes).
        :param auto_update_chromium: Auto upgrade of Chromium is enabled (true) or disabled (false).
        :param availability_location_outage: The alerting of location outage is enabled (true) or disabled (false).
        :param availability_node_outage: The alerting of node outage is enabled (true) or disabled (false). If enabled, the outage of any node in the location triggers an alert.
        :param availability_notifications_enabled: The notifications of location and node outage is enabled (true) or disabled (false).
        :param location_node_outage_delay_in_minutes: Alert if the location or node outage lasts longer than X minutes. Only applicable when availabilityLocationOutage or availabilityNodeOutage is set to true.
        :param nodes: A list of synthetic nodes belonging to the location.
        :param status: The status of the location:. ENABLED: The location is displayed as active in the UI. You can assign monitors to the location. DISABLED: The location is displayed as inactive in the UI. You can't assign monitors to the location. Monitors already assigned to the location will stay there and will be executed from the location. HIDDEN: The location is not displayed in the UI. You can't assign monitors to the location. You can only set location as HIDDEN when no monitor is assigned to it.
        :param type: Defines the actual set of fields depending on the value. See one of the following objects:. PUBLIC -> PublicSyntheticLocation PRIVATE -> PrivateSyntheticLocation CLUSTER -> PrivateSyntheticLocation
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76dbe5ad6abbff21ffa35ae1132e2e1d773db1fc8e133c98236ea20616c67c2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSyntheticLocationProps(
            city=city,
            country_code=country_code,
            latitude=latitude,
            longitude=longitude,
            name=name,
            region_code=region_code,
            auto_update_chromium=auto_update_chromium,
            availability_location_outage=availability_location_outage,
            availability_node_outage=availability_node_outage,
            availability_notifications_enabled=availability_notifications_enabled,
            location_node_outage_delay_in_minutes=location_node_outage_delay_in_minutes,
            nodes=nodes,
            status=status,
            type=type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrEntityId")
    def attr_entity_id(self) -> builtins.str:
        '''Attribute ``Dynatrace::Environment::SyntheticLocation.EntityId``.

        :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEntityId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnSyntheticLocationProps":
        '''Resource props.'''
        return typing.cast("CfnSyntheticLocationProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticlocation.CfnSyntheticLocationProps",
    jsii_struct_bases=[],
    name_mapping={
        "city": "city",
        "country_code": "countryCode",
        "latitude": "latitude",
        "longitude": "longitude",
        "name": "name",
        "region_code": "regionCode",
        "auto_update_chromium": "autoUpdateChromium",
        "availability_location_outage": "availabilityLocationOutage",
        "availability_node_outage": "availabilityNodeOutage",
        "availability_notifications_enabled": "availabilityNotificationsEnabled",
        "location_node_outage_delay_in_minutes": "locationNodeOutageDelayInMinutes",
        "nodes": "nodes",
        "status": "status",
        "type": "type",
    },
)
class CfnSyntheticLocationProps:
    def __init__(
        self,
        *,
        city: builtins.str,
        country_code: builtins.str,
        latitude: jsii.Number,
        longitude: jsii.Number,
        name: builtins.str,
        region_code: builtins.str,
        auto_update_chromium: typing.Optional[builtins.bool] = None,
        availability_location_outage: typing.Optional[builtins.bool] = None,
        availability_node_outage: typing.Optional[builtins.bool] = None,
        availability_notifications_enabled: typing.Optional[builtins.bool] = None,
        location_node_outage_delay_in_minutes: typing.Optional[jsii.Number] = None,
        nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional["CfnSyntheticLocationPropsStatus"] = None,
        type: typing.Optional["CfnSyntheticLocationPropsType"] = None,
    ) -> None:
        '''Manage a synthetic location (V1) in Dynatrace.

        :param city: The city of the location.
        :param country_code: The country code of the location. Use the alpha-2 code of the ISO 3166-2 standard (https://dt-url.net/iso3166-2), (for example, AT for Austria or PL for Poland).
        :param latitude: The latitude of the location in DDD.dddd format.
        :param longitude: The latitude of the location in DDD.dddd format.
        :param name: The name of the location.
        :param region_code: The region code of the location. For the USA or Canada use ISO 3166-2 state codes (without US- or CA- prefix), for example, VA for Virginia or OR for Oregon. For the rest of the world use FIPS 10-4 codes (https://dt-url.net/fipscodes).
        :param auto_update_chromium: Auto upgrade of Chromium is enabled (true) or disabled (false).
        :param availability_location_outage: The alerting of location outage is enabled (true) or disabled (false).
        :param availability_node_outage: The alerting of node outage is enabled (true) or disabled (false). If enabled, the outage of any node in the location triggers an alert.
        :param availability_notifications_enabled: The notifications of location and node outage is enabled (true) or disabled (false).
        :param location_node_outage_delay_in_minutes: Alert if the location or node outage lasts longer than X minutes. Only applicable when availabilityLocationOutage or availabilityNodeOutage is set to true.
        :param nodes: A list of synthetic nodes belonging to the location.
        :param status: The status of the location:. ENABLED: The location is displayed as active in the UI. You can assign monitors to the location. DISABLED: The location is displayed as inactive in the UI. You can't assign monitors to the location. Monitors already assigned to the location will stay there and will be executed from the location. HIDDEN: The location is not displayed in the UI. You can't assign monitors to the location. You can only set location as HIDDEN when no monitor is assigned to it.
        :param type: Defines the actual set of fields depending on the value. See one of the following objects:. PUBLIC -> PublicSyntheticLocation PRIVATE -> PrivateSyntheticLocation CLUSTER -> PrivateSyntheticLocation

        :schema: CfnSyntheticLocationProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ba7db32b8b7797141fca97d4b1dec4aa70a5c2874870454b7a6a1461b0709a1)
            check_type(argname="argument city", value=city, expected_type=type_hints["city"])
            check_type(argname="argument country_code", value=country_code, expected_type=type_hints["country_code"])
            check_type(argname="argument latitude", value=latitude, expected_type=type_hints["latitude"])
            check_type(argname="argument longitude", value=longitude, expected_type=type_hints["longitude"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region_code", value=region_code, expected_type=type_hints["region_code"])
            check_type(argname="argument auto_update_chromium", value=auto_update_chromium, expected_type=type_hints["auto_update_chromium"])
            check_type(argname="argument availability_location_outage", value=availability_location_outage, expected_type=type_hints["availability_location_outage"])
            check_type(argname="argument availability_node_outage", value=availability_node_outage, expected_type=type_hints["availability_node_outage"])
            check_type(argname="argument availability_notifications_enabled", value=availability_notifications_enabled, expected_type=type_hints["availability_notifications_enabled"])
            check_type(argname="argument location_node_outage_delay_in_minutes", value=location_node_outage_delay_in_minutes, expected_type=type_hints["location_node_outage_delay_in_minutes"])
            check_type(argname="argument nodes", value=nodes, expected_type=type_hints["nodes"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "city": city,
            "country_code": country_code,
            "latitude": latitude,
            "longitude": longitude,
            "name": name,
            "region_code": region_code,
        }
        if auto_update_chromium is not None:
            self._values["auto_update_chromium"] = auto_update_chromium
        if availability_location_outage is not None:
            self._values["availability_location_outage"] = availability_location_outage
        if availability_node_outage is not None:
            self._values["availability_node_outage"] = availability_node_outage
        if availability_notifications_enabled is not None:
            self._values["availability_notifications_enabled"] = availability_notifications_enabled
        if location_node_outage_delay_in_minutes is not None:
            self._values["location_node_outage_delay_in_minutes"] = location_node_outage_delay_in_minutes
        if nodes is not None:
            self._values["nodes"] = nodes
        if status is not None:
            self._values["status"] = status
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def city(self) -> builtins.str:
        '''The city of the location.

        :schema: CfnSyntheticLocationProps#City
        '''
        result = self._values.get("city")
        assert result is not None, "Required property 'city' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def country_code(self) -> builtins.str:
        '''The country code of the location.

        Use the alpha-2 code of the ISO 3166-2 standard (https://dt-url.net/iso3166-2), (for example, AT for Austria or PL for Poland).

        :schema: CfnSyntheticLocationProps#CountryCode
        '''
        result = self._values.get("country_code")
        assert result is not None, "Required property 'country_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def latitude(self) -> jsii.Number:
        '''The latitude of the location in DDD.dddd format.

        :schema: CfnSyntheticLocationProps#Latitude
        '''
        result = self._values.get("latitude")
        assert result is not None, "Required property 'latitude' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def longitude(self) -> jsii.Number:
        '''The latitude of the location in DDD.dddd format.

        :schema: CfnSyntheticLocationProps#Longitude
        '''
        result = self._values.get("longitude")
        assert result is not None, "Required property 'longitude' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the location.

        :schema: CfnSyntheticLocationProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region_code(self) -> builtins.str:
        '''The region code of the location.

        For the USA or Canada use ISO 3166-2 state codes (without US- or CA- prefix), for example, VA for Virginia or OR for Oregon.

        For the rest of the world use FIPS 10-4 codes (https://dt-url.net/fipscodes).

        :schema: CfnSyntheticLocationProps#RegionCode
        '''
        result = self._values.get("region_code")
        assert result is not None, "Required property 'region_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_update_chromium(self) -> typing.Optional[builtins.bool]:
        '''Auto upgrade of Chromium is enabled (true) or disabled (false).

        :schema: CfnSyntheticLocationProps#AutoUpdateChromium
        '''
        result = self._values.get("auto_update_chromium")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def availability_location_outage(self) -> typing.Optional[builtins.bool]:
        '''The alerting of location outage is enabled (true) or disabled (false).

        :schema: CfnSyntheticLocationProps#AvailabilityLocationOutage
        '''
        result = self._values.get("availability_location_outage")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def availability_node_outage(self) -> typing.Optional[builtins.bool]:
        '''The alerting of node outage is enabled (true) or disabled (false).

        If enabled, the outage of any node in the location triggers an alert.

        :schema: CfnSyntheticLocationProps#AvailabilityNodeOutage
        '''
        result = self._values.get("availability_node_outage")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def availability_notifications_enabled(self) -> typing.Optional[builtins.bool]:
        '''The notifications of location and node outage is enabled (true) or disabled (false).

        :schema: CfnSyntheticLocationProps#AvailabilityNotificationsEnabled
        '''
        result = self._values.get("availability_notifications_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def location_node_outage_delay_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''Alert if the location or node outage lasts longer than X minutes.

        Only applicable when availabilityLocationOutage or availabilityNodeOutage is set to true.

        :schema: CfnSyntheticLocationProps#LocationNodeOutageDelayInMinutes
        '''
        result = self._values.get("location_node_outage_delay_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nodes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of synthetic nodes belonging to the location.

        :schema: CfnSyntheticLocationProps#Nodes
        '''
        result = self._values.get("nodes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def status(self) -> typing.Optional["CfnSyntheticLocationPropsStatus"]:
        '''The status of the location:.

        ENABLED: The location is displayed as active in the UI. You can assign monitors to the location.
        DISABLED: The location is displayed as inactive in the UI. You can't assign monitors to the location. Monitors already assigned to the location will stay there and will be executed from the location.
        HIDDEN: The location is not displayed in the UI. You can't assign monitors to the location. You can only set location as HIDDEN when no monitor is assigned to it.

        :schema: CfnSyntheticLocationProps#Status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional["CfnSyntheticLocationPropsStatus"], result)

    @builtins.property
    def type(self) -> typing.Optional["CfnSyntheticLocationPropsType"]:
        '''Defines the actual set of fields depending on the value. See one of the following objects:.

        PUBLIC -> PublicSyntheticLocation
        PRIVATE -> PrivateSyntheticLocation
        CLUSTER -> PrivateSyntheticLocation

        :schema: CfnSyntheticLocationProps#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional["CfnSyntheticLocationPropsType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSyntheticLocationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticlocation.CfnSyntheticLocationPropsStatus"
)
class CfnSyntheticLocationPropsStatus(enum.Enum):
    '''The status of the location:.

    ENABLED: The location is displayed as active in the UI. You can assign monitors to the location.
    DISABLED: The location is displayed as inactive in the UI. You can't assign monitors to the location. Monitors already assigned to the location will stay there and will be executed from the location.
    HIDDEN: The location is not displayed in the UI. You can't assign monitors to the location. You can only set location as HIDDEN when no monitor is assigned to it.

    :schema: CfnSyntheticLocationPropsStatus
    '''

    ENABLED = "ENABLED"
    '''ENABLED.'''
    DISABLED = "DISABLED"
    '''DISABLED.'''
    HIDDEN = "HIDDEN"
    '''HIDDEN.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticlocation.CfnSyntheticLocationPropsType"
)
class CfnSyntheticLocationPropsType(enum.Enum):
    '''Defines the actual set of fields depending on the value. See one of the following objects:.

    PUBLIC -> PublicSyntheticLocation
    PRIVATE -> PrivateSyntheticLocation
    CLUSTER -> PrivateSyntheticLocation

    :schema: CfnSyntheticLocationPropsType
    '''

    PUBLIC = "PUBLIC"
    '''PUBLIC.'''
    PRIVATE = "PRIVATE"
    '''PRIVATE.'''
    CLUSTER = "CLUSTER"
    '''CLUSTER.'''


__all__ = [
    "CfnSyntheticLocation",
    "CfnSyntheticLocationProps",
    "CfnSyntheticLocationPropsStatus",
    "CfnSyntheticLocationPropsType",
]

publication.publish()

def _typecheckingstub__d76dbe5ad6abbff21ffa35ae1132e2e1d773db1fc8e133c98236ea20616c67c2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    city: builtins.str,
    country_code: builtins.str,
    latitude: jsii.Number,
    longitude: jsii.Number,
    name: builtins.str,
    region_code: builtins.str,
    auto_update_chromium: typing.Optional[builtins.bool] = None,
    availability_location_outage: typing.Optional[builtins.bool] = None,
    availability_node_outage: typing.Optional[builtins.bool] = None,
    availability_notifications_enabled: typing.Optional[builtins.bool] = None,
    location_node_outage_delay_in_minutes: typing.Optional[jsii.Number] = None,
    nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[CfnSyntheticLocationPropsStatus] = None,
    type: typing.Optional[CfnSyntheticLocationPropsType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba7db32b8b7797141fca97d4b1dec4aa70a5c2874870454b7a6a1461b0709a1(
    *,
    city: builtins.str,
    country_code: builtins.str,
    latitude: jsii.Number,
    longitude: jsii.Number,
    name: builtins.str,
    region_code: builtins.str,
    auto_update_chromium: typing.Optional[builtins.bool] = None,
    availability_location_outage: typing.Optional[builtins.bool] = None,
    availability_node_outage: typing.Optional[builtins.bool] = None,
    availability_notifications_enabled: typing.Optional[builtins.bool] = None,
    location_node_outage_delay_in_minutes: typing.Optional[jsii.Number] = None,
    nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[CfnSyntheticLocationPropsStatus] = None,
    type: typing.Optional[CfnSyntheticLocationPropsType] = None,
) -> None:
    """Type checking stubs"""
    pass
