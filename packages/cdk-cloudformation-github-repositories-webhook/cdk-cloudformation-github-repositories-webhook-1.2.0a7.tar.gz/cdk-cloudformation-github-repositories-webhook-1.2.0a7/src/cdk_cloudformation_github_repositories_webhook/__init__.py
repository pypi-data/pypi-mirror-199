'''
# github-repositories-webhook

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `GitHub::Repositories::Webhook` v1.2.0.

## Description

Repositories can have multiple webhooks installed. Each webhook should have a unique config. Multiple webhooks can share the same config as long as those webhooks do not have any events that overlap.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-github-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-github-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name GitHub::Repositories::Webhook \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/GitHub-Repositories-Webhook \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `GitHub::Repositories::Webhook`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fgithub-repositories-webhook+v1.2.0).
* Issues related to `GitHub::Repositories::Webhook` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-github-resource-providers).

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


class CfnWebhook(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/github-repositories-webhook.CfnWebhook",
):
    '''A CloudFormation ``GitHub::Repositories::Webhook``.

    :cloudformationResource: GitHub::Repositories::Webhook
    :link: https://github.com/aws-ia/cloudformation-github-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        owner: builtins.str,
        active: typing.Optional[builtins.bool] = None,
        content_type: typing.Optional["CfnWebhookPropsContentType"] = None,
        events: typing.Optional[typing.Sequence[builtins.str]] = None,
        insecure_ssl: typing.Optional["CfnWebhookPropsInsecureSsl"] = None,
        name: typing.Optional["CfnWebhookPropsName"] = None,
        repository: typing.Optional[builtins.str] = None,
        secret: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``GitHub::Repositories::Webhook``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param owner: The organisation owner.
        :param active: Determines if notifications are sent when the webhook is triggered. Set to true to send notifications.
        :param content_type: The media type used to serialize the payloads. Supported values include json and form. The default is form.
        :param events: Determines what events the hook is triggered for.
        :param insecure_ssl: Determines whether the SSL certificate of the host for url will be verified when delivering payloads. Supported values include 0 (verification is performed) and 1 (verification is not performed). The default is 0. We strongly recommend not setting this to 1 as you are subject to man-in-the-middle and other attacks.
        :param name: Use web to create a webhook. Default: web. This parameter only accepts the value web.
        :param repository: The name of the repository. The name is not case sensitive.
        :param secret: If provided, the secret will be used as the key to generate the HMAC hex digest value for delivery signature headers.
        :param url: The URL to which the payloads will be delivered.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ce4650c9d6a4e375b6469eb74f2741695c2a14fc147b68c0db6823029caca8e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnWebhookProps(
            owner=owner,
            active=active,
            content_type=content_type,
            events=events,
            insecure_ssl=insecure_ssl,
            name=name,
            repository=repository,
            secret=secret,
            url=url,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> jsii.Number:
        '''Attribute ``GitHub::Repositories::Webhook.Id``.

        :link: https://github.com/aws-ia/cloudformation-github-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnWebhookProps":
        '''Resource props.'''
        return typing.cast("CfnWebhookProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/github-repositories-webhook.CfnWebhookProps",
    jsii_struct_bases=[],
    name_mapping={
        "owner": "owner",
        "active": "active",
        "content_type": "contentType",
        "events": "events",
        "insecure_ssl": "insecureSsl",
        "name": "name",
        "repository": "repository",
        "secret": "secret",
        "url": "url",
    },
)
class CfnWebhookProps:
    def __init__(
        self,
        *,
        owner: builtins.str,
        active: typing.Optional[builtins.bool] = None,
        content_type: typing.Optional["CfnWebhookPropsContentType"] = None,
        events: typing.Optional[typing.Sequence[builtins.str]] = None,
        insecure_ssl: typing.Optional["CfnWebhookPropsInsecureSsl"] = None,
        name: typing.Optional["CfnWebhookPropsName"] = None,
        repository: typing.Optional[builtins.str] = None,
        secret: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Repositories can have multiple webhooks installed.

        Each webhook should have a unique config. Multiple webhooks can share the same config as long as those webhooks do not have any events that overlap.

        :param owner: The organisation owner.
        :param active: Determines if notifications are sent when the webhook is triggered. Set to true to send notifications.
        :param content_type: The media type used to serialize the payloads. Supported values include json and form. The default is form.
        :param events: Determines what events the hook is triggered for.
        :param insecure_ssl: Determines whether the SSL certificate of the host for url will be verified when delivering payloads. Supported values include 0 (verification is performed) and 1 (verification is not performed). The default is 0. We strongly recommend not setting this to 1 as you are subject to man-in-the-middle and other attacks.
        :param name: Use web to create a webhook. Default: web. This parameter only accepts the value web.
        :param repository: The name of the repository. The name is not case sensitive.
        :param secret: If provided, the secret will be used as the key to generate the HMAC hex digest value for delivery signature headers.
        :param url: The URL to which the payloads will be delivered.

        :schema: CfnWebhookProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24059aa4b694e2ca77ee56b252b4874475d17185fd845235c73f6540f101caf3)
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument active", value=active, expected_type=type_hints["active"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument insecure_ssl", value=insecure_ssl, expected_type=type_hints["insecure_ssl"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "owner": owner,
        }
        if active is not None:
            self._values["active"] = active
        if content_type is not None:
            self._values["content_type"] = content_type
        if events is not None:
            self._values["events"] = events
        if insecure_ssl is not None:
            self._values["insecure_ssl"] = insecure_ssl
        if name is not None:
            self._values["name"] = name
        if repository is not None:
            self._values["repository"] = repository
        if secret is not None:
            self._values["secret"] = secret
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def owner(self) -> builtins.str:
        '''The organisation owner.

        :schema: CfnWebhookProps#Owner
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def active(self) -> typing.Optional[builtins.bool]:
        '''Determines if notifications are sent when the webhook is triggered.

        Set to true to send notifications.

        :schema: CfnWebhookProps#Active
        '''
        result = self._values.get("active")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def content_type(self) -> typing.Optional["CfnWebhookPropsContentType"]:
        '''The media type used to serialize the payloads.

        Supported values include json and form. The default is form.

        :schema: CfnWebhookProps#ContentType
        '''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional["CfnWebhookPropsContentType"], result)

    @builtins.property
    def events(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Determines what events the hook is triggered for.

        :schema: CfnWebhookProps#Events
        '''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def insecure_ssl(self) -> typing.Optional["CfnWebhookPropsInsecureSsl"]:
        '''Determines whether the SSL certificate of the host for url will be verified when delivering payloads.

        Supported values include 0 (verification is performed) and 1 (verification is not performed). The default is 0. We strongly recommend not setting this to 1 as you are subject to man-in-the-middle and other attacks.

        :schema: CfnWebhookProps#InsecureSsl
        '''
        result = self._values.get("insecure_ssl")
        return typing.cast(typing.Optional["CfnWebhookPropsInsecureSsl"], result)

    @builtins.property
    def name(self) -> typing.Optional["CfnWebhookPropsName"]:
        '''Use web to create a webhook.

        Default: web. This parameter only accepts the value web.

        :schema: CfnWebhookProps#Name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional["CfnWebhookPropsName"], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''The name of the repository.

        The name is not case sensitive.

        :schema: CfnWebhookProps#Repository
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret(self) -> typing.Optional[builtins.str]:
        '''If provided, the secret will be used as the key to generate the HMAC hex digest value for delivery signature headers.

        :schema: CfnWebhookProps#Secret
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''The URL to which the payloads will be delivered.

        :schema: CfnWebhookProps#Url
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWebhookProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/github-repositories-webhook.CfnWebhookPropsContentType"
)
class CfnWebhookPropsContentType(enum.Enum):
    '''The media type used to serialize the payloads.

    Supported values include json and form. The default is form.

    :schema: CfnWebhookPropsContentType
    '''

    FORM = "FORM"
    '''form.'''
    JSON = "JSON"
    '''json.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/github-repositories-webhook.CfnWebhookPropsInsecureSsl"
)
class CfnWebhookPropsInsecureSsl(enum.Enum):
    '''Determines whether the SSL certificate of the host for url will be verified when delivering payloads.

    Supported values include 0 (verification is performed) and 1 (verification is not performed). The default is 0. We strongly recommend not setting this to 1 as you are subject to man-in-the-middle and other attacks.

    :schema: CfnWebhookPropsInsecureSsl
    '''

    VALUE_0 = "VALUE_0"
    '''0.'''
    VALUE_1 = "VALUE_1"
    '''1.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/github-repositories-webhook.CfnWebhookPropsName"
)
class CfnWebhookPropsName(enum.Enum):
    '''Use web to create a webhook.

    Default: web. This parameter only accepts the value web.

    :schema: CfnWebhookPropsName
    '''

    WEB = "WEB"
    '''web.'''


__all__ = [
    "CfnWebhook",
    "CfnWebhookProps",
    "CfnWebhookPropsContentType",
    "CfnWebhookPropsInsecureSsl",
    "CfnWebhookPropsName",
]

publication.publish()

def _typecheckingstub__4ce4650c9d6a4e375b6469eb74f2741695c2a14fc147b68c0db6823029caca8e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    owner: builtins.str,
    active: typing.Optional[builtins.bool] = None,
    content_type: typing.Optional[CfnWebhookPropsContentType] = None,
    events: typing.Optional[typing.Sequence[builtins.str]] = None,
    insecure_ssl: typing.Optional[CfnWebhookPropsInsecureSsl] = None,
    name: typing.Optional[CfnWebhookPropsName] = None,
    repository: typing.Optional[builtins.str] = None,
    secret: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24059aa4b694e2ca77ee56b252b4874475d17185fd845235c73f6540f101caf3(
    *,
    owner: builtins.str,
    active: typing.Optional[builtins.bool] = None,
    content_type: typing.Optional[CfnWebhookPropsContentType] = None,
    events: typing.Optional[typing.Sequence[builtins.str]] = None,
    insecure_ssl: typing.Optional[CfnWebhookPropsInsecureSsl] = None,
    name: typing.Optional[CfnWebhookPropsName] = None,
    repository: typing.Optional[builtins.str] = None,
    secret: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
