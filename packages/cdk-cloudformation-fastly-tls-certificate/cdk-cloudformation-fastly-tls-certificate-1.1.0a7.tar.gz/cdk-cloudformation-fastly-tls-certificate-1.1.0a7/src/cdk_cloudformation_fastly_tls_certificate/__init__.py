'''
# fastly-tls-certificate

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Fastly::Tls::Certificate` v1.1.0.

## Description

Manage a custom Tls Certificate upload

## References

* [Source](https://github.com/aws-ia/cloudformation-fastly-resource-providers)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Fastly::Tls::Certificate \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Fastly-Tls-Certificate \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Fastly::Tls::Certificate`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Ffastly-tls-certificate+v1.1.0).
* Issues related to `Fastly::Tls::Certificate` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-fastly-resource-providers).

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


class CfnCertificate(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/fastly-tls-certificate.CfnCertificate",
):
    '''A CloudFormation ``Fastly::Tls::Certificate``.

    :cloudformationResource: Fastly::Tls::Certificate
    :link: https://github.com/aws-ia/cloudformation-fastly-resource-providers
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        attributes: typing.Optional[typing.Union["CfnCertificatePropsAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
        relationships: typing.Optional[typing.Union["Relationships", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``Fastly::Tls::Certificate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param attributes: 
        :param relationships: 
        :param type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed4e72a3247f2002cb20831e095a74140078e9c395dbba34166d9bd3ff74d63e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCertificateProps(
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
        '''Attribute ``Fastly::Tls::Certificate.Id``.

        :link: https://github.com/aws-ia/cloudformation-fastly-resource-providers
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnCertificateProps":
        '''Resource props.'''
        return typing.cast("CfnCertificateProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-tls-certificate.CfnCertificateProps",
    jsii_struct_bases=[],
    name_mapping={
        "attributes": "attributes",
        "relationships": "relationships",
        "type": "type",
    },
)
class CfnCertificateProps:
    def __init__(
        self,
        *,
        attributes: typing.Optional[typing.Union["CfnCertificatePropsAttributes", typing.Dict[builtins.str, typing.Any]]] = None,
        relationships: typing.Optional[typing.Union["Relationships", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Manage a custom Tls Certificate upload.

        :param attributes: 
        :param relationships: 
        :param type: 

        :schema: CfnCertificateProps
        '''
        if isinstance(attributes, dict):
            attributes = CfnCertificatePropsAttributes(**attributes)
        if isinstance(relationships, dict):
            relationships = Relationships(**relationships)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__621773a716cc72cbe60d2fd37d3be6caf8c1b0106cc44d39d0c284434bd7214c)
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
    def attributes(self) -> typing.Optional["CfnCertificatePropsAttributes"]:
        '''
        :schema: CfnCertificateProps#Attributes
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional["CfnCertificatePropsAttributes"], result)

    @builtins.property
    def relationships(self) -> typing.Optional["Relationships"]:
        '''
        :schema: CfnCertificateProps#Relationships
        '''
        result = self._values.get("relationships")
        return typing.cast(typing.Optional["Relationships"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnCertificateProps#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCertificateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-tls-certificate.CfnCertificatePropsAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "cert_blob": "certBlob",
        "created_at": "createdAt",
        "issued_to": "issuedTo",
        "issuer": "issuer",
        "name": "name",
        "not_after": "notAfter",
        "not_before": "notBefore",
        "replace": "replace",
        "serial_number": "serialNumber",
        "signature_algorithm": "signatureAlgorithm",
        "updated_at": "updatedAt",
    },
)
class CfnCertificatePropsAttributes:
    def __init__(
        self,
        *,
        cert_blob: builtins.str,
        created_at: typing.Optional[datetime.datetime] = None,
        issued_to: typing.Optional[builtins.str] = None,
        issuer: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        not_after: typing.Optional[builtins.str] = None,
        not_before: typing.Optional[builtins.str] = None,
        replace: typing.Optional[builtins.str] = None,
        serial_number: typing.Optional[builtins.str] = None,
        signature_algorithm: typing.Optional[builtins.str] = None,
        updated_at: typing.Optional[datetime.datetime] = None,
    ) -> None:
        '''
        :param cert_blob: 
        :param created_at: 
        :param issued_to: 
        :param issuer: 
        :param name: 
        :param not_after: 
        :param not_before: 
        :param replace: 
        :param serial_number: 
        :param signature_algorithm: 
        :param updated_at: 

        :schema: CfnCertificatePropsAttributes
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b32ab4e50093697de43557dfedba54730ea1dcd0a0590d9f433298b35e7e12c6)
            check_type(argname="argument cert_blob", value=cert_blob, expected_type=type_hints["cert_blob"])
            check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
            check_type(argname="argument issued_to", value=issued_to, expected_type=type_hints["issued_to"])
            check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument not_after", value=not_after, expected_type=type_hints["not_after"])
            check_type(argname="argument not_before", value=not_before, expected_type=type_hints["not_before"])
            check_type(argname="argument replace", value=replace, expected_type=type_hints["replace"])
            check_type(argname="argument serial_number", value=serial_number, expected_type=type_hints["serial_number"])
            check_type(argname="argument signature_algorithm", value=signature_algorithm, expected_type=type_hints["signature_algorithm"])
            check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cert_blob": cert_blob,
        }
        if created_at is not None:
            self._values["created_at"] = created_at
        if issued_to is not None:
            self._values["issued_to"] = issued_to
        if issuer is not None:
            self._values["issuer"] = issuer
        if name is not None:
            self._values["name"] = name
        if not_after is not None:
            self._values["not_after"] = not_after
        if not_before is not None:
            self._values["not_before"] = not_before
        if replace is not None:
            self._values["replace"] = replace
        if serial_number is not None:
            self._values["serial_number"] = serial_number
        if signature_algorithm is not None:
            self._values["signature_algorithm"] = signature_algorithm
        if updated_at is not None:
            self._values["updated_at"] = updated_at

    @builtins.property
    def cert_blob(self) -> builtins.str:
        '''
        :schema: CfnCertificatePropsAttributes#CertBlob
        '''
        result = self._values.get("cert_blob")
        assert result is not None, "Required property 'cert_blob' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def created_at(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: CfnCertificatePropsAttributes#CreatedAt
        '''
        result = self._values.get("created_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def issued_to(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnCertificatePropsAttributes#IssuedTo
        '''
        result = self._values.get("issued_to")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issuer(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnCertificatePropsAttributes#Issuer
        '''
        result = self._values.get("issuer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnCertificatePropsAttributes#Name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def not_after(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnCertificatePropsAttributes#NotAfter
        '''
        result = self._values.get("not_after")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def not_before(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnCertificatePropsAttributes#NotBefore
        '''
        result = self._values.get("not_before")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replace(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnCertificatePropsAttributes#Replace
        '''
        result = self._values.get("replace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serial_number(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnCertificatePropsAttributes#SerialNumber
        '''
        result = self._values.get("serial_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signature_algorithm(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnCertificatePropsAttributes#SignatureAlgorithm
        '''
        result = self._values.get("signature_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def updated_at(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: CfnCertificatePropsAttributes#UpdatedAt
        '''
        result = self._values.get("updated_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCertificatePropsAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-tls-certificate.Data",
    jsii_struct_bases=[],
    name_mapping={"id": "id"},
)
class Data:
    def __init__(self, *, id: typing.Optional[builtins.str] = None) -> None:
        '''
        :param id: 

        :schema: Data
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ec75b765f07416333691b605aa051cc4c418bb5a368e312ce3e766681af925)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: Data#Id
        '''
        result = self._values.get("id")
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
    jsii_type="@cdk-cloudformation/fastly-tls-certificate.Relationships",
    jsii_struct_bases=[],
    name_mapping={"tls_domains": "tlsDomains"},
)
class Relationships:
    def __init__(
        self,
        *,
        tls_domains: typing.Optional[typing.Union["RelationshipsTlsDomains", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param tls_domains: 

        :schema: Relationships
        '''
        if isinstance(tls_domains, dict):
            tls_domains = RelationshipsTlsDomains(**tls_domains)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__453ef282ca4d8a097e97d92c592c0116ab9eb70fc8dbafa2b3149b0195a09102)
            check_type(argname="argument tls_domains", value=tls_domains, expected_type=type_hints["tls_domains"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tls_domains is not None:
            self._values["tls_domains"] = tls_domains

    @builtins.property
    def tls_domains(self) -> typing.Optional["RelationshipsTlsDomains"]:
        '''
        :schema: Relationships#TlsDomains
        '''
        result = self._values.get("tls_domains")
        return typing.cast(typing.Optional["RelationshipsTlsDomains"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Relationships(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-tls-certificate.RelationshipsTlsDomains",
    jsii_struct_bases=[],
    name_mapping={"data": "data"},
)
class RelationshipsTlsDomains:
    def __init__(
        self,
        *,
        data: typing.Optional[typing.Sequence[typing.Union[Data, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param data: 

        :schema: RelationshipsTlsDomains
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65cc02bab292f14c3ca19a7d9eed8779e5bbd50ed8d0a57d27b3582a1195cb45)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data is not None:
            self._values["data"] = data

    @builtins.property
    def data(self) -> typing.Optional[typing.List[Data]]:
        '''
        :schema: RelationshipsTlsDomains#Data
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.List[Data]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RelationshipsTlsDomains(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnCertificate",
    "CfnCertificateProps",
    "CfnCertificatePropsAttributes",
    "Data",
    "Relationships",
    "RelationshipsTlsDomains",
]

publication.publish()

def _typecheckingstub__ed4e72a3247f2002cb20831e095a74140078e9c395dbba34166d9bd3ff74d63e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    attributes: typing.Optional[typing.Union[CfnCertificatePropsAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
    relationships: typing.Optional[typing.Union[Relationships, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__621773a716cc72cbe60d2fd37d3be6caf8c1b0106cc44d39d0c284434bd7214c(
    *,
    attributes: typing.Optional[typing.Union[CfnCertificatePropsAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
    relationships: typing.Optional[typing.Union[Relationships, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b32ab4e50093697de43557dfedba54730ea1dcd0a0590d9f433298b35e7e12c6(
    *,
    cert_blob: builtins.str,
    created_at: typing.Optional[datetime.datetime] = None,
    issued_to: typing.Optional[builtins.str] = None,
    issuer: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    not_after: typing.Optional[builtins.str] = None,
    not_before: typing.Optional[builtins.str] = None,
    replace: typing.Optional[builtins.str] = None,
    serial_number: typing.Optional[builtins.str] = None,
    signature_algorithm: typing.Optional[builtins.str] = None,
    updated_at: typing.Optional[datetime.datetime] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ec75b765f07416333691b605aa051cc4c418bb5a368e312ce3e766681af925(
    *,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__453ef282ca4d8a097e97d92c592c0116ab9eb70fc8dbafa2b3149b0195a09102(
    *,
    tls_domains: typing.Optional[typing.Union[RelationshipsTlsDomains, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65cc02bab292f14c3ca19a7d9eed8779e5bbd50ed8d0a57d27b3582a1195cb45(
    *,
    data: typing.Optional[typing.Sequence[typing.Union[Data, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
