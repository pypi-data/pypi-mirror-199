# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetObfuscationExpressionResult',
    'AwaitableGetObfuscationExpressionResult',
    'get_obfuscation_expression',
    'get_obfuscation_expression_output',
]

@pulumi.output_type
class GetObfuscationExpressionResult:
    """
    A collection of values returned by getObfuscationExpression.
    """
    def __init__(__self__, account_id=None, id=None, name=None):
        if account_id and not isinstance(account_id, int):
            raise TypeError("Expected argument 'account_id' to be a int")
        pulumi.set(__self__, "account_id", account_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[int]:
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")


class AwaitableGetObfuscationExpressionResult(GetObfuscationExpressionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetObfuscationExpressionResult(
            account_id=self.account_id,
            id=self.id,
            name=self.name)


def get_obfuscation_expression(account_id: Optional[int] = None,
                               name: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetObfuscationExpressionResult:
    """
    Use this data source to get information about a specific Obfuscation Expression in New Relic that already exists.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_newrelic as newrelic

    expression = newrelic.get_obfuscation_expression(account_id=123456,
        name="The expression")
    rule = newrelic.ObfuscationRule("rule",
        description="description of the rule",
        filter="hostStatus=running",
        enabled=True,
        actions=[newrelic.ObfuscationRuleActionArgs(
            attributes=["message"],
            expression_id=expression.id,
            method="MASK",
        )])
    ```


    :param int account_id: The account id associated with the obfuscation expression. If left empty will default to account ID specified in provider level configuration.
    :param str name: Name of expression.
    """
    __args__ = dict()
    __args__['accountId'] = account_id
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('newrelic:index/getObfuscationExpression:getObfuscationExpression', __args__, opts=opts, typ=GetObfuscationExpressionResult).value

    return AwaitableGetObfuscationExpressionResult(
        account_id=__ret__.account_id,
        id=__ret__.id,
        name=__ret__.name)


@_utilities.lift_output_func(get_obfuscation_expression)
def get_obfuscation_expression_output(account_id: Optional[pulumi.Input[Optional[int]]] = None,
                                      name: Optional[pulumi.Input[str]] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetObfuscationExpressionResult]:
    """
    Use this data source to get information about a specific Obfuscation Expression in New Relic that already exists.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_newrelic as newrelic

    expression = newrelic.get_obfuscation_expression(account_id=123456,
        name="The expression")
    rule = newrelic.ObfuscationRule("rule",
        description="description of the rule",
        filter="hostStatus=running",
        enabled=True,
        actions=[newrelic.ObfuscationRuleActionArgs(
            attributes=["message"],
            expression_id=expression.id,
            method="MASK",
        )])
    ```


    :param int account_id: The account id associated with the obfuscation expression. If left empty will default to account ID specified in provider level configuration.
    :param str name: Name of expression.
    """
    ...
