'''
# fastly-tls-privatekeys

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Fastly::Tls::PrivateKeys` v1.1.0.

## Description

Manage the Tls Private Key upload

## References

* [Source](https://github.com/aws-ia/cloudformation-fastly-resource-providers)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Fastly::Tls::PrivateKeys \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Fastly-Tls-PrivateKeys \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Fastly::Tls::PrivateKeys`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Ffastly-tls-privatekeys+v1.1.0).
* Issues related to `Fastly::Tls::PrivateKeys` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-fastly-resource-providers).

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


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-tls-privatekeys.Attributes",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "created_at": "createdAt",
        "key_length": "keyLength",
        "key_type": "keyType",
        "name": "name",
        "public_key_sha1": "publicKeySha1",
        "replace": "replace",
    },
)
class Attributes:
    def __init__(
        self,
        *,
        key: builtins.str,
        created_at: typing.Optional[datetime.datetime] = None,
        key_length: typing.Optional[jsii.Number] = None,
        key_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        public_key_sha1: typing.Optional[builtins.str] = None,
        replace: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param key: The contents of the private key. Must be a PEM-formatted key. Not returned in response body.
        :param created_at: 
        :param key_length: 
        :param key_type: 
        :param name: A customizable name for your private key.
        :param public_key_sha1: 
        :param replace: 

        :schema: Attributes
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4140f09d7e2d884781525f7fe3663469c9b652c1168ad18bff1dec9e67b84596)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
            check_type(argname="argument key_length", value=key_length, expected_type=type_hints["key_length"])
            check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument public_key_sha1", value=public_key_sha1, expected_type=type_hints["public_key_sha1"])
            check_type(argname="argument replace", value=replace, expected_type=type_hints["replace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
        }
        if created_at is not None:
            self._values["created_at"] = created_at
        if key_length is not None:
            self._values["key_length"] = key_length
        if key_type is not None:
            self._values["key_type"] = key_type
        if name is not None:
            self._values["name"] = name
        if public_key_sha1 is not None:
            self._values["public_key_sha1"] = public_key_sha1
        if replace is not None:
            self._values["replace"] = replace

    @builtins.property
    def key(self) -> builtins.str:
        '''The contents of the private key.

        Must be a PEM-formatted key. Not returned in response body.

        :schema: Attributes#Key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def created_at(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: Attributes#CreatedAt
        '''
        result = self._values.get("created_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def key_length(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: Attributes#KeyLength
        '''
        result = self._values.get("key_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def key_type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Attributes#KeyType
        '''
        result = self._values.get("key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A customizable name for your private key.

        :schema: Attributes#Name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_key_sha1(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Attributes#PublicKeySha1
        '''
        result = self._values.get("public_key_sha1")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replace(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: Attributes#Replace
        '''
        result = self._values.get("replace")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Attributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfnPrivateKeys(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/fastly-tls-privatekeys.CfnPrivateKeys",
):
    '''A CloudFormation ``Fastly::Tls::PrivateKeys``.

    :cloudformationResource: Fastly::Tls::PrivateKeys
    :link: https://github.com/aws-ia/cloudformation-fastly-resource-providers
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        attributes: typing.Union[Attributes, typing.Dict[builtins.str, typing.Any]],
        type: typing.Optional["CfnPrivateKeysPropsType"] = None,
    ) -> None:
        '''Create a new ``Fastly::Tls::PrivateKeys``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param attributes: 
        :param type: Resource type. [Default tls_private_key]
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa913f94c6358009be024d61b88afe87a3c5af65e9376ce87a2b0b7f4f47841a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPrivateKeysProps(attributes=attributes, type=type)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''Attribute ``Fastly::Tls::PrivateKeys.Id``.

        :link: https://github.com/aws-ia/cloudformation-fastly-resource-providers
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnPrivateKeysProps":
        '''Resource props.'''
        return typing.cast("CfnPrivateKeysProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-tls-privatekeys.CfnPrivateKeysProps",
    jsii_struct_bases=[],
    name_mapping={"attributes": "attributes", "type": "type"},
)
class CfnPrivateKeysProps:
    def __init__(
        self,
        *,
        attributes: typing.Union[Attributes, typing.Dict[builtins.str, typing.Any]],
        type: typing.Optional["CfnPrivateKeysPropsType"] = None,
    ) -> None:
        '''Manage the Tls Private Key upload.

        :param attributes: 
        :param type: Resource type. [Default tls_private_key]

        :schema: CfnPrivateKeysProps
        '''
        if isinstance(attributes, dict):
            attributes = Attributes(**attributes)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c333788f43786281545150522ed0ceac69f48b0ca91c12dc4e5ca4c2fbd1ec1a)
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attributes": attributes,
        }
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def attributes(self) -> Attributes:
        '''
        :schema: CfnPrivateKeysProps#Attributes
        '''
        result = self._values.get("attributes")
        assert result is not None, "Required property 'attributes' is missing"
        return typing.cast(Attributes, result)

    @builtins.property
    def type(self) -> typing.Optional["CfnPrivateKeysPropsType"]:
        '''Resource type.

        [Default tls_private_key]

        :schema: CfnPrivateKeysProps#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional["CfnPrivateKeysPropsType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPrivateKeysProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/fastly-tls-privatekeys.CfnPrivateKeysPropsType"
)
class CfnPrivateKeysPropsType(enum.Enum):
    '''Resource type.

    [Default tls_private_key]

    :schema: CfnPrivateKeysPropsType
    '''

    TLS_PRIVATE_KEY = "TLS_PRIVATE_KEY"
    '''tls_private_key.'''


__all__ = [
    "Attributes",
    "CfnPrivateKeys",
    "CfnPrivateKeysProps",
    "CfnPrivateKeysPropsType",
]

publication.publish()

def _typecheckingstub__4140f09d7e2d884781525f7fe3663469c9b652c1168ad18bff1dec9e67b84596(
    *,
    key: builtins.str,
    created_at: typing.Optional[datetime.datetime] = None,
    key_length: typing.Optional[jsii.Number] = None,
    key_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    public_key_sha1: typing.Optional[builtins.str] = None,
    replace: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa913f94c6358009be024d61b88afe87a3c5af65e9376ce87a2b0b7f4f47841a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    attributes: typing.Union[Attributes, typing.Dict[builtins.str, typing.Any]],
    type: typing.Optional[CfnPrivateKeysPropsType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c333788f43786281545150522ed0ceac69f48b0ca91c12dc4e5ca4c2fbd1ec1a(
    *,
    attributes: typing.Union[Attributes, typing.Dict[builtins.str, typing.Any]],
    type: typing.Optional[CfnPrivateKeysPropsType] = None,
) -> None:
    """Type checking stubs"""
    pass
