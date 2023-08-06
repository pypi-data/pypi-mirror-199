'''
# fastly-logging-splunk

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Fastly::Logging::Splunk` v1.1.0.

## Description

Manage a Fastly Splunk Log.

## References

* [Source](https://developer.fastly.com/reference/api/logging/splunk/)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Fastly::Logging::Splunk \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Fastly-Logging-Splunk \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Fastly::Logging::Splunk`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Ffastly-logging-splunk+v1.1.0).
* Issues related to `Fastly::Logging::Splunk` should be reported to the [publisher](https://developer.fastly.com/reference/api/logging/splunk/).

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


class CfnSplunk(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/fastly-logging-splunk.CfnSplunk",
):
    '''A CloudFormation ``Fastly::Logging::Splunk``.

    :cloudformationResource: Fastly::Logging::Splunk
    :link: https://developer.fastly.com/reference/api/logging/splunk/
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        token: builtins.str,
        url: builtins.str,
        format_version: typing.Optional["CfnSplunkPropsFormatVersion"] = None,
        placement: typing.Optional["CfnSplunkPropsPlacement"] = None,
        request_max_bytes: typing.Optional[jsii.Number] = None,
        request_max_entries: typing.Optional[jsii.Number] = None,
        response_condition: typing.Optional[builtins.str] = None,
        service_id: typing.Optional[builtins.str] = None,
        tls_ca_cert: typing.Optional[builtins.str] = None,
        tls_client_cert: typing.Optional[builtins.str] = None,
        tls_client_key: typing.Optional[builtins.str] = None,
        tls_hostname: typing.Optional[builtins.str] = None,
        use_tls: typing.Optional["CfnSplunkPropsUseTls"] = None,
        version: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``Fastly::Logging::Splunk``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name for the real-time logging configuration.
        :param token: A Splunk token for use in posting logs over HTTP to your collector.
        :param url: The URL to post logs to.
        :param format_version: The version of the custom logging format used for the configured endpoint.
        :param placement: Where in the generated VCL the logging call should be placed.
        :param request_max_bytes: The maximum number of bytes sent in one request. Defaults 0 for unbounded. [Default 0]
        :param request_max_entries: The maximum number of logs sent in one request. Defaults 0 for unbounded. [Default 0]
        :param response_condition: The name of an existing condition in the configured endpoint, or leave blank to always execute.
        :param service_id: Alphanumeric string identifying the service. Read-only.
        :param tls_ca_cert: A secure certificate to authenticate a server with. Must be in PEM format.
        :param tls_client_cert: The client certificate used to make authenticated requests. Must be in PEM format.
        :param tls_client_key: The client private key used to make authenticated requests. Must be in PEM format.
        :param tls_hostname: The hostname to verify the server's certificate. This should be one of the Subject Alternative Name (SAN) fields for the certificate. Common Names (CN) are not supported.
        :param use_tls: Whether to use TLS. [Default 0]
        :param version: Integer identifying a domain version. Read-only.
        :param version_id: Alphanumeric string identifying the service version.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__666dbe92823e91a7004c9b28103f925f8acbb37483ce290743892d86adb89676)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSplunkProps(
            name=name,
            token=token,
            url=url,
            format_version=format_version,
            placement=placement,
            request_max_bytes=request_max_bytes,
            request_max_entries=request_max_entries,
            response_condition=response_condition,
            service_id=service_id,
            tls_ca_cert=tls_ca_cert,
            tls_client_cert=tls_client_cert,
            tls_client_key=tls_client_key,
            tls_hostname=tls_hostname,
            use_tls=use_tls,
            version=version,
            version_id=version_id,
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
        '''Attribute ``Fastly::Logging::Splunk.CreatedAt``.

        :link: https://developer.fastly.com/reference/api/logging/splunk/
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrDeletedAt")
    def attr_deleted_at(self) -> builtins.str:
        '''Attribute ``Fastly::Logging::Splunk.DeletedAt``.

        :link: https://developer.fastly.com/reference/api/logging/splunk/
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDeletedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''Attribute ``Fastly::Logging::Splunk.UpdatedAt``.

        :link: https://developer.fastly.com/reference/api/logging/splunk/
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnSplunkProps":
        '''Resource props.'''
        return typing.cast("CfnSplunkProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-logging-splunk.CfnSplunkProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "token": "token",
        "url": "url",
        "format_version": "formatVersion",
        "placement": "placement",
        "request_max_bytes": "requestMaxBytes",
        "request_max_entries": "requestMaxEntries",
        "response_condition": "responseCondition",
        "service_id": "serviceId",
        "tls_ca_cert": "tlsCaCert",
        "tls_client_cert": "tlsClientCert",
        "tls_client_key": "tlsClientKey",
        "tls_hostname": "tlsHostname",
        "use_tls": "useTls",
        "version": "version",
        "version_id": "versionId",
    },
)
class CfnSplunkProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        token: builtins.str,
        url: builtins.str,
        format_version: typing.Optional["CfnSplunkPropsFormatVersion"] = None,
        placement: typing.Optional["CfnSplunkPropsPlacement"] = None,
        request_max_bytes: typing.Optional[jsii.Number] = None,
        request_max_entries: typing.Optional[jsii.Number] = None,
        response_condition: typing.Optional[builtins.str] = None,
        service_id: typing.Optional[builtins.str] = None,
        tls_ca_cert: typing.Optional[builtins.str] = None,
        tls_client_cert: typing.Optional[builtins.str] = None,
        tls_client_key: typing.Optional[builtins.str] = None,
        tls_hostname: typing.Optional[builtins.str] = None,
        use_tls: typing.Optional["CfnSplunkPropsUseTls"] = None,
        version: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Manage a Fastly Splunk Log.

        :param name: The name for the real-time logging configuration.
        :param token: A Splunk token for use in posting logs over HTTP to your collector.
        :param url: The URL to post logs to.
        :param format_version: The version of the custom logging format used for the configured endpoint.
        :param placement: Where in the generated VCL the logging call should be placed.
        :param request_max_bytes: The maximum number of bytes sent in one request. Defaults 0 for unbounded. [Default 0]
        :param request_max_entries: The maximum number of logs sent in one request. Defaults 0 for unbounded. [Default 0]
        :param response_condition: The name of an existing condition in the configured endpoint, or leave blank to always execute.
        :param service_id: Alphanumeric string identifying the service. Read-only.
        :param tls_ca_cert: A secure certificate to authenticate a server with. Must be in PEM format.
        :param tls_client_cert: The client certificate used to make authenticated requests. Must be in PEM format.
        :param tls_client_key: The client private key used to make authenticated requests. Must be in PEM format.
        :param tls_hostname: The hostname to verify the server's certificate. This should be one of the Subject Alternative Name (SAN) fields for the certificate. Common Names (CN) are not supported.
        :param use_tls: Whether to use TLS. [Default 0]
        :param version: Integer identifying a domain version. Read-only.
        :param version_id: Alphanumeric string identifying the service version.

        :schema: CfnSplunkProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e8102a574a68bbb6c4d9bdaf27705fedf20e20b4a23a132124c702ae953b345)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument format_version", value=format_version, expected_type=type_hints["format_version"])
            check_type(argname="argument placement", value=placement, expected_type=type_hints["placement"])
            check_type(argname="argument request_max_bytes", value=request_max_bytes, expected_type=type_hints["request_max_bytes"])
            check_type(argname="argument request_max_entries", value=request_max_entries, expected_type=type_hints["request_max_entries"])
            check_type(argname="argument response_condition", value=response_condition, expected_type=type_hints["response_condition"])
            check_type(argname="argument service_id", value=service_id, expected_type=type_hints["service_id"])
            check_type(argname="argument tls_ca_cert", value=tls_ca_cert, expected_type=type_hints["tls_ca_cert"])
            check_type(argname="argument tls_client_cert", value=tls_client_cert, expected_type=type_hints["tls_client_cert"])
            check_type(argname="argument tls_client_key", value=tls_client_key, expected_type=type_hints["tls_client_key"])
            check_type(argname="argument tls_hostname", value=tls_hostname, expected_type=type_hints["tls_hostname"])
            check_type(argname="argument use_tls", value=use_tls, expected_type=type_hints["use_tls"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "token": token,
            "url": url,
        }
        if format_version is not None:
            self._values["format_version"] = format_version
        if placement is not None:
            self._values["placement"] = placement
        if request_max_bytes is not None:
            self._values["request_max_bytes"] = request_max_bytes
        if request_max_entries is not None:
            self._values["request_max_entries"] = request_max_entries
        if response_condition is not None:
            self._values["response_condition"] = response_condition
        if service_id is not None:
            self._values["service_id"] = service_id
        if tls_ca_cert is not None:
            self._values["tls_ca_cert"] = tls_ca_cert
        if tls_client_cert is not None:
            self._values["tls_client_cert"] = tls_client_cert
        if tls_client_key is not None:
            self._values["tls_client_key"] = tls_client_key
        if tls_hostname is not None:
            self._values["tls_hostname"] = tls_hostname
        if use_tls is not None:
            self._values["use_tls"] = use_tls
        if version is not None:
            self._values["version"] = version
        if version_id is not None:
            self._values["version_id"] = version_id

    @builtins.property
    def name(self) -> builtins.str:
        '''The name for the real-time logging configuration.

        :schema: CfnSplunkProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token(self) -> builtins.str:
        '''A Splunk token for use in posting logs over HTTP to your collector.

        :schema: CfnSplunkProps#Token
        '''
        result = self._values.get("token")
        assert result is not None, "Required property 'token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''The URL to post logs to.

        :schema: CfnSplunkProps#Url
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def format_version(self) -> typing.Optional["CfnSplunkPropsFormatVersion"]:
        '''The version of the custom logging format used for the configured endpoint.

        :schema: CfnSplunkProps#FormatVersion
        '''
        result = self._values.get("format_version")
        return typing.cast(typing.Optional["CfnSplunkPropsFormatVersion"], result)

    @builtins.property
    def placement(self) -> typing.Optional["CfnSplunkPropsPlacement"]:
        '''Where in the generated VCL the logging call should be placed.

        :schema: CfnSplunkProps#Placement
        '''
        result = self._values.get("placement")
        return typing.cast(typing.Optional["CfnSplunkPropsPlacement"], result)

    @builtins.property
    def request_max_bytes(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of bytes sent in one request.

        Defaults 0 for unbounded. [Default 0]

        :schema: CfnSplunkProps#RequestMaxBytes
        '''
        result = self._values.get("request_max_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def request_max_entries(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of logs sent in one request.

        Defaults 0 for unbounded. [Default 0]

        :schema: CfnSplunkProps#RequestMaxEntries
        '''
        result = self._values.get("request_max_entries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def response_condition(self) -> typing.Optional[builtins.str]:
        '''The name of an existing condition in the configured endpoint, or leave blank to always execute.

        :schema: CfnSplunkProps#ResponseCondition
        '''
        result = self._values.get("response_condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_id(self) -> typing.Optional[builtins.str]:
        '''Alphanumeric string identifying the service.

        Read-only.

        :schema: CfnSplunkProps#ServiceId
        '''
        result = self._values.get("service_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls_ca_cert(self) -> typing.Optional[builtins.str]:
        '''A secure certificate to authenticate a server with.

        Must be in PEM format.

        :schema: CfnSplunkProps#TlsCaCert
        '''
        result = self._values.get("tls_ca_cert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls_client_cert(self) -> typing.Optional[builtins.str]:
        '''The client certificate used to make authenticated requests.

        Must be in PEM format.

        :schema: CfnSplunkProps#TlsClientCert
        '''
        result = self._values.get("tls_client_cert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls_client_key(self) -> typing.Optional[builtins.str]:
        '''The client private key used to make authenticated requests.

        Must be in PEM format.

        :schema: CfnSplunkProps#TlsClientKey
        '''
        result = self._values.get("tls_client_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls_hostname(self) -> typing.Optional[builtins.str]:
        '''The hostname to verify the server's certificate.

        This should be one of the Subject Alternative Name (SAN) fields for the certificate. Common Names (CN) are not supported.

        :schema: CfnSplunkProps#TlsHostname
        '''
        result = self._values.get("tls_hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_tls(self) -> typing.Optional["CfnSplunkPropsUseTls"]:
        '''Whether to use TLS.

        [Default 0]

        :schema: CfnSplunkProps#UseTls
        '''
        result = self._values.get("use_tls")
        return typing.cast(typing.Optional["CfnSplunkPropsUseTls"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Integer identifying a domain version.

        Read-only.

        :schema: CfnSplunkProps#Version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''Alphanumeric string identifying the service version.

        :schema: CfnSplunkProps#VersionId
        '''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSplunkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/fastly-logging-splunk.CfnSplunkPropsFormatVersion"
)
class CfnSplunkPropsFormatVersion(enum.Enum):
    '''The version of the custom logging format used for the configured endpoint.

    :schema: CfnSplunkPropsFormatVersion
    '''

    VALUE_1 = "VALUE_1"
    '''1.'''
    VALUE_2 = "VALUE_2"
    '''2.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/fastly-logging-splunk.CfnSplunkPropsPlacement"
)
class CfnSplunkPropsPlacement(enum.Enum):
    '''Where in the generated VCL the logging call should be placed.

    :schema: CfnSplunkPropsPlacement
    '''

    NONE = "NONE"
    '''none.'''
    WAF_DEBUG = "WAF_DEBUG"
    '''waf_debug.'''


@jsii.enum(jsii_type="@cdk-cloudformation/fastly-logging-splunk.CfnSplunkPropsUseTls")
class CfnSplunkPropsUseTls(enum.Enum):
    '''Whether to use TLS.

    [Default 0]

    :schema: CfnSplunkPropsUseTls
    '''

    VALUE_0 = "VALUE_0"
    '''0.'''
    VALUE_1 = "VALUE_1"
    '''1.'''


__all__ = [
    "CfnSplunk",
    "CfnSplunkProps",
    "CfnSplunkPropsFormatVersion",
    "CfnSplunkPropsPlacement",
    "CfnSplunkPropsUseTls",
]

publication.publish()

def _typecheckingstub__666dbe92823e91a7004c9b28103f925f8acbb37483ce290743892d86adb89676(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    token: builtins.str,
    url: builtins.str,
    format_version: typing.Optional[CfnSplunkPropsFormatVersion] = None,
    placement: typing.Optional[CfnSplunkPropsPlacement] = None,
    request_max_bytes: typing.Optional[jsii.Number] = None,
    request_max_entries: typing.Optional[jsii.Number] = None,
    response_condition: typing.Optional[builtins.str] = None,
    service_id: typing.Optional[builtins.str] = None,
    tls_ca_cert: typing.Optional[builtins.str] = None,
    tls_client_cert: typing.Optional[builtins.str] = None,
    tls_client_key: typing.Optional[builtins.str] = None,
    tls_hostname: typing.Optional[builtins.str] = None,
    use_tls: typing.Optional[CfnSplunkPropsUseTls] = None,
    version: typing.Optional[builtins.str] = None,
    version_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8102a574a68bbb6c4d9bdaf27705fedf20e20b4a23a132124c702ae953b345(
    *,
    name: builtins.str,
    token: builtins.str,
    url: builtins.str,
    format_version: typing.Optional[CfnSplunkPropsFormatVersion] = None,
    placement: typing.Optional[CfnSplunkPropsPlacement] = None,
    request_max_bytes: typing.Optional[jsii.Number] = None,
    request_max_entries: typing.Optional[jsii.Number] = None,
    response_condition: typing.Optional[builtins.str] = None,
    service_id: typing.Optional[builtins.str] = None,
    tls_ca_cert: typing.Optional[builtins.str] = None,
    tls_client_cert: typing.Optional[builtins.str] = None,
    tls_client_key: typing.Optional[builtins.str] = None,
    tls_hostname: typing.Optional[builtins.str] = None,
    use_tls: typing.Optional[CfnSplunkPropsUseTls] = None,
    version: typing.Optional[builtins.str] = None,
    version_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
