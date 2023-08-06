'''
# dynatrace-environment-servicelevelobjective

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Dynatrace::Environment::ServiceLevelObjective` v1.3.0.

## Description

Manage a Service Level Objective in Dynatrace.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-dynatrace-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Dynatrace::Environment::ServiceLevelObjective \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Dynatrace-Environment-ServiceLevelObjective \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Dynatrace::Environment::ServiceLevelObjective`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fdynatrace-environment-servicelevelobjective+v1.3.0).
* Issues related to `Dynatrace::Environment::ServiceLevelObjective` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-dynatrace-resource-providers).

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


class CfnServiceLevelObjective(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/dynatrace-environment-servicelevelobjective.CfnServiceLevelObjective",
):
    '''A CloudFormation ``Dynatrace::Environment::ServiceLevelObjective``.

    :cloudformationResource: Dynatrace::Environment::ServiceLevelObjective
    :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        evaluation_type: "CfnServiceLevelObjectivePropsEvaluationType",
        name: builtins.str,
        timeframe: builtins.str,
        description: typing.Optional[builtins.str] = None,
        error_budget_burn_rate: typing.Optional[typing.Union["ErrorBudgetBurnRate", typing.Dict[builtins.str, typing.Any]]] = None,
        filter: typing.Optional[builtins.str] = None,
        has_access: typing.Optional[builtins.bool] = None,
        metric_expression: typing.Optional[builtins.str] = None,
        metric_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[jsii.Number] = None,
        warning: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``Dynatrace::Environment::ServiceLevelObjective``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param evaluation_type: The evaluation type of the SLO.
        :param name: The name of the SLO.
        :param timeframe: The timeframe for the SLO evaluation. Use the syntax of the global timeframe selector.
        :param description: The description of the SLO.
        :param error_budget_burn_rate: 
        :param filter: The entity filter for the SLO evaluation. Use the syntax of entity selector (https://dt-url.net/entityselector).
        :param has_access: The SLO is accessible through the settings if hasAccess is true.
        :param metric_expression: The percentage-based metric expression for the calculation of the SLO.
        :param metric_name: The name for a metric expression.
        :param target: The target value of the SLO.
        :param warning: The warning value of the SLO. At warning state the SLO is still fulfilled but is getting close to failure.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66cb0592a4066ed2ac350f622b0ab514f0a6dd8fec6a8f646e0f277a11cb07a7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServiceLevelObjectiveProps(
            evaluation_type=evaluation_type,
            name=name,
            timeframe=timeframe,
            description=description,
            error_budget_burn_rate=error_budget_burn_rate,
            filter=filter,
            has_access=has_access,
            metric_expression=metric_expression,
            metric_name=metric_name,
            target=target,
            warning=warning,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrBurnRateMetricKey")
    def attr_burn_rate_metric_key(self) -> builtins.str:
        '''Attribute ``Dynatrace::Environment::ServiceLevelObjective.BurnRateMetricKey``.

        :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrBurnRateMetricKey"))

    @builtins.property
    @jsii.member(jsii_name="attrEnabled")
    def attr_enabled(self) -> _aws_cdk_ceddda9d.IResolvable:
        '''Attribute ``Dynatrace::Environment::ServiceLevelObjective.Enabled``.

        :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
        '''
        return typing.cast(_aws_cdk_ceddda9d.IResolvable, jsii.get(self, "attrEnabled"))

    @builtins.property
    @jsii.member(jsii_name="attrError")
    def attr_error(self) -> builtins.str:
        '''Attribute ``Dynatrace::Environment::ServiceLevelObjective.Error``.

        :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrError"))

    @builtins.property
    @jsii.member(jsii_name="attrErrorBudget")
    def attr_error_budget(self) -> jsii.Number:
        '''Attribute ``Dynatrace::Environment::ServiceLevelObjective.ErrorBudget``.

        :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrErrorBudget"))

    @builtins.property
    @jsii.member(jsii_name="attrEvaluatedPercentage")
    def attr_evaluated_percentage(self) -> jsii.Number:
        '''Attribute ``Dynatrace::Environment::ServiceLevelObjective.EvaluatedPercentage``.

        :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrEvaluatedPercentage"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''Attribute ``Dynatrace::Environment::ServiceLevelObjective.Id``.

        :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrMetricKey")
    def attr_metric_key(self) -> builtins.str:
        '''Attribute ``Dynatrace::Environment::ServiceLevelObjective.MetricKey``.

        :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMetricKey"))

    @builtins.property
    @jsii.member(jsii_name="attrRelatedOpenProblems")
    def attr_related_open_problems(self) -> jsii.Number:
        '''Attribute ``Dynatrace::Environment::ServiceLevelObjective.RelatedOpenProblems``.

        :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrRelatedOpenProblems"))

    @builtins.property
    @jsii.member(jsii_name="attrRelatedTotalProblems")
    def attr_related_total_problems(self) -> jsii.Number:
        '''Attribute ``Dynatrace::Environment::ServiceLevelObjective.RelatedTotalProblems``.

        :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrRelatedTotalProblems"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''Attribute ``Dynatrace::Environment::ServiceLevelObjective.Status``.

        :link: https://github.com/aws-ia/cloudformation-dynatrace-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnServiceLevelObjectiveProps":
        '''Resource props.'''
        return typing.cast("CfnServiceLevelObjectiveProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-environment-servicelevelobjective.CfnServiceLevelObjectiveProps",
    jsii_struct_bases=[],
    name_mapping={
        "evaluation_type": "evaluationType",
        "name": "name",
        "timeframe": "timeframe",
        "description": "description",
        "error_budget_burn_rate": "errorBudgetBurnRate",
        "filter": "filter",
        "has_access": "hasAccess",
        "metric_expression": "metricExpression",
        "metric_name": "metricName",
        "target": "target",
        "warning": "warning",
    },
)
class CfnServiceLevelObjectiveProps:
    def __init__(
        self,
        *,
        evaluation_type: "CfnServiceLevelObjectivePropsEvaluationType",
        name: builtins.str,
        timeframe: builtins.str,
        description: typing.Optional[builtins.str] = None,
        error_budget_burn_rate: typing.Optional[typing.Union["ErrorBudgetBurnRate", typing.Dict[builtins.str, typing.Any]]] = None,
        filter: typing.Optional[builtins.str] = None,
        has_access: typing.Optional[builtins.bool] = None,
        metric_expression: typing.Optional[builtins.str] = None,
        metric_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[jsii.Number] = None,
        warning: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Manage a Service Level Objective in Dynatrace.

        :param evaluation_type: The evaluation type of the SLO.
        :param name: The name of the SLO.
        :param timeframe: The timeframe for the SLO evaluation. Use the syntax of the global timeframe selector.
        :param description: The description of the SLO.
        :param error_budget_burn_rate: 
        :param filter: The entity filter for the SLO evaluation. Use the syntax of entity selector (https://dt-url.net/entityselector).
        :param has_access: The SLO is accessible through the settings if hasAccess is true.
        :param metric_expression: The percentage-based metric expression for the calculation of the SLO.
        :param metric_name: The name for a metric expression.
        :param target: The target value of the SLO.
        :param warning: The warning value of the SLO. At warning state the SLO is still fulfilled but is getting close to failure.

        :schema: CfnServiceLevelObjectiveProps
        '''
        if isinstance(error_budget_burn_rate, dict):
            error_budget_burn_rate = ErrorBudgetBurnRate(**error_budget_burn_rate)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee30f2ceb916bf64407e98b8a7166e7fd6b85b423ca9cd94673c961bc9f99926)
            check_type(argname="argument evaluation_type", value=evaluation_type, expected_type=type_hints["evaluation_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument timeframe", value=timeframe, expected_type=type_hints["timeframe"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument error_budget_burn_rate", value=error_budget_burn_rate, expected_type=type_hints["error_budget_burn_rate"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument has_access", value=has_access, expected_type=type_hints["has_access"])
            check_type(argname="argument metric_expression", value=metric_expression, expected_type=type_hints["metric_expression"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument warning", value=warning, expected_type=type_hints["warning"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "evaluation_type": evaluation_type,
            "name": name,
            "timeframe": timeframe,
        }
        if description is not None:
            self._values["description"] = description
        if error_budget_burn_rate is not None:
            self._values["error_budget_burn_rate"] = error_budget_burn_rate
        if filter is not None:
            self._values["filter"] = filter
        if has_access is not None:
            self._values["has_access"] = has_access
        if metric_expression is not None:
            self._values["metric_expression"] = metric_expression
        if metric_name is not None:
            self._values["metric_name"] = metric_name
        if target is not None:
            self._values["target"] = target
        if warning is not None:
            self._values["warning"] = warning

    @builtins.property
    def evaluation_type(self) -> "CfnServiceLevelObjectivePropsEvaluationType":
        '''The evaluation type of the SLO.

        :schema: CfnServiceLevelObjectiveProps#EvaluationType
        '''
        result = self._values.get("evaluation_type")
        assert result is not None, "Required property 'evaluation_type' is missing"
        return typing.cast("CfnServiceLevelObjectivePropsEvaluationType", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the SLO.

        :schema: CfnServiceLevelObjectiveProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timeframe(self) -> builtins.str:
        '''The timeframe for the SLO evaluation.

        Use the syntax of the global timeframe selector.

        :schema: CfnServiceLevelObjectiveProps#Timeframe
        '''
        result = self._values.get("timeframe")
        assert result is not None, "Required property 'timeframe' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the SLO.

        :schema: CfnServiceLevelObjectiveProps#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def error_budget_burn_rate(self) -> typing.Optional["ErrorBudgetBurnRate"]:
        '''
        :schema: CfnServiceLevelObjectiveProps#ErrorBudgetBurnRate
        '''
        result = self._values.get("error_budget_burn_rate")
        return typing.cast(typing.Optional["ErrorBudgetBurnRate"], result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''The entity filter for the SLO evaluation.

        Use the syntax of entity selector (https://dt-url.net/entityselector).

        :schema: CfnServiceLevelObjectiveProps#Filter
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def has_access(self) -> typing.Optional[builtins.bool]:
        '''The SLO is accessible through the settings if hasAccess is true.

        :schema: CfnServiceLevelObjectiveProps#HasAccess
        '''
        result = self._values.get("has_access")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def metric_expression(self) -> typing.Optional[builtins.str]:
        '''The percentage-based metric expression for the calculation of the SLO.

        :schema: CfnServiceLevelObjectiveProps#MetricExpression
        '''
        result = self._values.get("metric_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metric_name(self) -> typing.Optional[builtins.str]:
        '''The name for a metric expression.

        :schema: CfnServiceLevelObjectiveProps#MetricName
        '''
        result = self._values.get("metric_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[jsii.Number]:
        '''The target value of the SLO.

        :schema: CfnServiceLevelObjectiveProps#Target
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def warning(self) -> typing.Optional[jsii.Number]:
        '''The warning value of the SLO.

        At warning state the SLO is still fulfilled but is getting close to failure.

        :schema: CfnServiceLevelObjectiveProps#Warning
        '''
        result = self._values.get("warning")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceLevelObjectiveProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/dynatrace-environment-servicelevelobjective.CfnServiceLevelObjectivePropsEvaluationType"
)
class CfnServiceLevelObjectivePropsEvaluationType(enum.Enum):
    '''The evaluation type of the SLO.

    :schema: CfnServiceLevelObjectivePropsEvaluationType
    '''

    AGGREGATE = "AGGREGATE"
    '''AGGREGATE.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/dynatrace-environment-servicelevelobjective.ErrorBudgetBurnRate",
    jsii_struct_bases=[],
    name_mapping={
        "burn_rate_visualization_enabled": "burnRateVisualizationEnabled",
        "fast_burn_threshold": "fastBurnThreshold",
    },
)
class ErrorBudgetBurnRate:
    def __init__(
        self,
        *,
        burn_rate_visualization_enabled: builtins.bool,
        fast_burn_threshold: jsii.Number,
    ) -> None:
        '''Error budget burn rate configuration of a service-level objective (SLO).

        :param burn_rate_visualization_enabled: The error budget burn rate visualization is enabled (true) or disabled (false). In case of false, no calculated values will be present here.
        :param fast_burn_threshold: The threshold between a slow and a fast burn rate.

        :schema: ErrorBudgetBurnRate
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd1e0e418612b16d97f0e47d8e9d40fbd4d0bdd5a07461590d325c610da41d1)
            check_type(argname="argument burn_rate_visualization_enabled", value=burn_rate_visualization_enabled, expected_type=type_hints["burn_rate_visualization_enabled"])
            check_type(argname="argument fast_burn_threshold", value=fast_burn_threshold, expected_type=type_hints["fast_burn_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "burn_rate_visualization_enabled": burn_rate_visualization_enabled,
            "fast_burn_threshold": fast_burn_threshold,
        }

    @builtins.property
    def burn_rate_visualization_enabled(self) -> builtins.bool:
        '''The error budget burn rate visualization is enabled (true) or disabled (false).

        In case of false, no calculated values will be present here.

        :schema: ErrorBudgetBurnRate#BurnRateVisualizationEnabled
        '''
        result = self._values.get("burn_rate_visualization_enabled")
        assert result is not None, "Required property 'burn_rate_visualization_enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def fast_burn_threshold(self) -> jsii.Number:
        '''The threshold between a slow and a fast burn rate.

        :schema: ErrorBudgetBurnRate#FastBurnThreshold
        '''
        result = self._values.get("fast_burn_threshold")
        assert result is not None, "Required property 'fast_burn_threshold' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ErrorBudgetBurnRate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnServiceLevelObjective",
    "CfnServiceLevelObjectiveProps",
    "CfnServiceLevelObjectivePropsEvaluationType",
    "ErrorBudgetBurnRate",
]

publication.publish()

def _typecheckingstub__66cb0592a4066ed2ac350f622b0ab514f0a6dd8fec6a8f646e0f277a11cb07a7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    evaluation_type: CfnServiceLevelObjectivePropsEvaluationType,
    name: builtins.str,
    timeframe: builtins.str,
    description: typing.Optional[builtins.str] = None,
    error_budget_burn_rate: typing.Optional[typing.Union[ErrorBudgetBurnRate, typing.Dict[builtins.str, typing.Any]]] = None,
    filter: typing.Optional[builtins.str] = None,
    has_access: typing.Optional[builtins.bool] = None,
    metric_expression: typing.Optional[builtins.str] = None,
    metric_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[jsii.Number] = None,
    warning: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee30f2ceb916bf64407e98b8a7166e7fd6b85b423ca9cd94673c961bc9f99926(
    *,
    evaluation_type: CfnServiceLevelObjectivePropsEvaluationType,
    name: builtins.str,
    timeframe: builtins.str,
    description: typing.Optional[builtins.str] = None,
    error_budget_burn_rate: typing.Optional[typing.Union[ErrorBudgetBurnRate, typing.Dict[builtins.str, typing.Any]]] = None,
    filter: typing.Optional[builtins.str] = None,
    has_access: typing.Optional[builtins.bool] = None,
    metric_expression: typing.Optional[builtins.str] = None,
    metric_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[jsii.Number] = None,
    warning: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd1e0e418612b16d97f0e47d8e9d40fbd4d0bdd5a07461590d325c610da41d1(
    *,
    burn_rate_visualization_enabled: builtins.bool,
    fast_burn_threshold: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass
