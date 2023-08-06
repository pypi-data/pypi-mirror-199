'''
# fastly-services-service

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Fastly::Services::Service` v1.2.0.

## Description

Manage a Fastly service.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-fastly-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-fastly-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Fastly::Services::Service \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Fastly-Services-Service \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Fastly::Services::Service`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Ffastly-services-service+v1.2.0).
* Issues related to `Fastly::Services::Service` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-fastly-resource-providers).

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


class CfnService(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/fastly-services-service.CfnService",
):
    '''A CloudFormation ``Fastly::Services::Service``.

    :cloudformationResource: Fastly::Services::Service
    :link: https://github.com/aws-ia/cloudformation-fastly-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        created_at: typing.Optional[datetime.datetime] = None,
        customer_id: typing.Optional[builtins.str] = None,
        deleted_at: typing.Optional[datetime.datetime] = None,
        id: typing.Optional[builtins.str] = None,
        paused: typing.Optional[builtins.bool] = None,
        type: typing.Optional["Type"] = None,
        updated_at: typing.Optional[datetime.datetime] = None,
    ) -> None:
        '''Create a new ``Fastly::Services::Service``.

        :param scope: - scope in which this resource is defined.
        :param id_: - scoped id of the resource.
        :param name: 
        :param comment: 
        :param created_at: 
        :param customer_id: 
        :param deleted_at: 
        :param id: 
        :param paused: 
        :param type: 
        :param updated_at: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca1b7399c4b5f2f0d3843ef0f9e125020ac7985edeaa55bd226f821e4b9e23b3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        props = CfnServiceProps(
            name=name,
            comment=comment,
            created_at=created_at,
            customer_id=customer_id,
            deleted_at=deleted_at,
            id=id,
            paused=paused,
            type=type,
            updated_at=updated_at,
        )

        jsii.create(self.__class__, self, [scope, id_, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrActiveVersionId")
    def attr_active_version_id(self) -> builtins.str:
        '''Attribute ``Fastly::Services::Service.ActiveVersionId``.

        :link: https://github.com/aws-ia/cloudformation-fastly-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrActiveVersionId"))

    @builtins.property
    @jsii.member(jsii_name="attrLatestVersionId")
    def attr_latest_version_id(self) -> builtins.str:
        '''Attribute ``Fastly::Services::Service.LatestVersionId``.

        :link: https://github.com/aws-ia/cloudformation-fastly-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLatestVersionId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnServiceProps":
        '''Resource props.'''
        return typing.cast("CfnServiceProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-services-service.CfnServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "comment": "comment",
        "created_at": "createdAt",
        "customer_id": "customerId",
        "deleted_at": "deletedAt",
        "id": "id",
        "paused": "paused",
        "type": "type",
        "updated_at": "updatedAt",
    },
)
class CfnServiceProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        created_at: typing.Optional[datetime.datetime] = None,
        customer_id: typing.Optional[builtins.str] = None,
        deleted_at: typing.Optional[datetime.datetime] = None,
        id: typing.Optional[builtins.str] = None,
        paused: typing.Optional[builtins.bool] = None,
        type: typing.Optional["Type"] = None,
        updated_at: typing.Optional[datetime.datetime] = None,
    ) -> None:
        '''Manage a Fastly service.

        :param name: 
        :param comment: 
        :param created_at: 
        :param customer_id: 
        :param deleted_at: 
        :param id: 
        :param paused: 
        :param type: 
        :param updated_at: 

        :schema: CfnServiceProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93dc9cc3207904a805fbe08dab6d92b988e3ee5944120b1054628b534d96261a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
            check_type(argname="argument customer_id", value=customer_id, expected_type=type_hints["customer_id"])
            check_type(argname="argument deleted_at", value=deleted_at, expected_type=type_hints["deleted_at"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument paused", value=paused, expected_type=type_hints["paused"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if comment is not None:
            self._values["comment"] = comment
        if created_at is not None:
            self._values["created_at"] = created_at
        if customer_id is not None:
            self._values["customer_id"] = customer_id
        if deleted_at is not None:
            self._values["deleted_at"] = deleted_at
        if id is not None:
            self._values["id"] = id
        if paused is not None:
            self._values["paused"] = paused
        if type is not None:
            self._values["type"] = type
        if updated_at is not None:
            self._values["updated_at"] = updated_at

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :schema: CfnServiceProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnServiceProps#Comment
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def created_at(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: CfnServiceProps#CreatedAt
        '''
        result = self._values.get("created_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def customer_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnServiceProps#CustomerId
        '''
        result = self._values.get("customer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deleted_at(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: CfnServiceProps#DeletedAt
        '''
        result = self._values.get("deleted_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnServiceProps#Id
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def paused(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnServiceProps#Paused
        '''
        result = self._values.get("paused")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def type(self) -> typing.Optional["Type"]:
        '''
        :schema: CfnServiceProps#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional["Type"], result)

    @builtins.property
    def updated_at(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: CfnServiceProps#UpdatedAt
        '''
        result = self._values.get("updated_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/fastly-services-service.Type")
class Type(enum.Enum):
    '''The type of this service.

    :schema: Type
    '''

    VCL = "VCL"
    '''vcl.'''
    WASM = "WASM"
    '''wasm.'''


__all__ = [
    "CfnService",
    "CfnServiceProps",
    "Type",
]

publication.publish()

def _typecheckingstub__ca1b7399c4b5f2f0d3843ef0f9e125020ac7985edeaa55bd226f821e4b9e23b3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    created_at: typing.Optional[datetime.datetime] = None,
    customer_id: typing.Optional[builtins.str] = None,
    deleted_at: typing.Optional[datetime.datetime] = None,
    id: typing.Optional[builtins.str] = None,
    paused: typing.Optional[builtins.bool] = None,
    type: typing.Optional[Type] = None,
    updated_at: typing.Optional[datetime.datetime] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93dc9cc3207904a805fbe08dab6d92b988e3ee5944120b1054628b534d96261a(
    *,
    name: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    created_at: typing.Optional[datetime.datetime] = None,
    customer_id: typing.Optional[builtins.str] = None,
    deleted_at: typing.Optional[datetime.datetime] = None,
    id: typing.Optional[builtins.str] = None,
    paused: typing.Optional[builtins.bool] = None,
    type: typing.Optional[Type] = None,
    updated_at: typing.Optional[datetime.datetime] = None,
) -> None:
    """Type checking stubs"""
    pass
