# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AwsLinkAccountArgs', 'AwsLinkAccount']

@pulumi.input_type
class AwsLinkAccountArgs:
    def __init__(__self__, *,
                 arn: pulumi.Input[str],
                 account_id: Optional[pulumi.Input[int]] = None,
                 metric_collection_mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AwsLinkAccount resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the IAM role.
        :param pulumi.Input[int] account_id: The New Relic account ID to operate on.  This allows the user to override the `account_id` attribute set on the provider. Defaults to the environment variable `NEW_RELIC_ACCOUNT_ID`.
        :param pulumi.Input[str] metric_collection_mode: How metrics will be collected. Use `PUSH` for a metric stream or `PULL` to integrate with individual services.
        :param pulumi.Input[str] name: The linked account name
        """
        pulumi.set(__self__, "arn", arn)
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if metric_collection_mode is not None:
            pulumi.set(__self__, "metric_collection_mode", metric_collection_mode)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the IAM role.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[pulumi.Input[int]]:
        """
        The New Relic account ID to operate on.  This allows the user to override the `account_id` attribute set on the provider. Defaults to the environment variable `NEW_RELIC_ACCOUNT_ID`.
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter(name="metricCollectionMode")
    def metric_collection_mode(self) -> Optional[pulumi.Input[str]]:
        """
        How metrics will be collected. Use `PUSH` for a metric stream or `PULL` to integrate with individual services.
        """
        return pulumi.get(self, "metric_collection_mode")

    @metric_collection_mode.setter
    def metric_collection_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metric_collection_mode", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The linked account name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _AwsLinkAccountState:
    def __init__(__self__, *,
                 account_id: Optional[pulumi.Input[int]] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 metric_collection_mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AwsLinkAccount resources.
        :param pulumi.Input[int] account_id: The New Relic account ID to operate on.  This allows the user to override the `account_id` attribute set on the provider. Defaults to the environment variable `NEW_RELIC_ACCOUNT_ID`.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the IAM role.
        :param pulumi.Input[str] metric_collection_mode: How metrics will be collected. Use `PUSH` for a metric stream or `PULL` to integrate with individual services.
        :param pulumi.Input[str] name: The linked account name
        """
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if metric_collection_mode is not None:
            pulumi.set(__self__, "metric_collection_mode", metric_collection_mode)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[pulumi.Input[int]]:
        """
        The New Relic account ID to operate on.  This allows the user to override the `account_id` attribute set on the provider. Defaults to the environment variable `NEW_RELIC_ACCOUNT_ID`.
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the IAM role.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="metricCollectionMode")
    def metric_collection_mode(self) -> Optional[pulumi.Input[str]]:
        """
        How metrics will be collected. Use `PUSH` for a metric stream or `PULL` to integrate with individual services.
        """
        return pulumi.get(self, "metric_collection_mode")

    @metric_collection_mode.setter
    def metric_collection_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metric_collection_mode", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The linked account name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class AwsLinkAccount(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[int]] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 metric_collection_mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Import

        Linked AWS accounts can be imported using the `id`, e.g. bash

        ```sh
         $ pulumi import newrelic:cloud/awsLinkAccount:AwsLinkAccount foo <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] account_id: The New Relic account ID to operate on.  This allows the user to override the `account_id` attribute set on the provider. Defaults to the environment variable `NEW_RELIC_ACCOUNT_ID`.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the IAM role.
        :param pulumi.Input[str] metric_collection_mode: How metrics will be collected. Use `PUSH` for a metric stream or `PULL` to integrate with individual services.
        :param pulumi.Input[str] name: The linked account name
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AwsLinkAccountArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Import

        Linked AWS accounts can be imported using the `id`, e.g. bash

        ```sh
         $ pulumi import newrelic:cloud/awsLinkAccount:AwsLinkAccount foo <id>
        ```

        :param str resource_name: The name of the resource.
        :param AwsLinkAccountArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AwsLinkAccountArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[int]] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 metric_collection_mode: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AwsLinkAccountArgs.__new__(AwsLinkAccountArgs)

            __props__.__dict__["account_id"] = account_id
            if arn is None and not opts.urn:
                raise TypeError("Missing required property 'arn'")
            __props__.__dict__["arn"] = arn
            __props__.__dict__["metric_collection_mode"] = metric_collection_mode
            __props__.__dict__["name"] = name
        super(AwsLinkAccount, __self__).__init__(
            'newrelic:cloud/awsLinkAccount:AwsLinkAccount',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            account_id: Optional[pulumi.Input[int]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            metric_collection_mode: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'AwsLinkAccount':
        """
        Get an existing AwsLinkAccount resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] account_id: The New Relic account ID to operate on.  This allows the user to override the `account_id` attribute set on the provider. Defaults to the environment variable `NEW_RELIC_ACCOUNT_ID`.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the IAM role.
        :param pulumi.Input[str] metric_collection_mode: How metrics will be collected. Use `PUSH` for a metric stream or `PULL` to integrate with individual services.
        :param pulumi.Input[str] name: The linked account name
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AwsLinkAccountState.__new__(_AwsLinkAccountState)

        __props__.__dict__["account_id"] = account_id
        __props__.__dict__["arn"] = arn
        __props__.__dict__["metric_collection_mode"] = metric_collection_mode
        __props__.__dict__["name"] = name
        return AwsLinkAccount(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Output[int]:
        """
        The New Relic account ID to operate on.  This allows the user to override the `account_id` attribute set on the provider. Defaults to the environment variable `NEW_RELIC_ACCOUNT_ID`.
        """
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the IAM role.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="metricCollectionMode")
    def metric_collection_mode(self) -> pulumi.Output[Optional[str]]:
        """
        How metrics will be collected. Use `PUSH` for a metric stream or `PULL` to integrate with individual services.
        """
        return pulumi.get(self, "metric_collection_mode")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The linked account name
        """
        return pulumi.get(self, "name")

