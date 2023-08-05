'''
# SNS Notification OpsGenie

This repository contains construct which can be used for sns notify to Opsgenie.
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

import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="sns-notify-opsgenie.Priority")
class Priority(enum.Enum):
    '''Enumeration of priority for Alarms.

    The ``Priority`` enum is used to represent the priority of an Alarm. It has five possible values.
    '''

    CRITICAL = "CRITICAL"
    '''indicates that the alarm is of the highest priority and requires immediate attention.'''
    HIGH = "HIGH"
    '''indicates that the alarm is of high priority and should be addressed as soon as possible.'''
    MEDIUM = "MEDIUM"
    '''indicates that the alarm is of medium priority and can be addressed in due course.'''
    LOW = "LOW"
    '''indicates that the alarm is of low priority and can be addressed at a later time.'''
    INFORMATION = "INFORMATION"
    '''indicates that the alarm is of the lowest priority and can be addressed at a later time.'''


class SnsNotifyOpsgenie(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="sns-notify-opsgenie.SnsNotifyOpsgenie",
):
    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__576d8dcbc853a1094b106e5ca48650388092147be3d1129811d5db36a41ebe12)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="getOpgsgenieTopicArn")
    def get_opgsgenie_topic_arn(
        self,
        account_id: builtins.str,
        priority: Priority,
        region: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_sns_ceddda9d.ITopic:
        '''Returns an sns.Topic object that represents an SNS topic in AWS. The topic ARN is constructed based on the accountId, priority, and region parameters.

        :param account_id: The AWS account ID where the topic is located.
        :param priority: The priority of the topic. Must be one of
        :param region: The AWS region where the topic is located. If not specified, defaults to eu-west-1.

        :return: An sns.Topic object that represents an SNS topic in AWS.

        :enum: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__502a3957945dfc250baea5cb9ddf63e398b7aed6927eebb43c4109c0ca85c7f0)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        return typing.cast(_aws_cdk_aws_sns_ceddda9d.ITopic, jsii.invoke(self, "getOpgsgenieTopicArn", [account_id, priority, region]))


__all__ = [
    "Priority",
    "SnsNotifyOpsgenie",
]

publication.publish()

def _typecheckingstub__576d8dcbc853a1094b106e5ca48650388092147be3d1129811d5db36a41ebe12(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__502a3957945dfc250baea5cb9ddf63e398b7aed6927eebb43c4109c0ca85c7f0(
    account_id: builtins.str,
    priority: Priority,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
