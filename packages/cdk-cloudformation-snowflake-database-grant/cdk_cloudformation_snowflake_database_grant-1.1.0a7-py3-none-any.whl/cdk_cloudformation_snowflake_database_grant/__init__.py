'''
# snowflake-database-grant

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Snowflake::Database::Grant` v1.1.0.

## Description

Allows privileges to be granted on a database to a role. https://docs.snowflake.com/en/sql-reference/sql/grant-privilege.html

## References

* [Documentation](https://github.com/aws-ia/cloudformation-snowflake-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-snowflake-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Snowflake::Database::Grant \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Snowflake-Database-Grant \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Snowflake::Database::Grant`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fsnowflake-database-grant+v1.1.0).
* Issues related to `Snowflake::Database::Grant` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-snowflake-resource-providers).

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
    jsii_type="@cdk-cloudformation/snowflake-database-grant.CfnGrant",
):
    '''A CloudFormation ``Snowflake::Database::Grant``.

    :cloudformationResource: Snowflake::Database::Grant
    :link: https://github.com/aws-ia/cloudformation-snowflake-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        database_name: builtins.str,
        privilege: builtins.str,
        role: builtins.str,
    ) -> None:
        '''Create a new ``Snowflake::Database::Grant``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param database_name: 
        :param privilege: 
        :param role: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__137a2d8157a1b2c2f0622105f30d13edc8e8fa8e7c4b53d19a00dfb7a7b5fdee)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGrantProps(
            database_name=database_name, privilege=privilege, role=role
        )

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
    jsii_type="@cdk-cloudformation/snowflake-database-grant.CfnGrantProps",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "privilege": "privilege",
        "role": "role",
    },
)
class CfnGrantProps:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        privilege: builtins.str,
        role: builtins.str,
    ) -> None:
        '''Allows privileges to be granted on a database to a role.

        https://docs.snowflake.com/en/sql-reference/sql/grant-privilege.html

        :param database_name: 
        :param privilege: 
        :param role: 

        :schema: CfnGrantProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579b38a5b4d22513c896beffa6e9e144bfc94aca08cac3d5ce44dea40fcb786b)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument privilege", value=privilege, expected_type=type_hints["privilege"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
            "privilege": privilege,
            "role": role,
        }

    @builtins.property
    def database_name(self) -> builtins.str:
        '''
        :schema: CfnGrantProps#DatabaseName
        '''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def privilege(self) -> builtins.str:
        '''
        :schema: CfnGrantProps#Privilege
        '''
        result = self._values.get("privilege")
        assert result is not None, "Required property 'privilege' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> builtins.str:
        '''
        :schema: CfnGrantProps#Role
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
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

def _typecheckingstub__137a2d8157a1b2c2f0622105f30d13edc8e8fa8e7c4b53d19a00dfb7a7b5fdee(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    database_name: builtins.str,
    privilege: builtins.str,
    role: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579b38a5b4d22513c896beffa6e9e144bfc94aca08cac3d5ce44dea40fcb786b(
    *,
    database_name: builtins.str,
    privilege: builtins.str,
    role: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
