'''
# snowflake-role-grant

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Snowflake::Role::Grant` v1.1.0.

## Description

Allows privileges to be granted on a role to a user. https://docs.snowflake.com/en/sql-reference/sql/grant-privilege.html

## References

* [Documentation](https://github.com/aws-ia/cloudformation-snowflake-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-snowflake-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Snowflake::Role::Grant \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Snowflake-Role-Grant \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Snowflake::Role::Grant`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fsnowflake-role-grant+v1.1.0).
* Issues related to `Snowflake::Role::Grant` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-snowflake-resource-providers).

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


class CfnGrant(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/snowflake-role-grant.CfnGrant",
):
    '''A CloudFormation ``Snowflake::Role::Grant``.

    :cloudformationResource: Snowflake::Role::Grant
    :link: https://github.com/aws-ia/cloudformation-snowflake-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        role_name: builtins.str,
        user: builtins.str,
    ) -> None:
        '''Create a new ``Snowflake::Role::Grant``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param role_name: 
        :param user: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f5560d1e5e3a13b99fcbcc30d0c2bef9883084058923497511976106f1d801a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGrantProps(role_name=role_name, user=user)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnGrantProps":
        '''Resource props.'''
        return typing.cast("CfnGrantProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/snowflake-role-grant.CfnGrantProps",
    jsii_struct_bases=[],
    name_mapping={"role_name": "roleName", "user": "user"},
)
class CfnGrantProps:
    def __init__(self, *, role_name: builtins.str, user: builtins.str) -> None:
        '''Allows privileges to be granted on a role to a user.

        https://docs.snowflake.com/en/sql-reference/sql/grant-privilege.html

        :param role_name: 
        :param user: 

        :schema: CfnGrantProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3284c33e8b03349966f892ab5b9b00e99096bc498130043ab3a6190912d92fa)
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_name": role_name,
            "user": user,
        }

    @builtins.property
    def role_name(self) -> builtins.str:
        '''
        :schema: CfnGrantProps#RoleName
        '''
        result = self._values.get("role_name")
        assert result is not None, "Required property 'role_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user(self) -> builtins.str:
        '''
        :schema: CfnGrantProps#User
        '''
        result = self._values.get("user")
        assert result is not None, "Required property 'user' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGrantProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnGrant",
    "CfnGrantProps",
]

publication.publish()

def _typecheckingstub__0f5560d1e5e3a13b99fcbcc30d0c2bef9883084058923497511976106f1d801a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    role_name: builtins.str,
    user: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3284c33e8b03349966f892ab5b9b00e99096bc498130043ab3a6190912d92fa(
    *,
    role_name: builtins.str,
    user: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
