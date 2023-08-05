# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = ['ServiceLevelArgs', 'ServiceLevel']

@pulumi.input_type
class ServiceLevelArgs:
    def __init__(__self__, *,
                 events: pulumi.Input['ServiceLevelEventsArgs'],
                 guid: pulumi.Input[str],
                 objective: pulumi.Input['ServiceLevelObjectiveArgs'],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ServiceLevel resource.
        :param pulumi.Input['ServiceLevelEventsArgs'] events: The events that define the NRDB data for the SLI/SLO calculations.
               See Events below for details.
        :param pulumi.Input[str] guid: The GUID of the entity (e.g, APM Service, Browser application, Workload, etc.) that you want to relate this SLI to. Note that changing the GUID will force a new resource.
        :param pulumi.Input['ServiceLevelObjectiveArgs'] objective: The objective of the SLI, only one can be defined.
               See Objective below for details.
        :param pulumi.Input[str] description: The description of the SLI.
        :param pulumi.Input[str] name: A short name for the SLI that will help anyone understand what it is about.
        """
        pulumi.set(__self__, "events", events)
        pulumi.set(__self__, "guid", guid)
        pulumi.set(__self__, "objective", objective)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def events(self) -> pulumi.Input['ServiceLevelEventsArgs']:
        """
        The events that define the NRDB data for the SLI/SLO calculations.
        See Events below for details.
        """
        return pulumi.get(self, "events")

    @events.setter
    def events(self, value: pulumi.Input['ServiceLevelEventsArgs']):
        pulumi.set(self, "events", value)

    @property
    @pulumi.getter
    def guid(self) -> pulumi.Input[str]:
        """
        The GUID of the entity (e.g, APM Service, Browser application, Workload, etc.) that you want to relate this SLI to. Note that changing the GUID will force a new resource.
        """
        return pulumi.get(self, "guid")

    @guid.setter
    def guid(self, value: pulumi.Input[str]):
        pulumi.set(self, "guid", value)

    @property
    @pulumi.getter
    def objective(self) -> pulumi.Input['ServiceLevelObjectiveArgs']:
        """
        The objective of the SLI, only one can be defined.
        See Objective below for details.
        """
        return pulumi.get(self, "objective")

    @objective.setter
    def objective(self, value: pulumi.Input['ServiceLevelObjectiveArgs']):
        pulumi.set(self, "objective", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the SLI.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A short name for the SLI that will help anyone understand what it is about.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _ServiceLevelState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 events: Optional[pulumi.Input['ServiceLevelEventsArgs']] = None,
                 guid: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 objective: Optional[pulumi.Input['ServiceLevelObjectiveArgs']] = None,
                 sli_guid: Optional[pulumi.Input[str]] = None,
                 sli_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ServiceLevel resources.
        :param pulumi.Input[str] description: The description of the SLI.
        :param pulumi.Input['ServiceLevelEventsArgs'] events: The events that define the NRDB data for the SLI/SLO calculations.
               See Events below for details.
        :param pulumi.Input[str] guid: The GUID of the entity (e.g, APM Service, Browser application, Workload, etc.) that you want to relate this SLI to. Note that changing the GUID will force a new resource.
        :param pulumi.Input[str] name: A short name for the SLI that will help anyone understand what it is about.
        :param pulumi.Input['ServiceLevelObjectiveArgs'] objective: The objective of the SLI, only one can be defined.
               See Objective below for details.
        :param pulumi.Input[str] sli_guid: The unique entity identifier of the Service Level Indicator in New Relic.
        :param pulumi.Input[str] sli_id: The unique entity identifier of the Service Level Indicator.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if events is not None:
            pulumi.set(__self__, "events", events)
        if guid is not None:
            pulumi.set(__self__, "guid", guid)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if objective is not None:
            pulumi.set(__self__, "objective", objective)
        if sli_guid is not None:
            pulumi.set(__self__, "sli_guid", sli_guid)
        if sli_id is not None:
            pulumi.set(__self__, "sli_id", sli_id)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the SLI.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def events(self) -> Optional[pulumi.Input['ServiceLevelEventsArgs']]:
        """
        The events that define the NRDB data for the SLI/SLO calculations.
        See Events below for details.
        """
        return pulumi.get(self, "events")

    @events.setter
    def events(self, value: Optional[pulumi.Input['ServiceLevelEventsArgs']]):
        pulumi.set(self, "events", value)

    @property
    @pulumi.getter
    def guid(self) -> Optional[pulumi.Input[str]]:
        """
        The GUID of the entity (e.g, APM Service, Browser application, Workload, etc.) that you want to relate this SLI to. Note that changing the GUID will force a new resource.
        """
        return pulumi.get(self, "guid")

    @guid.setter
    def guid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "guid", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A short name for the SLI that will help anyone understand what it is about.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def objective(self) -> Optional[pulumi.Input['ServiceLevelObjectiveArgs']]:
        """
        The objective of the SLI, only one can be defined.
        See Objective below for details.
        """
        return pulumi.get(self, "objective")

    @objective.setter
    def objective(self, value: Optional[pulumi.Input['ServiceLevelObjectiveArgs']]):
        pulumi.set(self, "objective", value)

    @property
    @pulumi.getter(name="sliGuid")
    def sli_guid(self) -> Optional[pulumi.Input[str]]:
        """
        The unique entity identifier of the Service Level Indicator in New Relic.
        """
        return pulumi.get(self, "sli_guid")

    @sli_guid.setter
    def sli_guid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sli_guid", value)

    @property
    @pulumi.getter(name="sliId")
    def sli_id(self) -> Optional[pulumi.Input[str]]:
        """
        The unique entity identifier of the Service Level Indicator.
        """
        return pulumi.get(self, "sli_id")

    @sli_id.setter
    def sli_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sli_id", value)


class ServiceLevel(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 events: Optional[pulumi.Input[pulumi.InputType['ServiceLevelEventsArgs']]] = None,
                 guid: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 objective: Optional[pulumi.Input[pulumi.InputType['ServiceLevelObjectiveArgs']]] = None,
                 __props__=None):
        """
        Use this resource to create, update, and delete New Relic Service Level Indicators and Objectives.

        A New Relic User API key is required to provision this resource.  Set the `api_key`
        attribute in the `provider` block or the `NEW_RELIC_API_KEY` environment
        variable with your User API key.

        Important:
        - Only roles that provide [permissions](https://docs.newrelic.com/docs/accounts/accounts-billing/new-relic-one-user-management/new-relic-one-user-model-understand-user-structure/) to create events to metric rules can create SLI/SLOs.
        - Only [Full users](https://docs.newrelic.com/docs/accounts/accounts-billing/new-relic-one-user-management/new-relic-one-user-model-understand-user-structure/#user-type) can view SLI/SLOs.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_newrelic as newrelic

        foo = newrelic.ServiceLevel("foo",
            description="Proportion of requests that are served faster than a threshold.",
            events=newrelic.ServiceLevelEventsArgs(
                account_id=12345678,
                good_events=newrelic.ServiceLevelEventsGoodEventsArgs(
                    from_="Transaction",
                    where="appName = 'Example application' AND (transactionType= 'Web') AND duration < 0.1",
                ),
                valid_events=newrelic.ServiceLevelEventsValidEventsArgs(
                    from_="Transaction",
                    where="appName = 'Example application' AND (transactionType='Web')",
                ),
            ),
            guid="MXxBUE18QVBQTElDQVRJT058MQ",
            objective=newrelic.ServiceLevelObjectiveArgs(
                target=99,
                time_window=newrelic.ServiceLevelObjectiveTimeWindowArgs(
                    rolling=newrelic.ServiceLevelObjectiveTimeWindowRollingArgs(
                        count=7,
                        unit="DAY",
                    ),
                ),
            ))
        ```
        ## Additional Example

        Service level with tags:

        ```python
        import pulumi
        import pulumi_newrelic as newrelic

        my_synthetic_monitor_service_level = newrelic.ServiceLevel("mySyntheticMonitorServiceLevel",
            guid="MXxBUE18QVBQTElDQVRJT058MQ",
            description="Proportion of successful synthetic checks.",
            events=newrelic.ServiceLevelEventsArgs(
                account_id=12345678,
                valid_events=newrelic.ServiceLevelEventsValidEventsArgs(
                    from_="SyntheticCheck",
                    where="entityGuid = 'MXxBUE18QVBQTElDQVRJT058MQ'",
                ),
                good_events=newrelic.ServiceLevelEventsGoodEventsArgs(
                    from_="SyntheticCheck",
                    where="entityGuid = 'MXxBUE18QVBQTElDQVRJT058MQ' AND result='SUCCESS'",
                ),
            ),
            objective=newrelic.ServiceLevelObjectiveArgs(
                target=99,
                time_window=newrelic.ServiceLevelObjectiveTimeWindowArgs(
                    rolling=newrelic.ServiceLevelObjectiveTimeWindowRollingArgs(
                        count=7,
                        unit="DAY",
                    ),
                ),
            ))
        my_synthetic_monitor_service_level_tags = newrelic.EntityTags("mySyntheticMonitorServiceLevelTags",
            guid=my_synthetic_monitor_service_level.sli_guid,
            tags=[
                newrelic.EntityTagsTagArgs(
                    key="user_journey",
                    values=[
                        "authentication",
                        "sso",
                    ],
                ),
                newrelic.EntityTagsTagArgs(
                    key="owner",
                    values=["identityTeam"],
                ),
            ])
        ```

        For up-to-date documentation about the tagging resource, please check EntityTags

        ## Import

        New Relic Service Levels can be imported using a concatenated string of the format

        `<account_id>:<sli_id>:<guid>`, where the `guid` is the entity the SLI relates to. Examplebash

        ```sh
         $ pulumi import newrelic:index/serviceLevel:ServiceLevel foo 12345678:4321:MXxBUE18QVBQTElDQVRJT058MQ
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the SLI.
        :param pulumi.Input[pulumi.InputType['ServiceLevelEventsArgs']] events: The events that define the NRDB data for the SLI/SLO calculations.
               See Events below for details.
        :param pulumi.Input[str] guid: The GUID of the entity (e.g, APM Service, Browser application, Workload, etc.) that you want to relate this SLI to. Note that changing the GUID will force a new resource.
        :param pulumi.Input[str] name: A short name for the SLI that will help anyone understand what it is about.
        :param pulumi.Input[pulumi.InputType['ServiceLevelObjectiveArgs']] objective: The objective of the SLI, only one can be defined.
               See Objective below for details.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServiceLevelArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Use this resource to create, update, and delete New Relic Service Level Indicators and Objectives.

        A New Relic User API key is required to provision this resource.  Set the `api_key`
        attribute in the `provider` block or the `NEW_RELIC_API_KEY` environment
        variable with your User API key.

        Important:
        - Only roles that provide [permissions](https://docs.newrelic.com/docs/accounts/accounts-billing/new-relic-one-user-management/new-relic-one-user-model-understand-user-structure/) to create events to metric rules can create SLI/SLOs.
        - Only [Full users](https://docs.newrelic.com/docs/accounts/accounts-billing/new-relic-one-user-management/new-relic-one-user-model-understand-user-structure/#user-type) can view SLI/SLOs.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_newrelic as newrelic

        foo = newrelic.ServiceLevel("foo",
            description="Proportion of requests that are served faster than a threshold.",
            events=newrelic.ServiceLevelEventsArgs(
                account_id=12345678,
                good_events=newrelic.ServiceLevelEventsGoodEventsArgs(
                    from_="Transaction",
                    where="appName = 'Example application' AND (transactionType= 'Web') AND duration < 0.1",
                ),
                valid_events=newrelic.ServiceLevelEventsValidEventsArgs(
                    from_="Transaction",
                    where="appName = 'Example application' AND (transactionType='Web')",
                ),
            ),
            guid="MXxBUE18QVBQTElDQVRJT058MQ",
            objective=newrelic.ServiceLevelObjectiveArgs(
                target=99,
                time_window=newrelic.ServiceLevelObjectiveTimeWindowArgs(
                    rolling=newrelic.ServiceLevelObjectiveTimeWindowRollingArgs(
                        count=7,
                        unit="DAY",
                    ),
                ),
            ))
        ```
        ## Additional Example

        Service level with tags:

        ```python
        import pulumi
        import pulumi_newrelic as newrelic

        my_synthetic_monitor_service_level = newrelic.ServiceLevel("mySyntheticMonitorServiceLevel",
            guid="MXxBUE18QVBQTElDQVRJT058MQ",
            description="Proportion of successful synthetic checks.",
            events=newrelic.ServiceLevelEventsArgs(
                account_id=12345678,
                valid_events=newrelic.ServiceLevelEventsValidEventsArgs(
                    from_="SyntheticCheck",
                    where="entityGuid = 'MXxBUE18QVBQTElDQVRJT058MQ'",
                ),
                good_events=newrelic.ServiceLevelEventsGoodEventsArgs(
                    from_="SyntheticCheck",
                    where="entityGuid = 'MXxBUE18QVBQTElDQVRJT058MQ' AND result='SUCCESS'",
                ),
            ),
            objective=newrelic.ServiceLevelObjectiveArgs(
                target=99,
                time_window=newrelic.ServiceLevelObjectiveTimeWindowArgs(
                    rolling=newrelic.ServiceLevelObjectiveTimeWindowRollingArgs(
                        count=7,
                        unit="DAY",
                    ),
                ),
            ))
        my_synthetic_monitor_service_level_tags = newrelic.EntityTags("mySyntheticMonitorServiceLevelTags",
            guid=my_synthetic_monitor_service_level.sli_guid,
            tags=[
                newrelic.EntityTagsTagArgs(
                    key="user_journey",
                    values=[
                        "authentication",
                        "sso",
                    ],
                ),
                newrelic.EntityTagsTagArgs(
                    key="owner",
                    values=["identityTeam"],
                ),
            ])
        ```

        For up-to-date documentation about the tagging resource, please check EntityTags

        ## Import

        New Relic Service Levels can be imported using a concatenated string of the format

        `<account_id>:<sli_id>:<guid>`, where the `guid` is the entity the SLI relates to. Examplebash

        ```sh
         $ pulumi import newrelic:index/serviceLevel:ServiceLevel foo 12345678:4321:MXxBUE18QVBQTElDQVRJT058MQ
        ```

        :param str resource_name: The name of the resource.
        :param ServiceLevelArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServiceLevelArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 events: Optional[pulumi.Input[pulumi.InputType['ServiceLevelEventsArgs']]] = None,
                 guid: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 objective: Optional[pulumi.Input[pulumi.InputType['ServiceLevelObjectiveArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ServiceLevelArgs.__new__(ServiceLevelArgs)

            __props__.__dict__["description"] = description
            if events is None and not opts.urn:
                raise TypeError("Missing required property 'events'")
            __props__.__dict__["events"] = events
            if guid is None and not opts.urn:
                raise TypeError("Missing required property 'guid'")
            __props__.__dict__["guid"] = guid
            __props__.__dict__["name"] = name
            if objective is None and not opts.urn:
                raise TypeError("Missing required property 'objective'")
            __props__.__dict__["objective"] = objective
            __props__.__dict__["sli_guid"] = None
            __props__.__dict__["sli_id"] = None
        super(ServiceLevel, __self__).__init__(
            'newrelic:index/serviceLevel:ServiceLevel',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            events: Optional[pulumi.Input[pulumi.InputType['ServiceLevelEventsArgs']]] = None,
            guid: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            objective: Optional[pulumi.Input[pulumi.InputType['ServiceLevelObjectiveArgs']]] = None,
            sli_guid: Optional[pulumi.Input[str]] = None,
            sli_id: Optional[pulumi.Input[str]] = None) -> 'ServiceLevel':
        """
        Get an existing ServiceLevel resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the SLI.
        :param pulumi.Input[pulumi.InputType['ServiceLevelEventsArgs']] events: The events that define the NRDB data for the SLI/SLO calculations.
               See Events below for details.
        :param pulumi.Input[str] guid: The GUID of the entity (e.g, APM Service, Browser application, Workload, etc.) that you want to relate this SLI to. Note that changing the GUID will force a new resource.
        :param pulumi.Input[str] name: A short name for the SLI that will help anyone understand what it is about.
        :param pulumi.Input[pulumi.InputType['ServiceLevelObjectiveArgs']] objective: The objective of the SLI, only one can be defined.
               See Objective below for details.
        :param pulumi.Input[str] sli_guid: The unique entity identifier of the Service Level Indicator in New Relic.
        :param pulumi.Input[str] sli_id: The unique entity identifier of the Service Level Indicator.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ServiceLevelState.__new__(_ServiceLevelState)

        __props__.__dict__["description"] = description
        __props__.__dict__["events"] = events
        __props__.__dict__["guid"] = guid
        __props__.__dict__["name"] = name
        __props__.__dict__["objective"] = objective
        __props__.__dict__["sli_guid"] = sli_guid
        __props__.__dict__["sli_id"] = sli_id
        return ServiceLevel(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the SLI.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def events(self) -> pulumi.Output['outputs.ServiceLevelEvents']:
        """
        The events that define the NRDB data for the SLI/SLO calculations.
        See Events below for details.
        """
        return pulumi.get(self, "events")

    @property
    @pulumi.getter
    def guid(self) -> pulumi.Output[str]:
        """
        The GUID of the entity (e.g, APM Service, Browser application, Workload, etc.) that you want to relate this SLI to. Note that changing the GUID will force a new resource.
        """
        return pulumi.get(self, "guid")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        A short name for the SLI that will help anyone understand what it is about.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def objective(self) -> pulumi.Output['outputs.ServiceLevelObjective']:
        """
        The objective of the SLI, only one can be defined.
        See Objective below for details.
        """
        return pulumi.get(self, "objective")

    @property
    @pulumi.getter(name="sliGuid")
    def sli_guid(self) -> pulumi.Output[str]:
        """
        The unique entity identifier of the Service Level Indicator in New Relic.
        """
        return pulumi.get(self, "sli_guid")

    @property
    @pulumi.getter(name="sliId")
    def sli_id(self) -> pulumi.Output[str]:
        """
        The unique entity identifier of the Service Level Indicator.
        """
        return pulumi.get(self, "sli_id")

