'''
# fastly-services-domain

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Fastly::Services::Domain` v1.2.0.

## Description

Manage a Fastly service domain.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-fastly-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-fastly-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Fastly::Services::Domain \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Fastly-Services-Domain \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Fastly::Services::Domain`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Ffastly-services-domain+v1.2.0).
* Issues related to `Fastly::Services::Domain` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-fastly-resource-providers).

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


class CfnDomain(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/fastly-services-domain.CfnDomain",
):
    '''A CloudFormation ``Fastly::Services::Domain``.

    :cloudformationResource: Fastly::Services::Domain
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
        comment: typing.Optional[builtins.str] = None,
        created_at: typing.Optional[datetime.datetime] = None,
        deleted_at: typing.Optional[datetime.datetime] = None,
        domain_name: typing.Optional[builtins.str] = None,
        updated_at: typing.Optional[datetime.datetime] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``Fastly::Services::Domain``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: 
        :param service_id: 
        :param version_id: 
        :param comment: 
        :param created_at: 
        :param deleted_at: 
        :param domain_name: 
        :param updated_at: 
        :param version: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ecc58ed5375cf1aa8ab5f97d04b3d35cb931520d8e4b9478c69206bf527c77)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDomainProps(
            name=name,
            service_id=service_id,
            version_id=version_id,
            comment=comment,
            created_at=created_at,
            deleted_at=deleted_at,
            domain_name=domain_name,
            updated_at=updated_at,
            version=version,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnDomainProps":
        '''Resource props.'''
        return typing.cast("CfnDomainProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-services-domain.CfnDomainProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "service_id": "serviceId",
        "version_id": "versionId",
        "comment": "comment",
        "created_at": "createdAt",
        "deleted_at": "deletedAt",
        "domain_name": "domainName",
        "updated_at": "updatedAt",
        "version": "version",
    },
)
class CfnDomainProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        service_id: builtins.str,
        version_id: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        created_at: typing.Optional[datetime.datetime] = None,
        deleted_at: typing.Optional[datetime.datetime] = None,
        domain_name: typing.Optional[builtins.str] = None,
        updated_at: typing.Optional[datetime.datetime] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Manage a Fastly service domain.

        :param name: 
        :param service_id: 
        :param version_id: 
        :param comment: 
        :param created_at: 
        :param deleted_at: 
        :param domain_name: 
        :param updated_at: 
        :param version: 

        :schema: CfnDomainProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c7f119958b7fecc973cb67c19ae3538ad24f98bf83d16fb01994370e9789b23)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_id", value=service_id, expected_type=type_hints["service_id"])
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
            check_type(argname="argument deleted_at", value=deleted_at, expected_type=type_hints["deleted_at"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "service_id": service_id,
            "version_id": version_id,
        }
        if comment is not None:
            self._values["comment"] = comment
        if created_at is not None:
            self._values["created_at"] = created_at
        if deleted_at is not None:
            self._values["deleted_at"] = deleted_at
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if updated_at is not None:
            self._values["updated_at"] = updated_at
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :schema: CfnDomainProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_id(self) -> builtins.str:
        '''
        :schema: CfnDomainProps#ServiceId
        '''
        result = self._values.get("service_id")
        assert result is not None, "Required property 'service_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version_id(self) -> builtins.str:
        '''
        :schema: CfnDomainProps#VersionId
        '''
        result = self._values.get("version_id")
        assert result is not None, "Required property 'version_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDomainProps#Comment
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def created_at(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: CfnDomainProps#CreatedAt
        '''
        result = self._values.get("created_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def deleted_at(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: CfnDomainProps#DeletedAt
        '''
        result = self._values.get("deleted_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDomainProps#DomainName
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def updated_at(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: CfnDomainProps#UpdatedAt
        '''
        result = self._values.get("updated_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDomainProps#Version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDomain",
    "CfnDomainProps",
]

publication.publish()

def _typecheckingstub__b2ecc58ed5375cf1aa8ab5f97d04b3d35cb931520d8e4b9478c69206bf527c77(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    service_id: builtins.str,
    version_id: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    created_at: typing.Optional[datetime.datetime] = None,
    deleted_at: typing.Optional[datetime.datetime] = None,
    domain_name: typing.Optional[builtins.str] = None,
    updated_at: typing.Optional[datetime.datetime] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c7f119958b7fecc973cb67c19ae3538ad24f98bf83d16fb01994370e9789b23(
    *,
    name: builtins.str,
    service_id: builtins.str,
    version_id: builtins.str,
    comment: typing.Optional[builtins.str] = None,
    created_at: typing.Optional[datetime.datetime] = None,
    deleted_at: typing.Optional[datetime.datetime] = None,
    domain_name: typing.Optional[builtins.str] = None,
    updated_at: typing.Optional[datetime.datetime] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
