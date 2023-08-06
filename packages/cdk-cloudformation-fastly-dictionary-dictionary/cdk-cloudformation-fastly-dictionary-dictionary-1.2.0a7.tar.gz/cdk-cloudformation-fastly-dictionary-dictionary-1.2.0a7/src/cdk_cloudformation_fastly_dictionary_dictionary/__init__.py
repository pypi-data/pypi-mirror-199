'''
# fastly-dictionary-dictionary

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Fastly::Dictionary::Dictionary` v1.2.0.

## Description

Manage a Fastly service dictionary.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-fastly-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-fastly-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Fastly::Dictionary::Dictionary \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Fastly-Dictionary-Dictionary \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Fastly::Dictionary::Dictionary`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Ffastly-dictionary-dictionary+v1.2.0).
* Issues related to `Fastly::Dictionary::Dictionary` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-fastly-resource-providers).

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


class CfnDictionary(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/fastly-dictionary-dictionary.CfnDictionary",
):
    '''A CloudFormation ``Fastly::Dictionary::Dictionary``.

    :cloudformationResource: Fastly::Dictionary::Dictionary
    :link: https://github.com/aws-ia/cloudformation-fastly-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        service_id: builtins.str,
        version_id: builtins.str,
        deleted_at: typing.Optional[datetime.datetime] = None,
    ) -> None:
        '''Create a new ``Fastly::Dictionary::Dictionary``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: Name for the Dictionary.
        :param service_id: Alphanumeric string identifying the service. Read-only.
        :param version_id: Alphanumeric string identifying the service version.
        :param deleted_at: Date and time in ISO 8601 format.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45500d92fc7cfb3243c2a0665cf58439bd66cb0e2c5df69f5018cf6f9c2241d5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDictionaryProps(
            name=name,
            service_id=service_id,
            version_id=version_id,
            deleted_at=deleted_at,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''Attribute ``Fastly::Dictionary::Dictionary.CreatedAt``.

        :link: https://github.com/aws-ia/cloudformation-fastly-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''Attribute ``Fastly::Dictionary::Dictionary.Id``.

        :link: https://github.com/aws-ia/cloudformation-fastly-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''Attribute ``Fastly::Dictionary::Dictionary.UpdatedAt``.

        :link: https://github.com/aws-ia/cloudformation-fastly-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrVersion")
    def attr_version(self) -> builtins.str:
        '''Attribute ``Fastly::Dictionary::Dictionary.Version``.

        :link: https://github.com/aws-ia/cloudformation-fastly-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVersion"))

    @builtins.property
    @jsii.member(jsii_name="attrWriteOnly")
    def attr_write_only(self) -> _aws_cdk_ceddda9d.IResolvable:
        '''Attribute ``Fastly::Dictionary::Dictionary.WriteOnly``.

        :link: https://github.com/aws-ia/cloudformation-fastly-resource-providers.git
        '''
        return typing.cast(_aws_cdk_ceddda9d.IResolvable, jsii.get(self, "attrWriteOnly"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnDictionaryProps":
        '''Resource props.'''
        return typing.cast("CfnDictionaryProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-dictionary-dictionary.CfnDictionaryProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "service_id": "serviceId",
        "version_id": "versionId",
        "deleted_at": "deletedAt",
    },
)
class CfnDictionaryProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        service_id: builtins.str,
        version_id: builtins.str,
        deleted_at: typing.Optional[datetime.datetime] = None,
    ) -> None:
        '''Manage a Fastly service dictionary.

        :param name: Name for the Dictionary.
        :param service_id: Alphanumeric string identifying the service. Read-only.
        :param version_id: Alphanumeric string identifying the service version.
        :param deleted_at: Date and time in ISO 8601 format.

        :schema: CfnDictionaryProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5bb1ea4afb4308329a455d91b7add20b8adf9049d4928d905bd9b06b1b9631)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_id", value=service_id, expected_type=type_hints["service_id"])
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
            check_type(argname="argument deleted_at", value=deleted_at, expected_type=type_hints["deleted_at"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "service_id": service_id,
            "version_id": version_id,
        }
        if deleted_at is not None:
            self._values["deleted_at"] = deleted_at

    @builtins.property
    def name(self) -> builtins.str:
        '''Name for the Dictionary.

        :schema: CfnDictionaryProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_id(self) -> builtins.str:
        '''Alphanumeric string identifying the service.

        Read-only.

        :schema: CfnDictionaryProps#ServiceId
        '''
        result = self._values.get("service_id")
        assert result is not None, "Required property 'service_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version_id(self) -> builtins.str:
        '''Alphanumeric string identifying the service version.

        :schema: CfnDictionaryProps#VersionId
        '''
        result = self._values.get("version_id")
        assert result is not None, "Required property 'version_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deleted_at(self) -> typing.Optional[datetime.datetime]:
        '''Date and time in ISO 8601 format.

        :schema: CfnDictionaryProps#DeletedAt
        '''
        result = self._values.get("deleted_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDictionaryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDictionary",
    "CfnDictionaryProps",
]

publication.publish()

def _typecheckingstub__45500d92fc7cfb3243c2a0665cf58439bd66cb0e2c5df69f5018cf6f9c2241d5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    service_id: builtins.str,
    version_id: builtins.str,
    deleted_at: typing.Optional[datetime.datetime] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5bb1ea4afb4308329a455d91b7add20b8adf9049d4928d905bd9b06b1b9631(
    *,
    name: builtins.str,
    service_id: builtins.str,
    version_id: builtins.str,
    deleted_at: typing.Optional[datetime.datetime] = None,
) -> None:
    """Type checking stubs"""
    pass
