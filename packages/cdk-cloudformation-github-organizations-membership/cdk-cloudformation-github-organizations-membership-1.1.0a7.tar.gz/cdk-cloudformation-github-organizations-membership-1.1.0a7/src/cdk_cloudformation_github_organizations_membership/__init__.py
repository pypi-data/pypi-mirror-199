'''
# github-organizations-membership

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `GitHub::Organizations::Membership` v1.1.0.

## Description

Add people to an organization. Will create an invite and user will only become a member once they accept this invite.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-github-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-github-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name GitHub::Organizations::Membership \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/GitHub-Organizations-Membership \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `GitHub::Organizations::Membership`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fgithub-organizations-membership+v1.1.0).
* Issues related to `GitHub::Organizations::Membership` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-github-resource-providers).

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
    jsii_type="@cdk-cloudformation/github-organizations-membership.CfnMembership",
):
    '''A CloudFormation ``GitHub::Organizations::Membership``.

    :cloudformationResource: GitHub::Organizations::Membership
    :link: https://github.com/aws-ia/cloudformation-github-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        organization: builtins.str,
        username: builtins.str,
        role: typing.Optional["CfnMembershipPropsRole"] = None,
    ) -> None:
        '''Create a new ``GitHub::Organizations::Membership``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param organization: The Organization the user is being added to.
        :param username: The handle for the GitHub user account.
        :param role: The role for the new member.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ebef1a56123eb6e6883684c4acf308eb2bff307253cf8188825b3764829a80a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMembershipProps(
            organization=organization, username=username, role=role
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnMembershipProps":
        '''Resource props.'''
        return typing.cast("CfnMembershipProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/github-organizations-membership.CfnMembershipProps",
    jsii_struct_bases=[],
    name_mapping={
        "organization": "organization",
        "username": "username",
        "role": "role",
    },
)
class CfnMembershipProps:
    def __init__(
        self,
        *,
        organization: builtins.str,
        username: builtins.str,
        role: typing.Optional["CfnMembershipPropsRole"] = None,
    ) -> None:
        '''Add people to an organization.

        Will create an invite and user will only become a member once they accept this invite.

        :param organization: The Organization the user is being added to.
        :param username: The handle for the GitHub user account.
        :param role: The role for the new member.

        :schema: CfnMembershipProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c335bc9bba67204c80e73759543a016574cc6a709bc74a8cbe1f319771aef0e3)
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "organization": organization,
            "username": username,
        }
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def organization(self) -> builtins.str:
        '''The Organization the user is being added to.

        :schema: CfnMembershipProps#Organization
        '''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''The handle for the GitHub user account.

        :schema: CfnMembershipProps#Username
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> typing.Optional["CfnMembershipPropsRole"]:
        '''The role for the new member.

        :schema: CfnMembershipProps#Role
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional["CfnMembershipPropsRole"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMembershipProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/github-organizations-membership.CfnMembershipPropsRole"
)
class CfnMembershipPropsRole(enum.Enum):
    '''The role for the new member.

    :schema: CfnMembershipPropsRole
    '''

    ADMIN = "ADMIN"
    '''admin.'''
    MEMBER = "MEMBER"
    '''member.'''


__all__ = [
    "CfnMembership",
    "CfnMembershipProps",
    "CfnMembershipPropsRole",
]

publication.publish()

def _typecheckingstub__3ebef1a56123eb6e6883684c4acf308eb2bff307253cf8188825b3764829a80a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    organization: builtins.str,
    username: builtins.str,
    role: typing.Optional[CfnMembershipPropsRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c335bc9bba67204c80e73759543a016574cc6a709bc74a8cbe1f319771aef0e3(
    *,
    organization: builtins.str,
    username: builtins.str,
    role: typing.Optional[CfnMembershipPropsRole] = None,
) -> None:
    """Type checking stubs"""
    pass
