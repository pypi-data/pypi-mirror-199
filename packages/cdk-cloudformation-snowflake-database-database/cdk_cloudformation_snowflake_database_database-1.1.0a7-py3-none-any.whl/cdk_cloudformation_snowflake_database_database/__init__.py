'''
# snowflake-database-database

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Snowflake::Database::Database` v1.1.0.

## Description

Allows for the creation and modification of a Snowflake Database. https://docs.snowflake.com/en/user-guide/databases.html

## References

* [Documentation](https://github.com/aws-ia/cloudformation-snowflake-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-snowflake-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Snowflake::Database::Database \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Snowflake-Database-Database \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Snowflake::Database::Database`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fsnowflake-database-database+v1.1.0).
* Issues related to `Snowflake::Database::Database` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-snowflake-resource-providers).

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


class CfnDatabase(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/snowflake-database-database.CfnDatabase",
):
    '''A CloudFormation ``Snowflake::Database::Database``.

    :cloudformationResource: Snowflake::Database::Database
    :link: https://github.com/aws-ia/cloudformation-snowflake-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        data_retention_time_in_days: typing.Optional[jsii.Number] = None,
        default_ddl_collation: typing.Optional[builtins.str] = None,
        max_data_extension_time_in_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``Snowflake::Database::Database``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: Specifies the identifier for the database; must be unique for your account.
        :param comment: Specifies a comment for the database.
        :param data_retention_time_in_days: Specifies the number of days for which Time Travel actions can be performed on the database.
        :param default_ddl_collation: Specifies a default collation specification for all schemas and tables added to the database.
        :param max_data_extension_time_in_days: The maximum number of days for which Snowflake can extend the data retention period for tables in the database.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31cb642e1a22cb7e7162afa7958b7d87dbea49872e2ac5309bd86dacff6b961f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDatabaseProps(
            name=name,
            comment=comment,
            data_retention_time_in_days=data_retention_time_in_days,
            default_ddl_collation=default_ddl_collation,
            max_data_extension_time_in_days=max_data_extension_time_in_days,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnDatabaseProps":
        '''Resource props.'''
        return typing.cast("CfnDatabaseProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/snowflake-database-database.CfnDatabaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "comment": "comment",
        "data_retention_time_in_days": "dataRetentionTimeInDays",
        "default_ddl_collation": "defaultDdlCollation",
        "max_data_extension_time_in_days": "maxDataExtensionTimeInDays",
    },
)
class CfnDatabaseProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        data_retention_time_in_days: typing.Optional[jsii.Number] = None,
        default_ddl_collation: typing.Optional[builtins.str] = None,
        max_data_extension_time_in_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Allows for the creation and modification of a Snowflake Database.

        https://docs.snowflake.com/en/user-guide/databases.html

        :param name: Specifies the identifier for the database; must be unique for your account.
        :param comment: Specifies a comment for the database.
        :param data_retention_time_in_days: Specifies the number of days for which Time Travel actions can be performed on the database.
        :param default_ddl_collation: Specifies a default collation specification for all schemas and tables added to the database.
        :param max_data_extension_time_in_days: The maximum number of days for which Snowflake can extend the data retention period for tables in the database.

        :schema: CfnDatabaseProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69305c238f46107d17fb28273d4a2aace25d0e9b5bd59842acc9857270e3fd43)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument data_retention_time_in_days", value=data_retention_time_in_days, expected_type=type_hints["data_retention_time_in_days"])
            check_type(argname="argument default_ddl_collation", value=default_ddl_collation, expected_type=type_hints["default_ddl_collation"])
            check_type(argname="argument max_data_extension_time_in_days", value=max_data_extension_time_in_days, expected_type=type_hints["max_data_extension_time_in_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if comment is not None:
            self._values["comment"] = comment
        if data_retention_time_in_days is not None:
            self._values["data_retention_time_in_days"] = data_retention_time_in_days
        if default_ddl_collation is not None:
            self._values["default_ddl_collation"] = default_ddl_collation
        if max_data_extension_time_in_days is not None:
            self._values["max_data_extension_time_in_days"] = max_data_extension_time_in_days

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the identifier for the database;

        must be unique for your account.

        :schema: CfnDatabaseProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the database.

        :schema: CfnDatabaseProps#Comment
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_retention_time_in_days(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of days for which Time Travel actions can be performed on the database.

        :schema: CfnDatabaseProps#DataRetentionTimeInDays
        '''
        result = self._values.get("data_retention_time_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_ddl_collation(self) -> typing.Optional[builtins.str]:
        '''Specifies a default collation specification for all schemas and tables added to the database.

        :schema: CfnDatabaseProps#DefaultDdlCollation
        '''
        result = self._values.get("default_ddl_collation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_data_extension_time_in_days(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of days for which Snowflake can extend the data retention period for tables in the database.

        :schema: CfnDatabaseProps#MaxDataExtensionTimeInDays
        '''
        result = self._values.get("max_data_extension_time_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatabaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDatabase",
    "CfnDatabaseProps",
]

publication.publish()

def _typecheckingstub__31cb642e1a22cb7e7162afa7958b7d87dbea49872e2ac5309bd86dacff6b961f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    data_retention_time_in_days: typing.Optional[jsii.Number] = None,
    default_ddl_collation: typing.Optional[builtins.str] = None,
    max_data_extension_time_in_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69305c238f46107d17fb28273d4a2aace25d0e9b5bd59842acc9857270e3fd43(
    *,
    name: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    data_retention_time_in_days: typing.Optional[jsii.Number] = None,
    default_ddl_collation: typing.Optional[builtins.str] = None,
    max_data_extension_time_in_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
