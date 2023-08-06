'''
# dynatrace-environment-metric

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Dynatrace::Environment::Metric` v1.1.0.

## Description

Manage a timeseries metric (V1) in Dynatrace.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-dynatrace-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Dynatrace::Environment::Metric \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Dynatrace-Environment-Metric \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Dynatrace::Environment::Metric`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fdynatrace-environment-metric+v1.1.0).
* Issues related to `Dynatrace::Environment::Metric` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-dynatrace-resource-providers).

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


class CfnMetric(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/dynatrace-environment-metric.CfnMetric",
):
    '''A CloudFormation ``Dynatrace::Environment::Metric``.

    :cloudformationResource: Dynatrace::Environment::Metric
    :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        plugin_id: typing.Optional[builtins.str] = None,
        timeseries_id: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
        unit: typing.Optional["Unit"] = None,
        warnings: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``Dynatrace::Environment::Metric``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param dimensions: 
        :param display_name: 
        :param plugin_id: The ID of the plugin, where the metric originates.
        :param timeseries_id: 
        :param types: 
        :param unit: 
        :param warnings: The warnings that occurred while creating the metric.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a578efa97501092d35877a88732e7c1e51bf877d5f7662f88d563a3a4a83bf48)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMetricProps(
            dimensions=dimensions,
            display_name=display_name,
            plugin_id=plugin_id,
            timeseries_id=timeseries_id,
            types=types,
            unit=unit,
            warnings=warnings,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAggregationTypes")
    def attr_aggregation_types(self) -> typing.List[builtins.str]:
        '''Attribute ``Dynatrace::Environment::Metric.AggregationTypes``.

        :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrAggregationTypes"))

    @builtins.property
    @jsii.member(jsii_name="attrDetailedSource")
    def attr_detailed_source(self) -> builtins.str:
        '''Attribute ``Dynatrace::Environment::Metric.DetailedSource``.

        :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDetailedSource"))

    @builtins.property
    @jsii.member(jsii_name="attrFilter")
    def attr_filter(self) -> builtins.str:
        '''Attribute ``Dynatrace::Environment::Metric.Filter``.

        :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFilter"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnMetricProps":
        '''Resource props.'''
        return typing.cast("CfnMetricProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-environment-metric.CfnMetricProps",
    jsii_struct_bases=[],
    name_mapping={
        "dimensions": "dimensions",
        "display_name": "displayName",
        "plugin_id": "pluginId",
        "timeseries_id": "timeseriesId",
        "types": "types",
        "unit": "unit",
        "warnings": "warnings",
    },
)
class CfnMetricProps:
    def __init__(
        self,
        *,
        dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        plugin_id: typing.Optional[builtins.str] = None,
        timeseries_id: typing.Optional[builtins.str] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
        unit: typing.Optional["Unit"] = None,
        warnings: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Manage a timeseries metric (V1) in Dynatrace.

        :param dimensions: 
        :param display_name: 
        :param plugin_id: The ID of the plugin, where the metric originates.
        :param timeseries_id: 
        :param types: 
        :param unit: 
        :param warnings: The warnings that occurred while creating the metric.

        :schema: CfnMetricProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26f1d8eeaebebb4dd5721b8698eedcfe4d2976285e03f2498adb1836b7573eaa)
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument plugin_id", value=plugin_id, expected_type=type_hints["plugin_id"])
            check_type(argname="argument timeseries_id", value=timeseries_id, expected_type=type_hints["timeseries_id"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            check_type(argname="argument warnings", value=warnings, expected_type=type_hints["warnings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if display_name is not None:
            self._values["display_name"] = display_name
        if plugin_id is not None:
            self._values["plugin_id"] = plugin_id
        if timeseries_id is not None:
            self._values["timeseries_id"] = timeseries_id
        if types is not None:
            self._values["types"] = types
        if unit is not None:
            self._values["unit"] = unit
        if warnings is not None:
            self._values["warnings"] = warnings

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: CfnMetricProps#Dimensions
        '''
        result = self._values.get("dimensions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnMetricProps#DisplayName
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the plugin, where the metric originates.

        :schema: CfnMetricProps#PluginId
        '''
        result = self._values.get("plugin_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeseries_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnMetricProps#TimeseriesId
        '''
        result = self._values.get("timeseries_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :schema: CfnMetricProps#Types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def unit(self) -> typing.Optional["Unit"]:
        '''
        :schema: CfnMetricProps#Unit
        '''
        result = self._values.get("unit")
        return typing.cast(typing.Optional["Unit"], result)

    @builtins.property
    def warnings(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The warnings that occurred while creating the metric.

        :schema: CfnMetricProps#Warnings
        '''
        result = self._values.get("warnings")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMetricProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/dynatrace-environment-metric.Unit")
class Unit(enum.Enum):
    '''The unit of the metric.

    :schema: Unit
    '''

    BILLION_BILCOUNT = "BILLION_BILCOUNT"
    '''Billion (bilcount).'''
    BIT_BIT = "BIT_BIT"
    '''Bit (bit).'''
    BIT_PER_HOUR_BIT_H = "BIT_PER_HOUR_BIT_H"
    '''BitPerHour (bit/h).'''
    BIT_PER_MINUTE_BIT_MIN = "BIT_PER_MINUTE_BIT_MIN"
    '''BitPerMinute (bit/min).'''
    BIT_PER_SECOND_BIT_S = "BIT_PER_SECOND_BIT_S"
    '''BitPerSecond (bit/s).'''
    BYTE_B = "BYTE_B"
    '''Byte (B).'''
    BYTE_PER_HOUR_B_H = "BYTE_PER_HOUR_B_H"
    '''BytePerHour (B/h).'''
    BYTE_PER_MINUTE_B_MIN = "BYTE_PER_MINUTE_B_MIN"
    '''BytePerMinute (B/min).'''
    BYTE_PER_SECOND_B_S = "BYTE_PER_SECOND_B_S"
    '''BytePerSecond (B/s).'''
    CORES = "CORES"
    '''Cores.'''
    COUNT_COUNT = "COUNT_COUNT"
    '''Count (count).'''
    DAY_DS = "DAY_DS"
    '''Day (ds).'''
    DECIBEL_MILLI_WATT_D_BM = "DECIBEL_MILLI_WATT_D_BM"
    '''DecibelMilliWatt (dBm).'''
    G = "G"
    '''G.'''
    GIBI_BYTE_GI_B = "GIBI_BYTE_GI_B"
    '''GibiByte (GiB).'''
    GIGA_BYTE_GB = "GIGA_BYTE_GB"
    '''GigaByte (GB).'''
    HOUR_HS = "HOUR_HS"
    '''Hour (hs).'''
    KIBI_BYTE_KI_B = "KIBI_BYTE_KI_B"
    '''KibiByte (KiB).'''
    KIBI_BYTE_PER_HOUR_KI_B_H = "KIBI_BYTE_PER_HOUR_KI_B_H"
    '''KibiBytePerHour (KiB/h).'''
    KIBI_BYTE_PER_MINUTE_KI_B_MIN = "KIBI_BYTE_PER_MINUTE_KI_B_MIN"
    '''KibiBytePerMinute (KiB/min).'''
    KIBI_BYTE_PER_SECOND_KI_B_S = "KIBI_BYTE_PER_SECOND_KI_B_S"
    '''KibiBytePerSecond (KiB/s).'''
    KILO_BYTE_K_B = "KILO_BYTE_K_B"
    '''KiloByte (kB).'''
    KILO_BYTE_PER_HOUR_K_B_H = "KILO_BYTE_PER_HOUR_K_B_H"
    '''KiloBytePerHour (kB/h).'''
    KILO_BYTE_PER_MINUTE_K_B_MIN = "KILO_BYTE_PER_MINUTE_K_B_MIN"
    '''KiloBytePerMinute (kB/min).'''
    KILO_BYTE_PER_SECOND_K_B_S = "KILO_BYTE_PER_SECOND_K_B_S"
    '''KiloBytePerSecond (kB/s).'''
    M = "M"
    '''M.'''
    MSU = "MSU"
    '''MSU.'''
    MEBI_BYTE_MI_B = "MEBI_BYTE_MI_B"
    '''MebiByte (MiB).'''
    MEBI_BYTE_PER_HOUR_MI_B_H = "MEBI_BYTE_PER_HOUR_MI_B_H"
    '''MebiBytePerHour (MiB/h).'''
    MEBI_BYTE_PER_MINUTE_MI_B_MIN = "MEBI_BYTE_PER_MINUTE_MI_B_MIN"
    '''MebiBytePerMinute (MiB/min).'''
    MEBI_BYTE_PER_SECOND_MI_B_S = "MEBI_BYTE_PER_SECOND_MI_B_S"
    '''MebiBytePerSecond (MiB/s).'''
    MEGA_BYTE_MB = "MEGA_BYTE_MB"
    '''MegaByte (MB).'''
    MEGA_BYTE_PER_HOUR_MB_H = "MEGA_BYTE_PER_HOUR_MB_H"
    '''MegaBytePerHour (MB/h).'''
    MEGA_BYTE_PER_MINUTE_MB_MIN = "MEGA_BYTE_PER_MINUTE_MB_MIN"
    '''MegaBytePerMinute (MB/min).'''
    MEGA_BYTE_PER_SECOND_MB_S = "MEGA_BYTE_PER_SECOND_MB_S"
    '''MegaBytePerSecond (MB/s).'''
    MICRO_SECOND_S = "MICRO_SECOND_S"
    '''MicroSecond (?s).'''
    MILLI_SECOND_MS = "MILLI_SECOND_MS"
    '''MilliSecond (ms).'''
    MILLI_SECOND_PER_MINUTE_MS_MIN = "MILLI_SECOND_PER_MINUTE_MS_MIN"
    '''MilliSecondPerMinute (ms/min).'''
    MILLION_MILCOUNT = "MILLION_MILCOUNT"
    '''Million (milcount).'''
    MINUTE_MINS = "MINUTE_MINS"
    '''Minute (mins).'''
    MONTH_MOS = "MONTH_MOS"
    '''Month (mos).'''
    N_A = "N_A"
    '''N/A.'''
    NANO_SECOND_NS = "NANO_SECOND_NS"
    '''NanoSecond (ns).'''
    NANO_SECOND_PER_MINUTE_NS_MIN = "NANO_SECOND_PER_MINUTE_NS_MIN"
    '''NanoSecondPerMinute (ns/min).'''
    PER_HOUR_COUNT_H = "PER_HOUR_COUNT_H"
    '''PerHour (count/h).'''
    PER_MINUTE_COUNT_MIN = "PER_MINUTE_COUNT_MIN"
    '''PerMinute (count/min).'''
    PER_SECOND_COUNT_S = "PER_SECOND_COUNT_S"
    '''PerSecond (count/s).'''
    PERCENT = "PERCENT"
    '''Percent (%).'''
    PIXEL_PX = "PIXEL_PX"
    '''Pixel (px).'''
    PROMILLE = "PROMILLE"
    '''Promille (?).'''
    RATIO = "RATIO"
    '''Ratio.'''
    SECOND_S = "SECOND_S"
    '''Second (s).'''
    STATE = "STATE"
    '''State.'''
    UNSPECIFIED = "UNSPECIFIED"
    '''Unspecified.'''
    WEEK_WS = "WEEK_WS"
    '''Week (ws).'''
    YEAR_YS = "YEAR_YS"
    '''Year (ys).'''
    K = "K"
    '''k.'''
    KM_H = "KM_H"
    '''km/h.'''
    M_H = "M_H"
    '''m/h.'''
    M_S = "M_S"
    '''m/s.'''
    M_CORES = "M_CORES"
    '''mCores.'''


__all__ = [
    "CfnMetric",
    "CfnMetricProps",
    "Unit",
]

publication.publish()

def _typecheckingstub__a578efa97501092d35877a88732e7c1e51bf877d5f7662f88d563a3a4a83bf48(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    plugin_id: typing.Optional[builtins.str] = None,
    timeseries_id: typing.Optional[builtins.str] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
    unit: typing.Optional[Unit] = None,
    warnings: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26f1d8eeaebebb4dd5721b8698eedcfe4d2976285e03f2498adb1836b7573eaa(
    *,
    dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    plugin_id: typing.Optional[builtins.str] = None,
    timeseries_id: typing.Optional[builtins.str] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
    unit: typing.Optional[Unit] = None,
    warnings: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
