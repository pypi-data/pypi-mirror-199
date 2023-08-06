'''
# fastly-services-healthcheck

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Fastly::Services::Healthcheck` v1.2.0.

## Description

Manage a Fastly service health check.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-fastly-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-fastly-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Fastly::Services::Healthcheck \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Fastly-Services-Healthcheck \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Fastly::Services::Healthcheck`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Ffastly-services-healthcheck+v1.2.0).
* Issues related to `Fastly::Services::Healthcheck` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-fastly-resource-providers).

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


class CfnHealthcheck(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/fastly-services-healthcheck.CfnHealthcheck",
):
    '''A CloudFormation ``Fastly::Services::Healthcheck``.

    :cloudformationResource: Fastly::Services::Healthcheck
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
        check_interval: typing.Optional[jsii.Number] = None,
        comment: typing.Optional[builtins.str] = None,
        created_at: typing.Optional[datetime.datetime] = None,
        deleted_at: typing.Optional[datetime.datetime] = None,
        expected_response: typing.Optional[jsii.Number] = None,
        healthcheck_name: typing.Optional[builtins.str] = None,
        host: typing.Optional[builtins.str] = None,
        http_version: typing.Optional["HttpVersion"] = None,
        initial: typing.Optional[jsii.Number] = None,
        method: typing.Optional["Method"] = None,
        path: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[jsii.Number] = None,
        updated_at: typing.Optional[datetime.datetime] = None,
        version: typing.Optional[builtins.str] = None,
        window: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``Fastly::Services::Healthcheck``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: 
        :param service_id: 
        :param version_id: 
        :param check_interval: 
        :param comment: 
        :param created_at: 
        :param deleted_at: 
        :param expected_response: 
        :param healthcheck_name: 
        :param host: 
        :param http_version: 
        :param initial: 
        :param method: 
        :param path: 
        :param threshold: 
        :param timeout: 
        :param updated_at: 
        :param version: 
        :param window: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8214e9f97ab2c375cf63709bec5a81eaa18c411b902712b53a0340450dea5692)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnHealthcheckProps(
            name=name,
            service_id=service_id,
            version_id=version_id,
            check_interval=check_interval,
            comment=comment,
            created_at=created_at,
            deleted_at=deleted_at,
            expected_response=expected_response,
            healthcheck_name=healthcheck_name,
            host=host,
            http_version=http_version,
            initial=initial,
            method=method,
            path=path,
            threshold=threshold,
            timeout=timeout,
            updated_at=updated_at,
            version=version,
            window=window,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnHealthcheckProps":
        '''Resource props.'''
        return typing.cast("CfnHealthcheckProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/fastly-services-healthcheck.CfnHealthcheckProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "service_id": "serviceId",
        "version_id": "versionId",
        "check_interval": "checkInterval",
        "comment": "comment",
        "created_at": "createdAt",
        "deleted_at": "deletedAt",
        "expected_response": "expectedResponse",
        "healthcheck_name": "healthcheckName",
        "host": "host",
        "http_version": "httpVersion",
        "initial": "initial",
        "method": "method",
        "path": "path",
        "threshold": "threshold",
        "timeout": "timeout",
        "updated_at": "updatedAt",
        "version": "version",
        "window": "window",
    },
)
class CfnHealthcheckProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        service_id: builtins.str,
        version_id: builtins.str,
        check_interval: typing.Optional[jsii.Number] = None,
        comment: typing.Optional[builtins.str] = None,
        created_at: typing.Optional[datetime.datetime] = None,
        deleted_at: typing.Optional[datetime.datetime] = None,
        expected_response: typing.Optional[jsii.Number] = None,
        healthcheck_name: typing.Optional[builtins.str] = None,
        host: typing.Optional[builtins.str] = None,
        http_version: typing.Optional["HttpVersion"] = None,
        initial: typing.Optional[jsii.Number] = None,
        method: typing.Optional["Method"] = None,
        path: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[jsii.Number] = None,
        updated_at: typing.Optional[datetime.datetime] = None,
        version: typing.Optional[builtins.str] = None,
        window: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Manage a Fastly service health check.

        :param name: 
        :param service_id: 
        :param version_id: 
        :param check_interval: 
        :param comment: 
        :param created_at: 
        :param deleted_at: 
        :param expected_response: 
        :param healthcheck_name: 
        :param host: 
        :param http_version: 
        :param initial: 
        :param method: 
        :param path: 
        :param threshold: 
        :param timeout: 
        :param updated_at: 
        :param version: 
        :param window: 

        :schema: CfnHealthcheckProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df174018e18eefb77ea6c4bff6119fba4a38b3c831dbd20cba894f9d61abe0ca)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_id", value=service_id, expected_type=type_hints["service_id"])
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
            check_type(argname="argument check_interval", value=check_interval, expected_type=type_hints["check_interval"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
            check_type(argname="argument deleted_at", value=deleted_at, expected_type=type_hints["deleted_at"])
            check_type(argname="argument expected_response", value=expected_response, expected_type=type_hints["expected_response"])
            check_type(argname="argument healthcheck_name", value=healthcheck_name, expected_type=type_hints["healthcheck_name"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument http_version", value=http_version, expected_type=type_hints["http_version"])
            check_type(argname="argument initial", value=initial, expected_type=type_hints["initial"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument window", value=window, expected_type=type_hints["window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "service_id": service_id,
            "version_id": version_id,
        }
        if check_interval is not None:
            self._values["check_interval"] = check_interval
        if comment is not None:
            self._values["comment"] = comment
        if created_at is not None:
            self._values["created_at"] = created_at
        if deleted_at is not None:
            self._values["deleted_at"] = deleted_at
        if expected_response is not None:
            self._values["expected_response"] = expected_response
        if healthcheck_name is not None:
            self._values["healthcheck_name"] = healthcheck_name
        if host is not None:
            self._values["host"] = host
        if http_version is not None:
            self._values["http_version"] = http_version
        if initial is not None:
            self._values["initial"] = initial
        if method is not None:
            self._values["method"] = method
        if path is not None:
            self._values["path"] = path
        if threshold is not None:
            self._values["threshold"] = threshold
        if timeout is not None:
            self._values["timeout"] = timeout
        if updated_at is not None:
            self._values["updated_at"] = updated_at
        if version is not None:
            self._values["version"] = version
        if window is not None:
            self._values["window"] = window

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :schema: CfnHealthcheckProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_id(self) -> builtins.str:
        '''
        :schema: CfnHealthcheckProps#ServiceId
        '''
        result = self._values.get("service_id")
        assert result is not None, "Required property 'service_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version_id(self) -> builtins.str:
        '''
        :schema: CfnHealthcheckProps#VersionId
        '''
        result = self._values.get("version_id")
        assert result is not None, "Required property 'version_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def check_interval(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnHealthcheckProps#CheckInterval
        '''
        result = self._values.get("check_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnHealthcheckProps#Comment
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def created_at(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: CfnHealthcheckProps#CreatedAt
        '''
        result = self._values.get("created_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def deleted_at(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: CfnHealthcheckProps#DeletedAt
        '''
        result = self._values.get("deleted_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def expected_response(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnHealthcheckProps#ExpectedResponse
        '''
        result = self._values.get("expected_response")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def healthcheck_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnHealthcheckProps#HealthcheckName
        '''
        result = self._values.get("healthcheck_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnHealthcheckProps#Host
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_version(self) -> typing.Optional["HttpVersion"]:
        '''
        :schema: CfnHealthcheckProps#HttpVersion
        '''
        result = self._values.get("http_version")
        return typing.cast(typing.Optional["HttpVersion"], result)

    @builtins.property
    def initial(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnHealthcheckProps#Initial
        '''
        result = self._values.get("initial")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def method(self) -> typing.Optional["Method"]:
        '''
        :schema: CfnHealthcheckProps#Method
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional["Method"], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnHealthcheckProps#Path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnHealthcheckProps#Threshold
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnHealthcheckProps#Timeout
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def updated_at(self) -> typing.Optional[datetime.datetime]:
        '''
        :schema: CfnHealthcheckProps#UpdatedAt
        '''
        result = self._values.get("updated_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnHealthcheckProps#Version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def window(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnHealthcheckProps#Window
        '''
        result = self._values.get("window")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHealthcheckProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/fastly-services-healthcheck.HttpVersion")
class HttpVersion(enum.Enum):
    '''Whether to use version 1.0 or 1.1 HTTP.

    :schema: HttpVersion
    '''

    VALUE_1_0 = "VALUE_1_0"
    '''1.0.'''
    VALUE_1_1 = "VALUE_1_1"
    '''1.1.'''


@jsii.enum(jsii_type="@cdk-cloudformation/fastly-services-healthcheck.Method")
class Method(enum.Enum):
    '''Which HTTP method to use.

    :schema: Method
    '''

    HEAD = "HEAD"
    '''HEAD.'''
    GET = "GET"
    '''GET.'''
    POST = "POST"
    '''POST.'''


__all__ = [
    "CfnHealthcheck",
    "CfnHealthcheckProps",
    "HttpVersion",
    "Method",
]

publication.publish()

def _typecheckingstub__8214e9f97ab2c375cf63709bec5a81eaa18c411b902712b53a0340450dea5692(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    service_id: builtins.str,
    version_id: builtins.str,
    check_interval: typing.Optional[jsii.Number] = None,
    comment: typing.Optional[builtins.str] = None,
    created_at: typing.Optional[datetime.datetime] = None,
    deleted_at: typing.Optional[datetime.datetime] = None,
    expected_response: typing.Optional[jsii.Number] = None,
    healthcheck_name: typing.Optional[builtins.str] = None,
    host: typing.Optional[builtins.str] = None,
    http_version: typing.Optional[HttpVersion] = None,
    initial: typing.Optional[jsii.Number] = None,
    method: typing.Optional[Method] = None,
    path: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[jsii.Number] = None,
    updated_at: typing.Optional[datetime.datetime] = None,
    version: typing.Optional[builtins.str] = None,
    window: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df174018e18eefb77ea6c4bff6119fba4a38b3c831dbd20cba894f9d61abe0ca(
    *,
    name: builtins.str,
    service_id: builtins.str,
    version_id: builtins.str,
    check_interval: typing.Optional[jsii.Number] = None,
    comment: typing.Optional[builtins.str] = None,
    created_at: typing.Optional[datetime.datetime] = None,
    deleted_at: typing.Optional[datetime.datetime] = None,
    expected_response: typing.Optional[jsii.Number] = None,
    healthcheck_name: typing.Optional[builtins.str] = None,
    host: typing.Optional[builtins.str] = None,
    http_version: typing.Optional[HttpVersion] = None,
    initial: typing.Optional[jsii.Number] = None,
    method: typing.Optional[Method] = None,
    path: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[jsii.Number] = None,
    updated_at: typing.Optional[datetime.datetime] = None,
    version: typing.Optional[builtins.str] = None,
    window: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
