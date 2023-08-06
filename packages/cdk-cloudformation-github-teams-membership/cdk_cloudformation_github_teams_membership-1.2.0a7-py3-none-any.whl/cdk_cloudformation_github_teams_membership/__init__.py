'''
# github-teams-membership

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `GitHub::Teams::Membership` v1.2.0.

## Description

Manages people's membership to GitHub teams

## References

* [Documentation](https://github.com/aws-ia/cloudformation-github-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-github-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name GitHub::Teams::Membership \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/GitHub-Teams-Membership \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `GitHub::Teams::Membership`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fgithub-teams-membership+v1.2.0).
* Issues related to `GitHub::Teams::Membership` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-github-resource-providers).

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


class CfnMembership(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/github-teams-membership.CfnMembership",
):
    '''A CloudFormation ``GitHub::Teams::Membership``.

    :cloudformationResource: GitHub::Teams::Membership
    :link: https://github.com/aws-ia/cloudformation-github-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        org: builtins.str,
        team_slug: builtins.str,
        role: typing.Optional["CfnMembershipPropsRole"] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``GitHub::Teams::Membership``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param org: The organization name. The name is not case sensitive. If not specified, then the managed repository will be within the currently logged-in user account.
        :param team_slug: TThe slug of the team name.
        :param role: The handle for the GitHub user account.
        :param username: The handle for the GitHub user account.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24bd53073ebaec93aff5ed2b51304f6d469c2bc75fc727f688d37b1de095a2d8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMembershipProps(
            org=org, team_slug=team_slug, role=role, username=username
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''Attribute ``GitHub::Teams::Membership.State``.

        :link: https://github.com/aws-ia/cloudformation-github-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnMembershipProps":
        '''Resource props.'''
        return typing.cast("CfnMembershipProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/github-teams-membership.CfnMembershipProps",
    jsii_struct_bases=[],
    name_mapping={
        "org": "org",
        "team_slug": "teamSlug",
        "role": "role",
        "username": "username",
    },
)
class CfnMembershipProps:
    def __init__(
        self,
        *,
        org: builtins.str,
        team_slug: builtins.str,
        role: typing.Optional["CfnMembershipPropsRole"] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Manages people's membership to GitHub teams.

        :param org: The organization name. The name is not case sensitive. If not specified, then the managed repository will be within the currently logged-in user account.
        :param team_slug: TThe slug of the team name.
        :param role: The handle for the GitHub user account.
        :param username: The handle for the GitHub user account.

        :schema: CfnMembershipProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8944343b892a0b92efc218b100d1f9b30161fe7de9cebe0b1d0dc28f4fbc475)
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument team_slug", value=team_slug, expected_type=type_hints["team_slug"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "org": org,
            "team_slug": team_slug,
        }
        if role is not None:
            self._values["role"] = role
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def org(self) -> builtins.str:
        '''The organization name.

        The name is not case sensitive. If not specified, then the managed repository will be within the currently logged-in user account.

        :schema: CfnMembershipProps#Org
        '''
        result = self._values.get("org")
        assert result is not None, "Required property 'org' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def team_slug(self) -> builtins.str:
        '''TThe slug of the team name.

        :schema: CfnMembershipProps#TeamSlug
        '''
        result = self._values.get("team_slug")
        assert result is not None, "Required property 'team_slug' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> typing.Optional["CfnMembershipPropsRole"]:
        '''The handle for the GitHub user account.

        :schema: CfnMembershipProps#Role
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional["CfnMembershipPropsRole"], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The handle for the GitHub user account.

        :schema: CfnMembershipProps#Username
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMembershipProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/github-teams-membership.CfnMembershipPropsRole"
)
class CfnMembershipPropsRole(enum.Enum):
    '''The handle for the GitHub user account.

    :schema: CfnMembershipPropsRole
    '''

    MEMBER = "MEMBER"
    '''member.'''
    MAINTAINER = "MAINTAINER"
    '''maintainer.'''


__all__ = [
    "CfnMembership",
    "CfnMembershipProps",
    "CfnMembershipPropsRole",
]

publication.publish()

def _typecheckingstub__24bd53073ebaec93aff5ed2b51304f6d469c2bc75fc727f688d37b1de095a2d8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    org: builtins.str,
    team_slug: builtins.str,
    role: typing.Optional[CfnMembershipPropsRole] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8944343b892a0b92efc218b100d1f9b30161fe7de9cebe0b1d0dc28f4fbc475(
    *,
    org: builtins.str,
    team_slug: builtins.str,
    role: typing.Optional[CfnMembershipPropsRole] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
