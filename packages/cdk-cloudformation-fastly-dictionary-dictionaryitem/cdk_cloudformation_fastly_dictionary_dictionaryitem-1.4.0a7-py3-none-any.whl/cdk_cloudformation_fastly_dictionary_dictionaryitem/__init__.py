'''
# fastly-dictionary-dictionaryitem

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Fastly::Dictionary::DictionaryItem` v1.4.0.

## Description

Manage a Fastly service dictionary item.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-fastly-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-fastly-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Fastly::Dictionary::DictionaryItem \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Fastly-Dictionary-DictionaryItem \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Fastly::Dictionary::DictionaryItem`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Ffastly-dictionary-dictionaryitem+v1.4.0).
* Issues related to `Fastly::Dictionary::DictionaryItem` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-fastly-resource-providers).

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


class CfnDictionaryItem(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/fastly-dictionary-dictionaryitem.CfnDictionaryItem",
):
    '''A CloudFormation ``Fastly::Dictionary::DictionaryItem``.

    :cloudformationResource: Fastly::Dictionary::DictionaryItem
    :link: https://github.com/aws-ia/cloudformation-fastly-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        dictionary_id: builtins.str,
        item_key: builtins.str,
        service_id: builtins.str,
        item_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``Fastly::Dictionary::DictionaryItem``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param dictionary_id: Alphanumeric string identifying a Dictionary.
        :param item_key: Item key.
        :param service_id: Alphanumeric string identifying the service. Read-only.
        :param item_value: Item key.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fdb3701578eb8614d0e9c0b9627d309d7768faa786fcb7a6fc18c233ed0ac92)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDictionaryItemProps(
            dictionary_id=dictionary_id,
            item_key=item_key,
            service_id=service_id,
            item_value=item_value,
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
        '''Attribute ``Fastly::Dictionary::DictionaryItem.CreatedAt``.

        :link: https://github.com/aws-ia/cloudformation-fastly-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrDeletedAt")
    def attr_deleted_at(self) -> builtins.str:
        '''Attribute ``Fastly::Dictionary::DictionaryItem.DeletedAt``.

        :link: https://github.com/aws-ia/cloudformation-fastly-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDeletedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''Attribute ``Fastly::Dictionary::DictionaryItem.UpdatedAt``.

        :link: https://github.com/aws-ia/cloudformation-fastly-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnDictionaryItemProps":
        '''Resource props.'''
        return typing.cast("CfnDictionaryItemProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-dictionary-dictionaryitem.CfnDictionaryItemProps",
    jsii_struct_bases=[],
    name_mapping={
        "dictionary_id": "dictionaryId",
        "item_key": "itemKey",
        "service_id": "serviceId",
        "item_value": "itemValue",
    },
)
class CfnDictionaryItemProps:
    def __init__(
        self,
        *,
        dictionary_id: builtins.str,
        item_key: builtins.str,
        service_id: builtins.str,
        item_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Manage a Fastly service dictionary item.

        :param dictionary_id: Alphanumeric string identifying a Dictionary.
        :param item_key: Item key.
        :param service_id: Alphanumeric string identifying the service. Read-only.
        :param item_value: Item key.

        :schema: CfnDictionaryItemProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54242e47fc5af8c6a0fbd26fa980b6fd40bba65cc7390b89c98a2112b5fa6e72)
            check_type(argname="argument dictionary_id", value=dictionary_id, expected_type=type_hints["dictionary_id"])
            check_type(argname="argument item_key", value=item_key, expected_type=type_hints["item_key"])
            check_type(argname="argument service_id", value=service_id, expected_type=type_hints["service_id"])
            check_type(argname="argument item_value", value=item_value, expected_type=type_hints["item_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dictionary_id": dictionary_id,
            "item_key": item_key,
            "service_id": service_id,
        }
        if item_value is not None:
            self._values["item_value"] = item_value

    @builtins.property
    def dictionary_id(self) -> builtins.str:
        '''Alphanumeric string identifying a Dictionary.

        :schema: CfnDictionaryItemProps#DictionaryId
        '''
        result = self._values.get("dictionary_id")
        assert result is not None, "Required property 'dictionary_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def item_key(self) -> builtins.str:
        '''Item key.

        :schema: CfnDictionaryItemProps#ItemKey
        '''
        result = self._values.get("item_key")
        assert result is not None, "Required property 'item_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_id(self) -> builtins.str:
        '''Alphanumeric string identifying the service.

        Read-only.

        :schema: CfnDictionaryItemProps#ServiceId
        '''
        result = self._values.get("service_id")
        assert result is not None, "Required property 'service_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def item_value(self) -> typing.Optional[builtins.str]:
        '''Item key.

        :schema: CfnDictionaryItemProps#ItemValue
        '''
        result = self._values.get("item_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDictionaryItemProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDictionaryItem",
    "CfnDictionaryItemProps",
]

publication.publish()

def _typecheckingstub__9fdb3701578eb8614d0e9c0b9627d309d7768faa786fcb7a6fc18c233ed0ac92(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    dictionary_id: builtins.str,
    item_key: builtins.str,
    service_id: builtins.str,
    item_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54242e47fc5af8c6a0fbd26fa980b6fd40bba65cc7390b89c98a2112b5fa6e72(
    *,
    dictionary_id: builtins.str,
    item_key: builtins.str,
    service_id: builtins.str,
    item_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
