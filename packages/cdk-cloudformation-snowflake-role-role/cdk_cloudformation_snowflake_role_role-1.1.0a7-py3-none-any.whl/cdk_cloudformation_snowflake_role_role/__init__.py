'''
# snowflake-role-role

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Snowflake::Role::Role` v1.1.0.

## Description

Allows for the creation and modification of a Snowflake Role. https://docs.snowflake.com/en/user-guide/security-access-control-overview.html#roles

## References

* [Documentation](https://github.com/aws-ia/cloudformation-snowflake-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-snowflake-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Snowflake::Role::Role \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Snowflake-Role-Role \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Snowflake::Role::Role`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fsnowflake-role-role+v1.1.0).
* Issues related to `Snowflake::Role::Role` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-snowflake-resource-providers).

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


class CfnRole(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/snowflake-role-role.CfnRole",
):
    '''A CloudFormation ``Snowflake::Role::Role``.

    :cloudformationResource: Snowflake::Role::Role
    :link: https://github.com/aws-ia/cloudformation-snowflake-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        comment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``Snowflake::Role::Role``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: Specifies the identifier for the role; must be unique for your account.
        :param comment: Specifies a comment for the role.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d519208bbb777191dd8c729a7b7f6e5197ef96f57ff0ee00e269138abd52888)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRoleProps(name=name, comment=comment)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnRoleProps":
        '''Resource props.'''
        return typing.cast("CfnRoleProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/snowflake-role-role.CfnRoleProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "comment": "comment"},
)
class CfnRoleProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        comment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Allows for the creation and modification of a Snowflake Role.

        https://docs.snowflake.com/en/user-guide/security-access-control-overview.html#roles

        :param name: Specifies the identifier for the role; must be unique for your account.
        :param comment: Specifies a comment for the role.

        :schema: CfnRoleProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400fb4fedf6f36bee44b922e91a7329023c6d4f259a0e569919a3ddb4685fbad)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if comment is not None:
            self._values["comment"] = comment

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the identifier for the role;

        must be unique for your account.

        :schema: CfnRoleProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the role.

        :schema: CfnRoleProps#Comment
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnRole",
    "CfnRoleProps",
]

publication.publish()

def _typecheckingstub__3d519208bbb777191dd8c729a7b7f6e5197ef96f57ff0ee00e269138abd52888(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    comment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400fb4fedf6f36bee44b922e91a7329023c6d4f259a0e569919a3ddb4685fbad(
    *,
    name: builtins.str,
    comment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
