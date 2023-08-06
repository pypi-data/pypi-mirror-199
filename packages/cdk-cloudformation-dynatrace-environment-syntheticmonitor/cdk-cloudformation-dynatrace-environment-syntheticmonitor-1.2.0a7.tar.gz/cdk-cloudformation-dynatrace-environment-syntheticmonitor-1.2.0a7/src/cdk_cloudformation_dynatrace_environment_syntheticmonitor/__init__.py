'''
# dynatrace-environment-syntheticmonitor

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Dynatrace::Environment::SyntheticMonitor` v1.2.0.

## Description

Manage a synthetic monitor (V1) in Dynatrace.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-dynatrace-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Dynatrace::Environment::SyntheticMonitor \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Dynatrace-Environment-SyntheticMonitor \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Dynatrace::Environment::SyntheticMonitor`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fdynatrace-environment-syntheticmonitor+v1.2.0).
* Issues related to `Dynatrace::Environment::SyntheticMonitor` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-dynatrace-resource-providers).

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


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticmonitor.AnomalyDetectionPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "loading_time_thresholds": "loadingTimeThresholds",
        "outage_handling": "outageHandling",
    },
)
class AnomalyDetectionPolicy:
    def __init__(
        self,
        *,
        loading_time_thresholds: typing.Union["LoadingTimeThresholdsPolicy", typing.Dict[builtins.str, typing.Any]],
        outage_handling: typing.Union["OutageHandlingPolicy", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''The anomaly detection configuration.

        :param loading_time_thresholds: 
        :param outage_handling: 

        :schema: AnomalyDetectionPolicy
        '''
        if isinstance(loading_time_thresholds, dict):
            loading_time_thresholds = LoadingTimeThresholdsPolicy(**loading_time_thresholds)
        if isinstance(outage_handling, dict):
            outage_handling = OutageHandlingPolicy(**outage_handling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81949df42d5c0bc4870c1be8c1d9f8f5dc78e8ecc842c9e73fc1956db39dc5db)
            check_type(argname="argument loading_time_thresholds", value=loading_time_thresholds, expected_type=type_hints["loading_time_thresholds"])
            check_type(argname="argument outage_handling", value=outage_handling, expected_type=type_hints["outage_handling"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "loading_time_thresholds": loading_time_thresholds,
            "outage_handling": outage_handling,
        }

    @builtins.property
    def loading_time_thresholds(self) -> "LoadingTimeThresholdsPolicy":
        '''
        :schema: AnomalyDetectionPolicy#LoadingTimeThresholds
        '''
        result = self._values.get("loading_time_thresholds")
        assert result is not None, "Required property 'loading_time_thresholds' is missing"
        return typing.cast("LoadingTimeThresholdsPolicy", result)

    @builtins.property
    def outage_handling(self) -> "OutageHandlingPolicy":
        '''
        :schema: AnomalyDetectionPolicy#OutageHandling
        '''
        result = self._values.get("outage_handling")
        assert result is not None, "Required property 'outage_handling' is missing"
        return typing.cast("OutageHandlingPolicy", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AnomalyDetectionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfnSyntheticMonitor(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticmonitor.CfnSyntheticMonitor",
):
    '''A CloudFormation ``Dynatrace::Environment::SyntheticMonitor``.

    :cloudformationResource: Dynatrace::Environment::SyntheticMonitor
    :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        enabled: builtins.bool,
        frequency_min: "CfnSyntheticMonitorPropsFrequencyMin",
        name: builtins.str,
        anomaly_detection: typing.Optional[typing.Union[AnomalyDetectionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        automatically_assigned_apps: typing.Optional[typing.Sequence[builtins.str]] = None,
        locations: typing.Optional[typing.Sequence[builtins.str]] = None,
        management_zones: typing.Optional[typing.Sequence[typing.Any]] = None,
        manually_assigned_apps: typing.Optional[typing.Sequence[builtins.str]] = None,
        script: typing.Optional[typing.Union["CfnSyntheticMonitorPropsScript", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["Tag", typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional["CfnSyntheticMonitorPropsType"] = None,
    ) -> None:
        '''Create a new ``Dynatrace::Environment::SyntheticMonitor``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param enabled: The monitor is enabled (true) or disabled (false).
        :param frequency_min: The frequency of the monitor, in minutes. You can use one of the following values: 5, 10, 15, 30, and 60.
        :param name: The name of the monitor.
        :param anomaly_detection: 
        :param automatically_assigned_apps: A set of automatically assigned applications.
        :param locations: A list of locations from which the monitor is executed. To specify a location, use its entity ID.
        :param management_zones: A set of management zones to which the monitor belongs to.
        :param manually_assigned_apps: A set of manually assigned applications.
        :param script: The script of a browser (https://dt-url.net/9c103rda) or HTTP monitor.
        :param tags: A set of tags assigned to the monitor.
        :param type: Defines the actual set of fields depending on the value. See one of the following objects:. BROWSER -> BrowserSyntheticMonitor HTTP -> HttpSyntheticMonitor
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82479bf99e367e0fab5d26eef29ea3da0b5a54d434716266e7af968779236aa3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSyntheticMonitorProps(
            enabled=enabled,
            frequency_min=frequency_min,
            name=name,
            anomaly_detection=anomaly_detection,
            automatically_assigned_apps=automatically_assigned_apps,
            locations=locations,
            management_zones=management_zones,
            manually_assigned_apps=manually_assigned_apps,
            script=script,
            tags=tags,
            type=type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedFrom")
    def attr_created_from(self) -> builtins.str:
        '''Attribute ``Dynatrace::Environment::SyntheticMonitor.CreatedFrom``.

        :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedFrom"))

    @builtins.property
    @jsii.member(jsii_name="attrEntityId")
    def attr_entity_id(self) -> builtins.str:
        '''Attribute ``Dynatrace::Environment::SyntheticMonitor.EntityId``.

        :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEntityId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnSyntheticMonitorProps":
        '''Resource props.'''
        return typing.cast("CfnSyntheticMonitorProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticmonitor.CfnSyntheticMonitorProps",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "frequency_min": "frequencyMin",
        "name": "name",
        "anomaly_detection": "anomalyDetection",
        "automatically_assigned_apps": "automaticallyAssignedApps",
        "locations": "locations",
        "management_zones": "managementZones",
        "manually_assigned_apps": "manuallyAssignedApps",
        "script": "script",
        "tags": "tags",
        "type": "type",
    },
)
class CfnSyntheticMonitorProps:
    def __init__(
        self,
        *,
        enabled: builtins.bool,
        frequency_min: "CfnSyntheticMonitorPropsFrequencyMin",
        name: builtins.str,
        anomaly_detection: typing.Optional[typing.Union[AnomalyDetectionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        automatically_assigned_apps: typing.Optional[typing.Sequence[builtins.str]] = None,
        locations: typing.Optional[typing.Sequence[builtins.str]] = None,
        management_zones: typing.Optional[typing.Sequence[typing.Any]] = None,
        manually_assigned_apps: typing.Optional[typing.Sequence[builtins.str]] = None,
        script: typing.Optional[typing.Union["CfnSyntheticMonitorPropsScript", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["Tag", typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional["CfnSyntheticMonitorPropsType"] = None,
    ) -> None:
        '''Manage a synthetic monitor (V1) in Dynatrace.

        :param enabled: The monitor is enabled (true) or disabled (false).
        :param frequency_min: The frequency of the monitor, in minutes. You can use one of the following values: 5, 10, 15, 30, and 60.
        :param name: The name of the monitor.
        :param anomaly_detection: 
        :param automatically_assigned_apps: A set of automatically assigned applications.
        :param locations: A list of locations from which the monitor is executed. To specify a location, use its entity ID.
        :param management_zones: A set of management zones to which the monitor belongs to.
        :param manually_assigned_apps: A set of manually assigned applications.
        :param script: The script of a browser (https://dt-url.net/9c103rda) or HTTP monitor.
        :param tags: A set of tags assigned to the monitor.
        :param type: Defines the actual set of fields depending on the value. See one of the following objects:. BROWSER -> BrowserSyntheticMonitor HTTP -> HttpSyntheticMonitor

        :schema: CfnSyntheticMonitorProps
        '''
        if isinstance(anomaly_detection, dict):
            anomaly_detection = AnomalyDetectionPolicy(**anomaly_detection)
        if isinstance(script, dict):
            script = CfnSyntheticMonitorPropsScript(**script)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__620e053a2ad318507e6ef87fe4013efae05be98ab2bba2bcc464ebb1954de777)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument frequency_min", value=frequency_min, expected_type=type_hints["frequency_min"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument anomaly_detection", value=anomaly_detection, expected_type=type_hints["anomaly_detection"])
            check_type(argname="argument automatically_assigned_apps", value=automatically_assigned_apps, expected_type=type_hints["automatically_assigned_apps"])
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
            check_type(argname="argument management_zones", value=management_zones, expected_type=type_hints["management_zones"])
            check_type(argname="argument manually_assigned_apps", value=manually_assigned_apps, expected_type=type_hints["manually_assigned_apps"])
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "frequency_min": frequency_min,
            "name": name,
        }
        if anomaly_detection is not None:
            self._values["anomaly_detection"] = anomaly_detection
        if automatically_assigned_apps is not None:
            self._values["automatically_assigned_apps"] = automatically_assigned_apps
        if locations is not None:
            self._values["locations"] = locations
        if management_zones is not None:
            self._values["management_zones"] = management_zones
        if manually_assigned_apps is not None:
            self._values["manually_assigned_apps"] = manually_assigned_apps
        if script is not None:
            self._values["script"] = script
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''The monitor is enabled (true) or disabled (false).

        :schema: CfnSyntheticMonitorProps#Enabled
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def frequency_min(self) -> "CfnSyntheticMonitorPropsFrequencyMin":
        '''The frequency of the monitor, in minutes.

        You can use one of the following values: 5, 10, 15, 30, and 60.

        :schema: CfnSyntheticMonitorProps#FrequencyMin
        '''
        result = self._values.get("frequency_min")
        assert result is not None, "Required property 'frequency_min' is missing"
        return typing.cast("CfnSyntheticMonitorPropsFrequencyMin", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the monitor.

        :schema: CfnSyntheticMonitorProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def anomaly_detection(self) -> typing.Optional[AnomalyDetectionPolicy]:
        '''
        :schema: CfnSyntheticMonitorProps#AnomalyDetection
        '''
        result = self._values.get("anomaly_detection")
        return typing.cast(typing.Optional[AnomalyDetectionPolicy], result)

    @builtins.property
    def automatically_assigned_apps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of automatically assigned applications.

        :schema: CfnSyntheticMonitorProps#AutomaticallyAssignedApps
        '''
        result = self._values.get("automatically_assigned_apps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def locations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of locations from which the monitor is executed.

        To specify a location, use its entity ID.

        :schema: CfnSyntheticMonitorProps#Locations
        '''
        result = self._values.get("locations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def management_zones(self) -> typing.Optional[typing.List[typing.Any]]:
        '''A set of management zones to which the monitor belongs to.

        :schema: CfnSyntheticMonitorProps#ManagementZones
        '''
        result = self._values.get("management_zones")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def manually_assigned_apps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A set of manually assigned applications.

        :schema: CfnSyntheticMonitorProps#ManuallyAssignedApps
        '''
        result = self._values.get("manually_assigned_apps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def script(self) -> typing.Optional["CfnSyntheticMonitorPropsScript"]:
        '''The script of a browser (https://dt-url.net/9c103rda) or HTTP monitor.

        :schema: CfnSyntheticMonitorProps#Script
        '''
        result = self._values.get("script")
        return typing.cast(typing.Optional["CfnSyntheticMonitorPropsScript"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["Tag"]]:
        '''A set of tags assigned to the monitor.

        :schema: CfnSyntheticMonitorProps#Tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["Tag"]], result)

    @builtins.property
    def type(self) -> typing.Optional["CfnSyntheticMonitorPropsType"]:
        '''Defines the actual set of fields depending on the value. See one of the following objects:.

        BROWSER -> BrowserSyntheticMonitor
        HTTP -> HttpSyntheticMonitor

        :schema: CfnSyntheticMonitorProps#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional["CfnSyntheticMonitorPropsType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSyntheticMonitorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticmonitor.CfnSyntheticMonitorPropsFrequencyMin"
)
class CfnSyntheticMonitorPropsFrequencyMin(enum.Enum):
    '''The frequency of the monitor, in minutes.

    You can use one of the following values: 5, 10, 15, 30, and 60.

    :schema: CfnSyntheticMonitorPropsFrequencyMin
    '''

    VALUE_5 = "VALUE_5"
    '''5.'''
    VALUE_10 = "VALUE_10"
    '''10.'''
    VALUE_15 = "VALUE_15"
    '''15.'''
    VALUE_30 = "VALUE_30"
    '''30.'''
    VALUE_60 = "VALUE_60"
    '''60.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticmonitor.CfnSyntheticMonitorPropsScript",
    jsii_struct_bases=[],
    name_mapping={"requests": "requests", "version": "version"},
)
class CfnSyntheticMonitorPropsScript:
    def __init__(
        self,
        *,
        requests: typing.Optional[typing.Sequence[typing.Union["RequestsInput", typing.Dict[builtins.str, typing.Any]]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''The script of a browser (https://dt-url.net/9c103rda) or HTTP monitor.

        :param requests: 
        :param version: 

        :schema: CfnSyntheticMonitorPropsScript
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00aee9c5e489c7d08d6dc63ee718a7b8d38a30d780f639fc445ebf958848454c)
            check_type(argname="argument requests", value=requests, expected_type=type_hints["requests"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if requests is not None:
            self._values["requests"] = requests
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def requests(self) -> typing.Optional[typing.List["RequestsInput"]]:
        '''
        :schema: CfnSyntheticMonitorPropsScript#Requests
        '''
        result = self._values.get("requests")
        return typing.cast(typing.Optional[typing.List["RequestsInput"]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnSyntheticMonitorPropsScript#Version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSyntheticMonitorPropsScript(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticmonitor.CfnSyntheticMonitorPropsType"
)
class CfnSyntheticMonitorPropsType(enum.Enum):
    '''Defines the actual set of fields depending on the value. See one of the following objects:.

    BROWSER -> BrowserSyntheticMonitor
    HTTP -> HttpSyntheticMonitor

    :schema: CfnSyntheticMonitorPropsType
    '''

    BROWSER = "BROWSER"
    '''BROWSER.'''
    HTTP = "HTTP"
    '''HTTP.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticmonitor.GlobalOutagePolicy",
    jsii_struct_bases=[],
    name_mapping={"consecutive_runs": "consecutiveRuns"},
)
class GlobalOutagePolicy:
    def __init__(self, *, consecutive_runs: jsii.Number) -> None:
        '''Global outage handling configuration.

        :param consecutive_runs: Alert if all locations are unable to access the web application X times consecutively.

        :schema: GlobalOutagePolicy
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f5926d9a93db7986fbcf994b6b7e7c26bc3ab817698d5552a139faf242fd9da)
            check_type(argname="argument consecutive_runs", value=consecutive_runs, expected_type=type_hints["consecutive_runs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consecutive_runs": consecutive_runs,
        }

    @builtins.property
    def consecutive_runs(self) -> jsii.Number:
        '''Alert if all locations are unable to access the web application X times consecutively.

        :schema: GlobalOutagePolicy#ConsecutiveRuns
        '''
        result = self._values.get("consecutive_runs")
        assert result is not None, "Required property 'consecutive_runs' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlobalOutagePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticmonitor.LoadingTimeThreshold",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value_ms": "valueMs"},
)
class LoadingTimeThreshold:
    def __init__(
        self,
        *,
        type: "LoadingTimeThresholdType",
        value_ms: jsii.Number,
    ) -> None:
        '''The performance threshold rule.

        :param type: The type of the threshold: total loading time or action loading time.
        :param value_ms: Notify if monitor takes longer than X milliseconds to load.

        :schema: LoadingTimeThreshold
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc4d09afa0488aa99bd5621a0066fcb0c1122d0a226ab895d2f7a0c3d7688662)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value_ms", value=value_ms, expected_type=type_hints["value_ms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "value_ms": value_ms,
        }

    @builtins.property
    def type(self) -> "LoadingTimeThresholdType":
        '''The type of the threshold: total loading time or action loading time.

        :schema: LoadingTimeThreshold#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("LoadingTimeThresholdType", result)

    @builtins.property
    def value_ms(self) -> jsii.Number:
        '''Notify if monitor takes longer than X milliseconds to load.

        :schema: LoadingTimeThreshold#ValueMs
        '''
        result = self._values.get("value_ms")
        assert result is not None, "Required property 'value_ms' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadingTimeThreshold(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticmonitor.LoadingTimeThresholdType"
)
class LoadingTimeThresholdType(enum.Enum):
    '''The type of the threshold: total loading time or action loading time.

    :schema: LoadingTimeThresholdType
    '''

    ACTION = "ACTION"
    '''ACTION.'''
    TOTAL = "TOTAL"
    '''TOTAL.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticmonitor.LoadingTimeThresholdsPolicy",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "thresholds": "thresholds"},
)
class LoadingTimeThresholdsPolicy:
    def __init__(
        self,
        *,
        enabled: builtins.bool,
        thresholds: typing.Sequence[typing.Union[LoadingTimeThreshold, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''Performance thresholds configuration.

        :param enabled: Performance threshold is enabled (true) or disabled (false).
        :param thresholds: The list of performance threshold rules.

        :schema: LoadingTimeThresholdsPolicy
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00dde122eacb67775f2afcbf3fe90fbba832dd3920e644c4dccc73ae44f62fac)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument thresholds", value=thresholds, expected_type=type_hints["thresholds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "thresholds": thresholds,
        }

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''Performance threshold is enabled (true) or disabled (false).

        :schema: LoadingTimeThresholdsPolicy#Enabled
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def thresholds(self) -> typing.List[LoadingTimeThreshold]:
        '''The list of performance threshold rules.

        :schema: LoadingTimeThresholdsPolicy#Thresholds
        '''
        result = self._values.get("thresholds")
        assert result is not None, "Required property 'thresholds' is missing"
        return typing.cast(typing.List[LoadingTimeThreshold], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadingTimeThresholdsPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticmonitor.LocalOutagePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "affected_locations": "affectedLocations",
        "consecutive_runs": "consecutiveRuns",
    },
)
class LocalOutagePolicy:
    def __init__(
        self,
        *,
        affected_locations: jsii.Number,
        consecutive_runs: jsii.Number,
    ) -> None:
        '''Local outage handling configuration.

        Alert if affectedLocations of locations are unable to access the web application consecutiveRuns times consecutively.

        :param affected_locations: The number of affected locations to trigger an alert.
        :param consecutive_runs: The number of consecutive fails to trigger an alert.

        :schema: LocalOutagePolicy
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4287a781d1ac89e53704a601439b6eac9abb037ac8edb79ef526ae65f6c7d910)
            check_type(argname="argument affected_locations", value=affected_locations, expected_type=type_hints["affected_locations"])
            check_type(argname="argument consecutive_runs", value=consecutive_runs, expected_type=type_hints["consecutive_runs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "affected_locations": affected_locations,
            "consecutive_runs": consecutive_runs,
        }

    @builtins.property
    def affected_locations(self) -> jsii.Number:
        '''The number of affected locations to trigger an alert.

        :schema: LocalOutagePolicy#AffectedLocations
        '''
        result = self._values.get("affected_locations")
        assert result is not None, "Required property 'affected_locations' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def consecutive_runs(self) -> jsii.Number:
        '''The number of consecutive fails to trigger an alert.

        :schema: LocalOutagePolicy#ConsecutiveRuns
        '''
        result = self._values.get("consecutive_runs")
        assert result is not None, "Required property 'consecutive_runs' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LocalOutagePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticmonitor.OutageHandlingPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "global_outage": "globalOutage",
        "global_outage_policy": "globalOutagePolicy",
        "local_outage": "localOutage",
        "local_outage_policy": "localOutagePolicy",
        "retry_on_error": "retryOnError",
    },
)
class OutageHandlingPolicy:
    def __init__(
        self,
        *,
        global_outage: typing.Optional[builtins.bool] = None,
        global_outage_policy: typing.Optional[typing.Union[GlobalOutagePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        local_outage: typing.Optional[builtins.bool] = None,
        local_outage_policy: typing.Optional[typing.Union[LocalOutagePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        retry_on_error: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Outage handling configuration.

        :param global_outage: When enabled (true), generate a problem and send an alert when the monitor is unavailable at all configured locations.
        :param global_outage_policy: 
        :param local_outage: When enabled (true), generate a problem and send an alert when the monitor is unavailable for one or more consecutive runs at any location.
        :param local_outage_policy: 
        :param retry_on_error: Schedule retry if browser monitor execution results in a fail. For HTTP monitors this property is ignored.

        :schema: OutageHandlingPolicy
        '''
        if isinstance(global_outage_policy, dict):
            global_outage_policy = GlobalOutagePolicy(**global_outage_policy)
        if isinstance(local_outage_policy, dict):
            local_outage_policy = LocalOutagePolicy(**local_outage_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1769cca047412905eb576f36e02073397e9b7e17958e9a80ec4d6de24d399d5a)
            check_type(argname="argument global_outage", value=global_outage, expected_type=type_hints["global_outage"])
            check_type(argname="argument global_outage_policy", value=global_outage_policy, expected_type=type_hints["global_outage_policy"])
            check_type(argname="argument local_outage", value=local_outage, expected_type=type_hints["local_outage"])
            check_type(argname="argument local_outage_policy", value=local_outage_policy, expected_type=type_hints["local_outage_policy"])
            check_type(argname="argument retry_on_error", value=retry_on_error, expected_type=type_hints["retry_on_error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if global_outage is not None:
            self._values["global_outage"] = global_outage
        if global_outage_policy is not None:
            self._values["global_outage_policy"] = global_outage_policy
        if local_outage is not None:
            self._values["local_outage"] = local_outage
        if local_outage_policy is not None:
            self._values["local_outage_policy"] = local_outage_policy
        if retry_on_error is not None:
            self._values["retry_on_error"] = retry_on_error

    @builtins.property
    def global_outage(self) -> typing.Optional[builtins.bool]:
        '''When enabled (true), generate a problem and send an alert when the monitor is unavailable at all configured locations.

        :schema: OutageHandlingPolicy#GlobalOutage
        '''
        result = self._values.get("global_outage")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def global_outage_policy(self) -> typing.Optional[GlobalOutagePolicy]:
        '''
        :schema: OutageHandlingPolicy#GlobalOutagePolicy
        '''
        result = self._values.get("global_outage_policy")
        return typing.cast(typing.Optional[GlobalOutagePolicy], result)

    @builtins.property
    def local_outage(self) -> typing.Optional[builtins.bool]:
        '''When enabled (true), generate a problem and send an alert when the monitor is unavailable for one or more consecutive runs at any location.

        :schema: OutageHandlingPolicy#LocalOutage
        '''
        result = self._values.get("local_outage")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def local_outage_policy(self) -> typing.Optional[LocalOutagePolicy]:
        '''
        :schema: OutageHandlingPolicy#LocalOutagePolicy
        '''
        result = self._values.get("local_outage_policy")
        return typing.cast(typing.Optional[LocalOutagePolicy], result)

    @builtins.property
    def retry_on_error(self) -> typing.Optional[builtins.bool]:
        '''Schedule retry if browser monitor execution results in a fail.

        For HTTP monitors this property is ignored.

        :schema: OutageHandlingPolicy#RetryOnError
        '''
        result = self._values.get("retry_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OutageHandlingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticmonitor.RequestsInput",
    jsii_struct_bases=[],
    name_mapping={
        "configuration": "configuration",
        "description": "description",
        "method": "method",
        "url": "url",
        "validation": "validation",
    },
)
class RequestsInput:
    def __init__(
        self,
        *,
        configuration: typing.Optional[typing.Union["RequestsInputConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        method: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
        validation: typing.Optional[typing.Union["RequestsInputValidation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param configuration: 
        :param description: 
        :param method: 
        :param url: 
        :param validation: 

        :schema: RequestsInput
        '''
        if isinstance(configuration, dict):
            configuration = RequestsInputConfiguration(**configuration)
        if isinstance(validation, dict):
            validation = RequestsInputValidation(**validation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b991544ca0521f7f4319c5b1f33affef2038b03cd1ace6ca5aa2201caaf75ab)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument validation", value=validation, expected_type=type_hints["validation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration is not None:
            self._values["configuration"] = configuration
        if description is not None:
            self._values["description"] = description
        if method is not None:
            self._values["method"] = method
        if url is not None:
            self._values["url"] = url
        if validation is not None:
            self._values["validation"] = validation

    @builtins.property
    def configuration(self) -> typing.Optional["RequestsInputConfiguration"]:
        '''
        :schema: RequestsInput#Configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional["RequestsInputConfiguration"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :schema: RequestsInput#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''
        :schema: RequestsInput#Method
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''
        :schema: RequestsInput#Url
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validation(self) -> typing.Optional["RequestsInputValidation"]:
        '''
        :schema: RequestsInput#Validation
        '''
        result = self._values.get("validation")
        return typing.cast(typing.Optional["RequestsInputValidation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RequestsInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticmonitor.RequestsInputConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "accept_any_certificate": "acceptAnyCertificate",
        "follow_redirects": "followRedirects",
        "should_not_persist_sensitive_data": "shouldNotPersistSensitiveData",
    },
)
class RequestsInputConfiguration:
    def __init__(
        self,
        *,
        accept_any_certificate: typing.Optional[builtins.bool] = None,
        follow_redirects: typing.Optional[builtins.bool] = None,
        should_not_persist_sensitive_data: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param accept_any_certificate: 
        :param follow_redirects: 
        :param should_not_persist_sensitive_data: 

        :schema: RequestsInputConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4716cec3f2bc5a3a5a0f6c71b5ea79b834b1b16d281687c0ccdc11f7b7e48bac)
            check_type(argname="argument accept_any_certificate", value=accept_any_certificate, expected_type=type_hints["accept_any_certificate"])
            check_type(argname="argument follow_redirects", value=follow_redirects, expected_type=type_hints["follow_redirects"])
            check_type(argname="argument should_not_persist_sensitive_data", value=should_not_persist_sensitive_data, expected_type=type_hints["should_not_persist_sensitive_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accept_any_certificate is not None:
            self._values["accept_any_certificate"] = accept_any_certificate
        if follow_redirects is not None:
            self._values["follow_redirects"] = follow_redirects
        if should_not_persist_sensitive_data is not None:
            self._values["should_not_persist_sensitive_data"] = should_not_persist_sensitive_data

    @builtins.property
    def accept_any_certificate(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: RequestsInputConfiguration#AcceptAnyCertificate
        '''
        result = self._values.get("accept_any_certificate")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def follow_redirects(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: RequestsInputConfiguration#FollowRedirects
        '''
        result = self._values.get("follow_redirects")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def should_not_persist_sensitive_data(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: RequestsInputConfiguration#ShouldNotPersistSensitiveData
        '''
        result = self._values.get("should_not_persist_sensitive_data")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RequestsInputConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticmonitor.RequestsInputValidation",
    jsii_struct_bases=[],
    name_mapping={"rules": "rules"},
)
class RequestsInputValidation:
    def __init__(
        self,
        *,
        rules: typing.Optional[typing.Sequence[typing.Union["RequestsRules", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param rules: 

        :schema: RequestsInputValidation
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71745e98c16f31caf2f21808671b27f050e9a33dc3232535aed28ae6e336ac64)
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def rules(self) -> typing.Optional[typing.List["RequestsRules"]]:
        '''
        :schema: RequestsInputValidation#Rules
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.List["RequestsRules"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RequestsInputValidation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticmonitor.RequestsRules",
    jsii_struct_bases=[],
    name_mapping={"pass_if_found": "passIfFound", "type": "type", "value": "value"},
)
class RequestsRules:
    def __init__(
        self,
        *,
        pass_if_found: typing.Optional[builtins.bool] = None,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pass_if_found: 
        :param type: 
        :param value: 

        :schema: RequestsRules
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7830a490cfe27dfb62605dc48c4a0e821bc58bb8185c03da68f66c2b2007741f)
            check_type(argname="argument pass_if_found", value=pass_if_found, expected_type=type_hints["pass_if_found"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pass_if_found is not None:
            self._values["pass_if_found"] = pass_if_found
        if type is not None:
            self._values["type"] = type
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def pass_if_found(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: RequestsRules#PassIfFound
        '''
        result = self._values.get("pass_if_found")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: RequestsRules#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''
        :schema: RequestsRules#Value
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RequestsRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticmonitor.Tag",
    jsii_struct_bases=[],
    name_mapping={
        "context": "context",
        "key": "key",
        "source": "source",
        "value": "value",
    },
)
class Tag:
    def __init__(
        self,
        *,
        context: "TagContext",
        key: builtins.str,
        source: typing.Optional["TagSource"] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Tag with source of a Dynatrace entity.

        :param context: The origin of the tag, such as AWS or Cloud Foundry. Custom tags use the CONTEXTLESS value.
        :param key: The key of the tag. Custom tags have the tag value here.
        :param source: The source of the tag, such as USER, RULE_BASED or AUTO.
        :param value: The value of the tag. Not applicable to custom tags.

        :schema: Tag
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e3eb70e6de42e438dde39c2e45e6efeeb7c9daaaed0325d04e632944e98e52)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "context": context,
            "key": key,
        }
        if source is not None:
            self._values["source"] = source
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def context(self) -> "TagContext":
        '''The origin of the tag, such as AWS or Cloud Foundry.

        Custom tags use the CONTEXTLESS value.

        :schema: Tag#Context
        '''
        result = self._values.get("context")
        assert result is not None, "Required property 'context' is missing"
        return typing.cast("TagContext", result)

    @builtins.property
    def key(self) -> builtins.str:
        '''The key of the tag.

        Custom tags have the tag value here.

        :schema: Tag#Key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> typing.Optional["TagSource"]:
        '''The source of the tag, such as USER, RULE_BASED or AUTO.

        :schema: Tag#Source
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional["TagSource"], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The value of the tag.

        Not applicable to custom tags.

        :schema: Tag#Value
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Tag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticmonitor.TagContext"
)
class TagContext(enum.Enum):
    '''The origin of the tag, such as AWS or Cloud Foundry.

    Custom tags use the CONTEXTLESS value.

    :schema: TagContext
    '''

    AWS = "AWS"
    '''AWS.'''
    AWS_GENERIC = "AWS_GENERIC"
    '''AWS_GENERIC.'''
    AZURE = "AZURE"
    '''AZURE.'''
    CLOUD_FOUNDRY = "CLOUD_FOUNDRY"
    '''CLOUD_FOUNDRY.'''
    CONTEXTLESS = "CONTEXTLESS"
    '''CONTEXTLESS.'''
    ENVIRONMENT = "ENVIRONMENT"
    '''ENVIRONMENT.'''
    GOOGLE_CLOUD = "GOOGLE_CLOUD"
    '''GOOGLE_CLOUD.'''
    KUBERNETES = "KUBERNETES"
    '''KUBERNETES.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/dynatrace-environment-syntheticmonitor.TagSource"
)
class TagSource(enum.Enum):
    '''The source of the tag, such as USER, RULE_BASED or AUTO.

    :schema: TagSource
    '''

    AUTO = "AUTO"
    '''AUTO.'''
    RULE_BASED = "RULE_BASED"
    '''RULE_BASED.'''
    USER = "USER"
    '''USER.'''


__all__ = [
    "AnomalyDetectionPolicy",
    "CfnSyntheticMonitor",
    "CfnSyntheticMonitorProps",
    "CfnSyntheticMonitorPropsFrequencyMin",
    "CfnSyntheticMonitorPropsScript",
    "CfnSyntheticMonitorPropsType",
    "GlobalOutagePolicy",
    "LoadingTimeThreshold",
    "LoadingTimeThresholdType",
    "LoadingTimeThresholdsPolicy",
    "LocalOutagePolicy",
    "OutageHandlingPolicy",
    "RequestsInput",
    "RequestsInputConfiguration",
    "RequestsInputValidation",
    "RequestsRules",
    "Tag",
    "TagContext",
    "TagSource",
]

publication.publish()

def _typecheckingstub__81949df42d5c0bc4870c1be8c1d9f8f5dc78e8ecc842c9e73fc1956db39dc5db(
    *,
    loading_time_thresholds: typing.Union[LoadingTimeThresholdsPolicy, typing.Dict[builtins.str, typing.Any]],
    outage_handling: typing.Union[OutageHandlingPolicy, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82479bf99e367e0fab5d26eef29ea3da0b5a54d434716266e7af968779236aa3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    enabled: builtins.bool,
    frequency_min: CfnSyntheticMonitorPropsFrequencyMin,
    name: builtins.str,
    anomaly_detection: typing.Optional[typing.Union[AnomalyDetectionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    automatically_assigned_apps: typing.Optional[typing.Sequence[builtins.str]] = None,
    locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    management_zones: typing.Optional[typing.Sequence[typing.Any]] = None,
    manually_assigned_apps: typing.Optional[typing.Sequence[builtins.str]] = None,
    script: typing.Optional[typing.Union[CfnSyntheticMonitorPropsScript, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[CfnSyntheticMonitorPropsType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__620e053a2ad318507e6ef87fe4013efae05be98ab2bba2bcc464ebb1954de777(
    *,
    enabled: builtins.bool,
    frequency_min: CfnSyntheticMonitorPropsFrequencyMin,
    name: builtins.str,
    anomaly_detection: typing.Optional[typing.Union[AnomalyDetectionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    automatically_assigned_apps: typing.Optional[typing.Sequence[builtins.str]] = None,
    locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    management_zones: typing.Optional[typing.Sequence[typing.Any]] = None,
    manually_assigned_apps: typing.Optional[typing.Sequence[builtins.str]] = None,
    script: typing.Optional[typing.Union[CfnSyntheticMonitorPropsScript, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[CfnSyntheticMonitorPropsType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00aee9c5e489c7d08d6dc63ee718a7b8d38a30d780f639fc445ebf958848454c(
    *,
    requests: typing.Optional[typing.Sequence[typing.Union[RequestsInput, typing.Dict[builtins.str, typing.Any]]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5926d9a93db7986fbcf994b6b7e7c26bc3ab817698d5552a139faf242fd9da(
    *,
    consecutive_runs: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc4d09afa0488aa99bd5621a0066fcb0c1122d0a226ab895d2f7a0c3d7688662(
    *,
    type: LoadingTimeThresholdType,
    value_ms: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00dde122eacb67775f2afcbf3fe90fbba832dd3920e644c4dccc73ae44f62fac(
    *,
    enabled: builtins.bool,
    thresholds: typing.Sequence[typing.Union[LoadingTimeThreshold, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4287a781d1ac89e53704a601439b6eac9abb037ac8edb79ef526ae65f6c7d910(
    *,
    affected_locations: jsii.Number,
    consecutive_runs: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1769cca047412905eb576f36e02073397e9b7e17958e9a80ec4d6de24d399d5a(
    *,
    global_outage: typing.Optional[builtins.bool] = None,
    global_outage_policy: typing.Optional[typing.Union[GlobalOutagePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    local_outage: typing.Optional[builtins.bool] = None,
    local_outage_policy: typing.Optional[typing.Union[LocalOutagePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_on_error: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b991544ca0521f7f4319c5b1f33affef2038b03cd1ace6ca5aa2201caaf75ab(
    *,
    configuration: typing.Optional[typing.Union[RequestsInputConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    method: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
    validation: typing.Optional[typing.Union[RequestsInputValidation, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4716cec3f2bc5a3a5a0f6c71b5ea79b834b1b16d281687c0ccdc11f7b7e48bac(
    *,
    accept_any_certificate: typing.Optional[builtins.bool] = None,
    follow_redirects: typing.Optional[builtins.bool] = None,
    should_not_persist_sensitive_data: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71745e98c16f31caf2f21808671b27f050e9a33dc3232535aed28ae6e336ac64(
    *,
    rules: typing.Optional[typing.Sequence[typing.Union[RequestsRules, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7830a490cfe27dfb62605dc48c4a0e821bc58bb8185c03da68f66c2b2007741f(
    *,
    pass_if_found: typing.Optional[builtins.bool] = None,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e3eb70e6de42e438dde39c2e45e6efeeb7c9daaaed0325d04e632944e98e52(
    *,
    context: TagContext,
    key: builtins.str,
    source: typing.Optional[TagSource] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
