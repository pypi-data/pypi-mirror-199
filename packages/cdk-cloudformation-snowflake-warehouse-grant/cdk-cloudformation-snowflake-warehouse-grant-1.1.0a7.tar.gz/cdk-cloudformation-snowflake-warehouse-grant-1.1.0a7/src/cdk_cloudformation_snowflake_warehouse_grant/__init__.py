'''
# snowflake-warehouse-grant

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Snowflake::Warehouse::Grant` v1.1.0.

## Description

Allows privileges to be granted on a warehouse to a role. https://docs.snowflake.com/en/sql-reference/sql/grant-privilege.html

## References

* [Documentation](https://github.com/aws-ia/cloudformation-snowflake-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-snowflake-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Snowflake::Warehouse::Grant \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Snowflake-Warehouse-Grant \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Snowflake::Warehouse::Grant`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fsnowflake-warehouse-grant+v1.1.0).
* Issues related to `Snowflake::Warehouse::Grant` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-snowflake-resource-providers).

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
    jsii_type="@cdk-cloudformation/snowflake-warehouse-grant.CfnGrant",
):
    '''A CloudFormation ``Snowflake::Warehouse::Grant``.

    :cloudformationResource: Snowflake::Warehouse::Grant
    :link: https://github.com/aws-ia/cloudformation-snowflake-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        privilege: builtins.str,
        role: builtins.str,
        warehouse_name: builtins.str,
    ) -> None:
        '''Create a new ``Snowflake::Warehouse::Grant``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param privilege: 
        :param role: 
        :param warehouse_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1261b818215942d79ce3da10012bdb14a0f659d30f1704a8970a72e13fda12c0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGrantProps(
            privilege=privilege, role=role, warehouse_name=warehouse_name
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
    jsii_type="@cdk-cloudformation/snowflake-warehouse-grant.CfnGrantProps",
    jsii_struct_bases=[],
    name_mapping={
        "privilege": "privilege",
        "role": "role",
        "warehouse_name": "warehouseName",
    },
)
class CfnGrantProps:
    def __init__(
        self,
        *,
        privilege: builtins.str,
        role: builtins.str,
        warehouse_name: builtins.str,
    ) -> None:
        '''Allows privileges to be granted on a warehouse to a role.

        https://docs.snowflake.com/en/sql-reference/sql/grant-privilege.html

        :param privilege: 
        :param role: 
        :param warehouse_name: 

        :schema: CfnGrantProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bf3006b20b0b99fbc4d55c653ccde4001662715e88aeb66f8fd41ce03e561f5)
            check_type(argname="argument privilege", value=privilege, expected_type=type_hints["privilege"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument warehouse_name", value=warehouse_name, expected_type=type_hints["warehouse_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "privilege": privilege,
            "role": role,
            "warehouse_name": warehouse_name,
        }

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

    @builtins.property
    def warehouse_name(self) -> builtins.str:
        '''
        :schema: CfnGrantProps#WarehouseName
        '''
        result = self._values.get("warehouse_name")
        assert result is not None, "Required property 'warehouse_name' is missing"
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

def _typecheckingstub__1261b818215942d79ce3da10012bdb14a0f659d30f1704a8970a72e13fda12c0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    privilege: builtins.str,
    role: builtins.str,
    warehouse_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bf3006b20b0b99fbc4d55c653ccde4001662715e88aeb66f8fd41ce03e561f5(
    *,
    privilege: builtins.str,
    role: builtins.str,
    warehouse_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
