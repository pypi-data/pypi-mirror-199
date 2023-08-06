'''
# github-teams-team

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `GitHub::Teams::Team` v1.2.0.

## Description

Manage a team in Github

## References

* [Documentation](https://github.com/aws-ia/cloudformation-github-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-github-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name GitHub::Teams::Team \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/GitHub-Teams-Team \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `GitHub::Teams::Team`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fgithub-teams-team+v1.2.0).
* Issues related to `GitHub::Teams::Team` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-github-resource-providers).

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


class CfnTeam(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/github-teams-team.CfnTeam",
):
    '''A CloudFormation ``GitHub::Teams::Team``.

    :cloudformationResource: GitHub::Teams::Team
    :link: https://github.com/aws-ia/cloudformation-github-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        organization: builtins.str,
        description: typing.Optional[builtins.str] = None,
        privacy: typing.Optional["CfnTeamPropsPrivacy"] = None,
    ) -> None:
        '''Create a new ``GitHub::Teams::Team``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: Team name.
        :param organization: The Organization that the team will belong to.
        :param description: Describe the team.
        :param privacy: The privacy for the team - must be either secret or closed.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec3797549d39158e06ae1c74d2ed4af0afd9ae4374febfdf9170ecd5cb3c4a12)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTeamProps(
            name=name,
            organization=organization,
            description=description,
            privacy=privacy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrSlug")
    def attr_slug(self) -> builtins.str:
        '''Attribute ``GitHub::Teams::Team.Slug``.

        :link: https://github.com/aws-ia/cloudformation-github-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSlug"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnTeamProps":
        '''Resource props.'''
        return typing.cast("CfnTeamProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/github-teams-team.CfnTeamProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "organization": "organization",
        "description": "description",
        "privacy": "privacy",
    },
)
class CfnTeamProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        organization: builtins.str,
        description: typing.Optional[builtins.str] = None,
        privacy: typing.Optional["CfnTeamPropsPrivacy"] = None,
    ) -> None:
        '''Manage a team in Github.

        :param name: Team name.
        :param organization: The Organization that the team will belong to.
        :param description: Describe the team.
        :param privacy: The privacy for the team - must be either secret or closed.

        :schema: CfnTeamProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af3bbba1aefe9a31d2477c203b8e58bfba3a16c8f06cc58d74f0ed9f8eddfaa)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument privacy", value=privacy, expected_type=type_hints["privacy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "organization": organization,
        }
        if description is not None:
            self._values["description"] = description
        if privacy is not None:
            self._values["privacy"] = privacy

    @builtins.property
    def name(self) -> builtins.str:
        '''Team name.

        :schema: CfnTeamProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''The Organization that the team will belong to.

        :schema: CfnTeamProps#Organization
        '''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Describe the team.

        :schema: CfnTeamProps#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def privacy(self) -> typing.Optional["CfnTeamPropsPrivacy"]:
        '''The privacy for the team - must be either secret or closed.

        :schema: CfnTeamProps#Privacy
        '''
        result = self._values.get("privacy")
        return typing.cast(typing.Optional["CfnTeamPropsPrivacy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTeamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/github-teams-team.CfnTeamPropsPrivacy")
class CfnTeamPropsPrivacy(enum.Enum):
    '''The privacy for the team - must be either secret or closed.

    :schema: CfnTeamPropsPrivacy
    '''

    SECRET = "SECRET"
    '''secret.'''
    CLOSED = "CLOSED"
    '''closed.'''


__all__ = [
    "CfnTeam",
    "CfnTeamProps",
    "CfnTeamPropsPrivacy",
]

publication.publish()

def _typecheckingstub__ec3797549d39158e06ae1c74d2ed4af0afd9ae4374febfdf9170ecd5cb3c4a12(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    organization: builtins.str,
    description: typing.Optional[builtins.str] = None,
    privacy: typing.Optional[CfnTeamPropsPrivacy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af3bbba1aefe9a31d2477c203b8e58bfba3a16c8f06cc58d74f0ed9f8eddfaa(
    *,
    name: builtins.str,
    organization: builtins.str,
    description: typing.Optional[builtins.str] = None,
    privacy: typing.Optional[CfnTeamPropsPrivacy] = None,
) -> None:
    """Type checking stubs"""
    pass
