'''
# fastly-tls-domain

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Fastly::Tls::Domain` v1.1.0.

## Description

Manage the activation of a Tls Domain

## References

* [Source](https://github.com/aws-ia/cloudformation-fastly-resource-providers)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Fastly::Tls::Domain \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Fastly-Tls-Domain \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Fastly::Tls::Domain`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Ffastly-tls-domain+v1.1.0).
* Issues related to `Fastly::Tls::Domain` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-fastly-resource-providers).

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
    jsii_type="@cdk-cloudformation/fastly-tls-domain.CfnDomain",
):
    '''A CloudFormation ``Fastly::Tls::Domain``.

    :cloudformationResource: Fastly::Tls::Domain
    :link: https://github.com/aws-ia/cloudformation-fastly-resource-providers
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        attributes: typing.Optional[typing.Union["CfnDomainPropsAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
        relationships: typing.Optional[typing.Union["Relationships", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``Fastly::Tls::Domain``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param attributes: 
        :param relationships: 
        :param type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d33f617034c88672704708d06c11431b4d83617306a58da809c1f4d364a70a5d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDomainProps(
            attributes=attributes, relationships=relationships, type=type
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''Attribute ``Fastly::Tls::Domain.Id``.

        :link: https://github.com/aws-ia/cloudformation-fastly-resource-providers
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnDomainProps":
        '''Resource props.'''
        return typing.cast("CfnDomainProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-tls-domain.CfnDomainProps",
    jsii_struct_bases=[],
    name_mapping={
        "attributes": "attributes",
        "relationships": "relationships",
        "type": "type",
    },
)
class CfnDomainProps:
    def __init__(
        self,
        *,
        attributes: typing.Optional[typing.Union["CfnDomainPropsAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
        relationships: typing.Optional[typing.Union["Relationships", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Manage the activation of a Tls Domain.

        :param attributes: 
        :param relationships: 
        :param type: 

        :schema: CfnDomainProps
        '''
        if isinstance(attributes, dict):
            attributes = CfnDomainPropsAttributes(**attributes)
        if isinstance(relationships, dict):
            relationships = Relationships(**relationships)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a17d782d394c6ed535df8487bb2a077081880aef4b907ad683bfccb547d8514)
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument relationships", value=relationships, expected_type=type_hints["relationships"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attributes is not None:
            self._values["attributes"] = attributes
        if relationships is not None:
            self._values["relationships"] = relationships
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def attributes(self) -> typing.Optional["CfnDomainPropsAttributes"]:
        '''
        :schema: CfnDomainProps#Attributes
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional["CfnDomainPropsAttributes"], result)

    @builtins.property
    def relationships(self) -> typing.Optional["Relationships"]:
        '''
        :schema: CfnDomainProps#Relationships
        '''
        result = self._values.get("relationships")
        return typing.cast(typing.Optional["Relationships"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDomainProps#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-tls-domain.CfnDomainPropsAttributes",
    jsii_struct_bases=[],
    name_mapping={"created_at": "createdAt"},
)
class CfnDomainPropsAttributes:
    def __init__(
        self,
        *,
        created_at: typing.Optional[datetime.datetime] = None,
    ) -> None:
        '''
        :param created_at: 

        :schema: CfnDomainPropsAttributes
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f4deffb2dd4d2ec4938db0371c55e3fa07c6c295ed84becc1ae7a01bacdeca0)
            check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if created_at is not None:
            self._values["created_at"] = created_at

    @builtins.property
    def created_at(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: CfnDomainPropsAttributes#CreatedAt
        '''
        result = self._values.get("created_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainPropsAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-tls-domain.Data",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "type": "type"},
)
class Data:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: 
        :param type: 

        :schema: Data
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__045171151807776c81694747db29b78d2491f534fdc18a075bd56fe440ab6c80)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Data#Id
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Data#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Data(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-tls-domain.Relationships",
    jsii_struct_bases=[],
    name_mapping={
        "tls_certificate": "tlsCertificate",
        "tls_configuration": "tlsConfiguration",
        "tls_domain": "tlsDomain",
    },
)
class Relationships:
    def __init__(
        self,
        *,
        tls_certificate: typing.Optional[typing.Union["RelationshipsTlsCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_configuration: typing.Optional[typing.Union["RelationshipsTlsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_domain: typing.Optional[typing.Union["RelationshipsTlsDomain", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param tls_certificate: 
        :param tls_configuration: 
        :param tls_domain: 

        :schema: Relationships
        '''
        if isinstance(tls_certificate, dict):
            tls_certificate = RelationshipsTlsCertificate(**tls_certificate)
        if isinstance(tls_configuration, dict):
            tls_configuration = RelationshipsTlsConfiguration(**tls_configuration)
        if isinstance(tls_domain, dict):
            tls_domain = RelationshipsTlsDomain(**tls_domain)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23c1a99f18a0dc39b0cb576705f25b9ccdcdc64fc1e86b95d121081090ea4fb0)
            check_type(argname="argument tls_certificate", value=tls_certificate, expected_type=type_hints["tls_certificate"])
            check_type(argname="argument tls_configuration", value=tls_configuration, expected_type=type_hints["tls_configuration"])
            check_type(argname="argument tls_domain", value=tls_domain, expected_type=type_hints["tls_domain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tls_certificate is not None:
            self._values["tls_certificate"] = tls_certificate
        if tls_configuration is not None:
            self._values["tls_configuration"] = tls_configuration
        if tls_domain is not None:
            self._values["tls_domain"] = tls_domain

    @builtins.property
    def tls_certificate(self) -> typing.Optional["RelationshipsTlsCertificate"]:
        '''
        :schema: Relationships#TlsCertificate
        '''
        result = self._values.get("tls_certificate")
        return typing.cast(typing.Optional["RelationshipsTlsCertificate"], result)

    @builtins.property
    def tls_configuration(self) -> typing.Optional["RelationshipsTlsConfiguration"]:
        '''
        :schema: Relationships#TlsConfiguration
        '''
        result = self._values.get("tls_configuration")
        return typing.cast(typing.Optional["RelationshipsTlsConfiguration"], result)

    @builtins.property
    def tls_domain(self) -> typing.Optional["RelationshipsTlsDomain"]:
        '''
        :schema: Relationships#TlsDomain
        '''
        result = self._values.get("tls_domain")
        return typing.cast(typing.Optional["RelationshipsTlsDomain"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Relationships(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-tls-domain.RelationshipsTlsCertificate",
    jsii_struct_bases=[],
    name_mapping={"data": "data"},
)
class RelationshipsTlsCertificate:
    def __init__(
        self,
        *,
        data: typing.Optional[typing.Union[Data, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param data: 

        :schema: RelationshipsTlsCertificate
        '''
        if isinstance(data, dict):
            data = Data(**data)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__778bc076bf2cb5b5beb847f4751172362628ce95164d2cb6119aada5440dc4aa)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data is not None:
            self._values["data"] = data

    @builtins.property
    def data(self) -> typing.Optional[Data]:
        '''
        :schema: RelationshipsTlsCertificate#Data
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[Data], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RelationshipsTlsCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-tls-domain.RelationshipsTlsConfiguration",
    jsii_struct_bases=[],
    name_mapping={"data": "data"},
)
class RelationshipsTlsConfiguration:
    def __init__(
        self,
        *,
        data: typing.Optional[typing.Union[Data, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param data: 

        :schema: RelationshipsTlsConfiguration
        '''
        if isinstance(data, dict):
            data = Data(**data)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac27d797a4e855f07831af3424448ebf4229a6227a6ba36aaa991d37710273b4)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data is not None:
            self._values["data"] = data

    @builtins.property
    def data(self) -> typing.Optional[Data]:
        '''
        :schema: RelationshipsTlsConfiguration#Data
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[Data], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RelationshipsTlsConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-tls-domain.RelationshipsTlsDomain",
    jsii_struct_bases=[],
    name_mapping={"data": "data"},
)
class RelationshipsTlsDomain:
    def __init__(
        self,
        *,
        data: typing.Optional[typing.Union[Data, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param data: 

        :schema: RelationshipsTlsDomain
        '''
        if isinstance(data, dict):
            data = Data(**data)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5e9e40e1e9e45cb4e63d8f3b13f05f21bd20cb01fc3e4a74d06344617978efb)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data is not None:
            self._values["data"] = data

    @builtins.property
    def data(self) -> typing.Optional[Data]:
        '''
        :schema: RelationshipsTlsDomain#Data
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[Data], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RelationshipsTlsDomain(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDomain",
    "CfnDomainProps",
    "CfnDomainPropsAttributes",
    "Data",
    "Relationships",
    "RelationshipsTlsCertificate",
    "RelationshipsTlsConfiguration",
    "RelationshipsTlsDomain",
]

publication.publish()

def _typecheckingstub__d33f617034c88672704708d06c11431b4d83617306a58da809c1f4d364a70a5d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    attributes: typing.Optional[typing.Union[CfnDomainPropsAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
    relationships: typing.Optional[typing.Union[Relationships, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a17d782d394c6ed535df8487bb2a077081880aef4b907ad683bfccb547d8514(
    *,
    attributes: typing.Optional[typing.Union[CfnDomainPropsAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
    relationships: typing.Optional[typing.Union[Relationships, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f4deffb2dd4d2ec4938db0371c55e3fa07c6c295ed84becc1ae7a01bacdeca0(
    *,
    created_at: typing.Optional[datetime.datetime] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045171151807776c81694747db29b78d2491f534fdc18a075bd56fe440ab6c80(
    *,
    id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c1a99f18a0dc39b0cb576705f25b9ccdcdc64fc1e86b95d121081090ea4fb0(
    *,
    tls_certificate: typing.Optional[typing.Union[RelationshipsTlsCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_configuration: typing.Optional[typing.Union[RelationshipsTlsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_domain: typing.Optional[typing.Union[RelationshipsTlsDomain, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__778bc076bf2cb5b5beb847f4751172362628ce95164d2cb6119aada5440dc4aa(
    *,
    data: typing.Optional[typing.Union[Data, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac27d797a4e855f07831af3424448ebf4229a6227a6ba36aaa991d37710273b4(
    *,
    data: typing.Optional[typing.Union[Data, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e9e40e1e9e45cb4e63d8f3b13f05f21bd20cb01fc3e4a74d06344617978efb(
    *,
    data: typing.Optional[typing.Union[Data, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
