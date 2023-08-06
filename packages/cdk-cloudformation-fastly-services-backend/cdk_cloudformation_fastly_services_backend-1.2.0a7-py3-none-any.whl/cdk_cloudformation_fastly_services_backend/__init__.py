'''
# fastly-services-backend

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Fastly::Services::Backend` v1.2.0.

## Description

Manage a Fastly service backend.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-fastly-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-fastly-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Fastly::Services::Backend \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Fastly-Services-Backend \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Fastly::Services::Backend`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Ffastly-services-backend+v1.2.0).
* Issues related to `Fastly::Services::Backend` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-fastly-resource-providers).

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


class CfnBackend(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/fastly-services-backend.CfnBackend",
):
    '''A CloudFormation ``Fastly::Services::Backend``.

    :cloudformationResource: Fastly::Services::Backend
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
        address: typing.Optional[builtins.str] = None,
        auto_loadbalance: typing.Optional[builtins.bool] = None,
        backend_name: typing.Optional[builtins.str] = None,
        between_bytes_timeout: typing.Optional[jsii.Number] = None,
        client_cert: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        connect_timeout: typing.Optional[jsii.Number] = None,
        created_at: typing.Optional[datetime.datetime] = None,
        deleted_at: typing.Optional[datetime.datetime] = None,
        first_byte_timeout: typing.Optional[jsii.Number] = None,
        healthcheck: typing.Optional[builtins.str] = None,
        ipv4: typing.Optional[builtins.str] = None,
        ipv6: typing.Optional[builtins.str] = None,
        max_conn: typing.Optional[jsii.Number] = None,
        max_tls_version: typing.Optional["MaxTlsVersion"] = None,
        min_tls_version: typing.Optional["MinTlsVersion"] = None,
        override_host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        request_condition: typing.Optional[builtins.str] = None,
        shield: typing.Optional[builtins.str] = None,
        ssl_ca_cert: typing.Optional[builtins.str] = None,
        ssl_cert_hostname: typing.Optional[builtins.str] = None,
        ssl_check_cert: typing.Optional[builtins.bool] = None,
        ssl_ciphers: typing.Optional[builtins.str] = None,
        ssl_client_cert: typing.Optional[builtins.str] = None,
        ssl_client_key: typing.Optional[builtins.str] = None,
        ssl_sni_hostname: typing.Optional[builtins.str] = None,
        updated_at: typing.Optional[datetime.datetime] = None,
        use_ssl: typing.Optional[builtins.bool] = None,
        version: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``Fastly::Services::Backend``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: 
        :param service_id: 
        :param version_id: 
        :param address: 
        :param auto_loadbalance: 
        :param backend_name: 
        :param between_bytes_timeout: 
        :param client_cert: 
        :param comment: 
        :param connect_timeout: 
        :param created_at: 
        :param deleted_at: 
        :param first_byte_timeout: 
        :param healthcheck: 
        :param ipv4: 
        :param ipv6: 
        :param max_conn: 
        :param max_tls_version: 
        :param min_tls_version: 
        :param override_host: 
        :param port: 
        :param request_condition: 
        :param shield: 
        :param ssl_ca_cert: 
        :param ssl_cert_hostname: 
        :param ssl_check_cert: 
        :param ssl_ciphers: 
        :param ssl_client_cert: 
        :param ssl_client_key: 
        :param ssl_sni_hostname: 
        :param updated_at: 
        :param use_ssl: 
        :param version: 
        :param weight: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bab8314cc72b3e625c440acdb8eb47a34a489fefd699be12e2248a57e9530b9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnBackendProps(
            name=name,
            service_id=service_id,
            version_id=version_id,
            address=address,
            auto_loadbalance=auto_loadbalance,
            backend_name=backend_name,
            between_bytes_timeout=between_bytes_timeout,
            client_cert=client_cert,
            comment=comment,
            connect_timeout=connect_timeout,
            created_at=created_at,
            deleted_at=deleted_at,
            first_byte_timeout=first_byte_timeout,
            healthcheck=healthcheck,
            ipv4=ipv4,
            ipv6=ipv6,
            max_conn=max_conn,
            max_tls_version=max_tls_version,
            min_tls_version=min_tls_version,
            override_host=override_host,
            port=port,
            request_condition=request_condition,
            shield=shield,
            ssl_ca_cert=ssl_ca_cert,
            ssl_cert_hostname=ssl_cert_hostname,
            ssl_check_cert=ssl_check_cert,
            ssl_ciphers=ssl_ciphers,
            ssl_client_cert=ssl_client_cert,
            ssl_client_key=ssl_client_key,
            ssl_sni_hostname=ssl_sni_hostname,
            updated_at=updated_at,
            use_ssl=use_ssl,
            version=version,
            weight=weight,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnBackendProps":
        '''Resource props.'''
        return typing.cast("CfnBackendProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-services-backend.CfnBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "service_id": "serviceId",
        "version_id": "versionId",
        "address": "address",
        "auto_loadbalance": "autoLoadbalance",
        "backend_name": "backendName",
        "between_bytes_timeout": "betweenBytesTimeout",
        "client_cert": "clientCert",
        "comment": "comment",
        "connect_timeout": "connectTimeout",
        "created_at": "createdAt",
        "deleted_at": "deletedAt",
        "first_byte_timeout": "firstByteTimeout",
        "healthcheck": "healthcheck",
        "ipv4": "ipv4",
        "ipv6": "ipv6",
        "max_conn": "maxConn",
        "max_tls_version": "maxTlsVersion",
        "min_tls_version": "minTlsVersion",
        "override_host": "overrideHost",
        "port": "port",
        "request_condition": "requestCondition",
        "shield": "shield",
        "ssl_ca_cert": "sslCaCert",
        "ssl_cert_hostname": "sslCertHostname",
        "ssl_check_cert": "sslCheckCert",
        "ssl_ciphers": "sslCiphers",
        "ssl_client_cert": "sslClientCert",
        "ssl_client_key": "sslClientKey",
        "ssl_sni_hostname": "sslSniHostname",
        "updated_at": "updatedAt",
        "use_ssl": "useSsl",
        "version": "version",
        "weight": "weight",
    },
)
class CfnBackendProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        service_id: builtins.str,
        version_id: builtins.str,
        address: typing.Optional[builtins.str] = None,
        auto_loadbalance: typing.Optional[builtins.bool] = None,
        backend_name: typing.Optional[builtins.str] = None,
        between_bytes_timeout: typing.Optional[jsii.Number] = None,
        client_cert: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        connect_timeout: typing.Optional[jsii.Number] = None,
        created_at: typing.Optional[datetime.datetime] = None,
        deleted_at: typing.Optional[datetime.datetime] = None,
        first_byte_timeout: typing.Optional[jsii.Number] = None,
        healthcheck: typing.Optional[builtins.str] = None,
        ipv4: typing.Optional[builtins.str] = None,
        ipv6: typing.Optional[builtins.str] = None,
        max_conn: typing.Optional[jsii.Number] = None,
        max_tls_version: typing.Optional["MaxTlsVersion"] = None,
        min_tls_version: typing.Optional["MinTlsVersion"] = None,
        override_host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        request_condition: typing.Optional[builtins.str] = None,
        shield: typing.Optional[builtins.str] = None,
        ssl_ca_cert: typing.Optional[builtins.str] = None,
        ssl_cert_hostname: typing.Optional[builtins.str] = None,
        ssl_check_cert: typing.Optional[builtins.bool] = None,
        ssl_ciphers: typing.Optional[builtins.str] = None,
        ssl_client_cert: typing.Optional[builtins.str] = None,
        ssl_client_key: typing.Optional[builtins.str] = None,
        ssl_sni_hostname: typing.Optional[builtins.str] = None,
        updated_at: typing.Optional[datetime.datetime] = None,
        use_ssl: typing.Optional[builtins.bool] = None,
        version: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Manage a Fastly service backend.

        :param name: 
        :param service_id: 
        :param version_id: 
        :param address: 
        :param auto_loadbalance: 
        :param backend_name: 
        :param between_bytes_timeout: 
        :param client_cert: 
        :param comment: 
        :param connect_timeout: 
        :param created_at: 
        :param deleted_at: 
        :param first_byte_timeout: 
        :param healthcheck: 
        :param ipv4: 
        :param ipv6: 
        :param max_conn: 
        :param max_tls_version: 
        :param min_tls_version: 
        :param override_host: 
        :param port: 
        :param request_condition: 
        :param shield: 
        :param ssl_ca_cert: 
        :param ssl_cert_hostname: 
        :param ssl_check_cert: 
        :param ssl_ciphers: 
        :param ssl_client_cert: 
        :param ssl_client_key: 
        :param ssl_sni_hostname: 
        :param updated_at: 
        :param use_ssl: 
        :param version: 
        :param weight: 

        :schema: CfnBackendProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4db93d689717f71c83e958bc2b37aa81500ccdd08058b693d49f0cf2a8f90f7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_id", value=service_id, expected_type=type_hints["service_id"])
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument auto_loadbalance", value=auto_loadbalance, expected_type=type_hints["auto_loadbalance"])
            check_type(argname="argument backend_name", value=backend_name, expected_type=type_hints["backend_name"])
            check_type(argname="argument between_bytes_timeout", value=between_bytes_timeout, expected_type=type_hints["between_bytes_timeout"])
            check_type(argname="argument client_cert", value=client_cert, expected_type=type_hints["client_cert"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument connect_timeout", value=connect_timeout, expected_type=type_hints["connect_timeout"])
            check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
            check_type(argname="argument deleted_at", value=deleted_at, expected_type=type_hints["deleted_at"])
            check_type(argname="argument first_byte_timeout", value=first_byte_timeout, expected_type=type_hints["first_byte_timeout"])
            check_type(argname="argument healthcheck", value=healthcheck, expected_type=type_hints["healthcheck"])
            check_type(argname="argument ipv4", value=ipv4, expected_type=type_hints["ipv4"])
            check_type(argname="argument ipv6", value=ipv6, expected_type=type_hints["ipv6"])
            check_type(argname="argument max_conn", value=max_conn, expected_type=type_hints["max_conn"])
            check_type(argname="argument max_tls_version", value=max_tls_version, expected_type=type_hints["max_tls_version"])
            check_type(argname="argument min_tls_version", value=min_tls_version, expected_type=type_hints["min_tls_version"])
            check_type(argname="argument override_host", value=override_host, expected_type=type_hints["override_host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument request_condition", value=request_condition, expected_type=type_hints["request_condition"])
            check_type(argname="argument shield", value=shield, expected_type=type_hints["shield"])
            check_type(argname="argument ssl_ca_cert", value=ssl_ca_cert, expected_type=type_hints["ssl_ca_cert"])
            check_type(argname="argument ssl_cert_hostname", value=ssl_cert_hostname, expected_type=type_hints["ssl_cert_hostname"])
            check_type(argname="argument ssl_check_cert", value=ssl_check_cert, expected_type=type_hints["ssl_check_cert"])
            check_type(argname="argument ssl_ciphers", value=ssl_ciphers, expected_type=type_hints["ssl_ciphers"])
            check_type(argname="argument ssl_client_cert", value=ssl_client_cert, expected_type=type_hints["ssl_client_cert"])
            check_type(argname="argument ssl_client_key", value=ssl_client_key, expected_type=type_hints["ssl_client_key"])
            check_type(argname="argument ssl_sni_hostname", value=ssl_sni_hostname, expected_type=type_hints["ssl_sni_hostname"])
            check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
            check_type(argname="argument use_ssl", value=use_ssl, expected_type=type_hints["use_ssl"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "service_id": service_id,
            "version_id": version_id,
        }
        if address is not None:
            self._values["address"] = address
        if auto_loadbalance is not None:
            self._values["auto_loadbalance"] = auto_loadbalance
        if backend_name is not None:
            self._values["backend_name"] = backend_name
        if between_bytes_timeout is not None:
            self._values["between_bytes_timeout"] = between_bytes_timeout
        if client_cert is not None:
            self._values["client_cert"] = client_cert
        if comment is not None:
            self._values["comment"] = comment
        if connect_timeout is not None:
            self._values["connect_timeout"] = connect_timeout
        if created_at is not None:
            self._values["created_at"] = created_at
        if deleted_at is not None:
            self._values["deleted_at"] = deleted_at
        if first_byte_timeout is not None:
            self._values["first_byte_timeout"] = first_byte_timeout
        if healthcheck is not None:
            self._values["healthcheck"] = healthcheck
        if ipv4 is not None:
            self._values["ipv4"] = ipv4
        if ipv6 is not None:
            self._values["ipv6"] = ipv6
        if max_conn is not None:
            self._values["max_conn"] = max_conn
        if max_tls_version is not None:
            self._values["max_tls_version"] = max_tls_version
        if min_tls_version is not None:
            self._values["min_tls_version"] = min_tls_version
        if override_host is not None:
            self._values["override_host"] = override_host
        if port is not None:
            self._values["port"] = port
        if request_condition is not None:
            self._values["request_condition"] = request_condition
        if shield is not None:
            self._values["shield"] = shield
        if ssl_ca_cert is not None:
            self._values["ssl_ca_cert"] = ssl_ca_cert
        if ssl_cert_hostname is not None:
            self._values["ssl_cert_hostname"] = ssl_cert_hostname
        if ssl_check_cert is not None:
            self._values["ssl_check_cert"] = ssl_check_cert
        if ssl_ciphers is not None:
            self._values["ssl_ciphers"] = ssl_ciphers
        if ssl_client_cert is not None:
            self._values["ssl_client_cert"] = ssl_client_cert
        if ssl_client_key is not None:
            self._values["ssl_client_key"] = ssl_client_key
        if ssl_sni_hostname is not None:
            self._values["ssl_sni_hostname"] = ssl_sni_hostname
        if updated_at is not None:
            self._values["updated_at"] = updated_at
        if use_ssl is not None:
            self._values["use_ssl"] = use_ssl
        if version is not None:
            self._values["version"] = version
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :schema: CfnBackendProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_id(self) -> builtins.str:
        '''
        :schema: CfnBackendProps#ServiceId
        '''
        result = self._values.get("service_id")
        assert result is not None, "Required property 'service_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version_id(self) -> builtins.str:
        '''
        :schema: CfnBackendProps#VersionId
        '''
        result = self._values.get("version_id")
        assert result is not None, "Required property 'version_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnBackendProps#Address
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_loadbalance(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnBackendProps#AutoLoadbalance
        '''
        result = self._values.get("auto_loadbalance")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def backend_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnBackendProps#BackendName
        '''
        result = self._values.get("backend_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def between_bytes_timeout(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnBackendProps#BetweenBytesTimeout
        '''
        result = self._values.get("between_bytes_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_cert(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnBackendProps#ClientCert
        '''
        result = self._values.get("client_cert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnBackendProps#Comment
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connect_timeout(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnBackendProps#ConnectTimeout
        '''
        result = self._values.get("connect_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def created_at(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: CfnBackendProps#CreatedAt
        '''
        result = self._values.get("created_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def deleted_at(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: CfnBackendProps#DeletedAt
        '''
        result = self._values.get("deleted_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def first_byte_timeout(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnBackendProps#FirstByteTimeout
        '''
        result = self._values.get("first_byte_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def healthcheck(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnBackendProps#Healthcheck
        '''
        result = self._values.get("healthcheck")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv4(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnBackendProps#Ipv4
        '''
        result = self._values.get("ipv4")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnBackendProps#Ipv6
        '''
        result = self._values.get("ipv6")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_conn(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnBackendProps#MaxConn
        '''
        result = self._values.get("max_conn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_tls_version(self) -> typing.Optional["MaxTlsVersion"]:
        '''
        :schema: CfnBackendProps#MaxTlsVersion
        '''
        result = self._values.get("max_tls_version")
        return typing.cast(typing.Optional["MaxTlsVersion"], result)

    @builtins.property
    def min_tls_version(self) -> typing.Optional["MinTlsVersion"]:
        '''
        :schema: CfnBackendProps#MinTlsVersion
        '''
        result = self._values.get("min_tls_version")
        return typing.cast(typing.Optional["MinTlsVersion"], result)

    @builtins.property
    def override_host(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnBackendProps#OverrideHost
        '''
        result = self._values.get("override_host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnBackendProps#Port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def request_condition(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnBackendProps#RequestCondition
        '''
        result = self._values.get("request_condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shield(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnBackendProps#Shield
        '''
        result = self._values.get("shield")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_ca_cert(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnBackendProps#SslCaCert
        '''
        result = self._values.get("ssl_ca_cert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_cert_hostname(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnBackendProps#SslCertHostname
        '''
        result = self._values.get("ssl_cert_hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_check_cert(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnBackendProps#SslCheckCert
        '''
        result = self._values.get("ssl_check_cert")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ssl_ciphers(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnBackendProps#SslCiphers
        '''
        result = self._values.get("ssl_ciphers")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_client_cert(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnBackendProps#SslClientCert
        '''
        result = self._values.get("ssl_client_cert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_client_key(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnBackendProps#SslClientKey
        '''
        result = self._values.get("ssl_client_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_sni_hostname(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnBackendProps#SslSniHostname
        '''
        result = self._values.get("ssl_sni_hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def updated_at(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: CfnBackendProps#UpdatedAt
        '''
        result = self._values.get("updated_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def use_ssl(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnBackendProps#UseSsl
        '''
        result = self._values.get("use_ssl")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnBackendProps#Version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnBackendProps#Weight
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/fastly-services-backend.MaxTlsVersion")
class MaxTlsVersion(enum.Enum):
    '''Maximum allowed TLS version on SSL connections to this backend.

    If your backend server is not able to negotiate a connection meeting this constraint, a synthetic 503 error response will be generated.

    :schema: MaxTlsVersion
    '''

    VALUE_1 = "VALUE_1"
    '''1.'''
    VALUE_1_0 = "VALUE_1_0"
    '''1.0.'''
    VALUE_1_1 = "VALUE_1_1"
    '''1.1.'''
    VALUE_1_2 = "VALUE_1_2"
    '''1.2.'''
    VALUE_1_3 = "VALUE_1_3"
    '''1.3.'''


@jsii.enum(jsii_type="@cdk-cloudformation/fastly-services-backend.MinTlsVersion")
class MinTlsVersion(enum.Enum):
    '''Minimum allowed TLS version on SSL connections to this backend.

    If your backend server is not able to negotiate a connection meeting this constraint, a synthetic 503 error response will be generated.

    :schema: MinTlsVersion
    '''

    VALUE_1 = "VALUE_1"
    '''1.'''
    VALUE_1_0 = "VALUE_1_0"
    '''1.0.'''
    VALUE_1_1 = "VALUE_1_1"
    '''1.1.'''
    VALUE_1_2 = "VALUE_1_2"
    '''1.2.'''
    VALUE_1_3 = "VALUE_1_3"
    '''1.3.'''


__all__ = [
    "CfnBackend",
    "CfnBackendProps",
    "MaxTlsVersion",
    "MinTlsVersion",
]

publication.publish()

def _typecheckingstub__2bab8314cc72b3e625c440acdb8eb47a34a489fefd699be12e2248a57e9530b9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    service_id: builtins.str,
    version_id: builtins.str,
    address: typing.Optional[builtins.str] = None,
    auto_loadbalance: typing.Optional[builtins.bool] = None,
    backend_name: typing.Optional[builtins.str] = None,
    between_bytes_timeout: typing.Optional[jsii.Number] = None,
    client_cert: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    connect_timeout: typing.Optional[jsii.Number] = None,
    created_at: typing.Optional[datetime.datetime] = None,
    deleted_at: typing.Optional[datetime.datetime] = None,
    first_byte_timeout: typing.Optional[jsii.Number] = None,
    healthcheck: typing.Optional[builtins.str] = None,
    ipv4: typing.Optional[builtins.str] = None,
    ipv6: typing.Optional[builtins.str] = None,
    max_conn: typing.Optional[jsii.Number] = None,
    max_tls_version: typing.Optional[MaxTlsVersion] = None,
    min_tls_version: typing.Optional[MinTlsVersion] = None,
    override_host: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    request_condition: typing.Optional[builtins.str] = None,
    shield: typing.Optional[builtins.str] = None,
    ssl_ca_cert: typing.Optional[builtins.str] = None,
    ssl_cert_hostname: typing.Optional[builtins.str] = None,
    ssl_check_cert: typing.Optional[builtins.bool] = None,
    ssl_ciphers: typing.Optional[builtins.str] = None,
    ssl_client_cert: typing.Optional[builtins.str] = None,
    ssl_client_key: typing.Optional[builtins.str] = None,
    ssl_sni_hostname: typing.Optional[builtins.str] = None,
    updated_at: typing.Optional[datetime.datetime] = None,
    use_ssl: typing.Optional[builtins.bool] = None,
    version: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4db93d689717f71c83e958bc2b37aa81500ccdd08058b693d49f0cf2a8f90f7(
    *,
    name: builtins.str,
    service_id: builtins.str,
    version_id: builtins.str,
    address: typing.Optional[builtins.str] = None,
    auto_loadbalance: typing.Optional[builtins.bool] = None,
    backend_name: typing.Optional[builtins.str] = None,
    between_bytes_timeout: typing.Optional[jsii.Number] = None,
    client_cert: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    connect_timeout: typing.Optional[jsii.Number] = None,
    created_at: typing.Optional[datetime.datetime] = None,
    deleted_at: typing.Optional[datetime.datetime] = None,
    first_byte_timeout: typing.Optional[jsii.Number] = None,
    healthcheck: typing.Optional[builtins.str] = None,
    ipv4: typing.Optional[builtins.str] = None,
    ipv6: typing.Optional[builtins.str] = None,
    max_conn: typing.Optional[jsii.Number] = None,
    max_tls_version: typing.Optional[MaxTlsVersion] = None,
    min_tls_version: typing.Optional[MinTlsVersion] = None,
    override_host: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    request_condition: typing.Optional[builtins.str] = None,
    shield: typing.Optional[builtins.str] = None,
    ssl_ca_cert: typing.Optional[builtins.str] = None,
    ssl_cert_hostname: typing.Optional[builtins.str] = None,
    ssl_check_cert: typing.Optional[builtins.bool] = None,
    ssl_ciphers: typing.Optional[builtins.str] = None,
    ssl_client_cert: typing.Optional[builtins.str] = None,
    ssl_client_key: typing.Optional[builtins.str] = None,
    ssl_sni_hostname: typing.Optional[builtins.str] = None,
    updated_at: typing.Optional[datetime.datetime] = None,
    use_ssl: typing.Optional[builtins.bool] = None,
    version: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
