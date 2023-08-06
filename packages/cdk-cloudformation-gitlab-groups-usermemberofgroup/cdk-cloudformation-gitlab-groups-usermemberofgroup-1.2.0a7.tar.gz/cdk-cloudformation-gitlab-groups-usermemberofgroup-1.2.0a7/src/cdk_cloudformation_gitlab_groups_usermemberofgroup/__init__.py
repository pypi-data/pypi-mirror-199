'''
# gitlab-groups-usermemberofgroup

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `GitLab::Groups::UserMemberOfGroup` v1.2.0.

## Description

Adds a user as a member of a GitLab group

## References

* [Documentation](https://github.com/aws-ia/cloudformation-gitlab-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name GitLab::Groups::UserMemberOfGroup \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/GitLab-Groups-UserMemberOfGroup \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `GitLab::Groups::UserMemberOfGroup`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fgitlab-groups-usermemberofgroup+v1.2.0).
* Issues related to `GitLab::Groups::UserMemberOfGroup` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-gitlab-resource-providers).

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


class CfnUserMemberOfGroup(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/gitlab-groups-usermemberofgroup.CfnUserMemberOfGroup",
):
    '''A CloudFormation ``GitLab::Groups::UserMemberOfGroup``.

    :cloudformationResource: GitLab::Groups::UserMemberOfGroup
    :link: https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_level: "CfnUserMemberOfGroupPropsAccessLevel",
        group_id: jsii.Number,
        user_id: typing.Optional[jsii.Number] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``GitLab::Groups::UserMemberOfGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param access_level: The access level to grant to this user in the group, e.g. 'Guest', 'Developer', or 'Maintainer'. Note the GitLab API may not allow all values.
        :param group_id: ID of the group to which the user should be added.
        :param user_id: ID (numeric) of the user to add to the group. Either this or Username but not both should be supplied.
        :param username: Username (handle, e.g. often written starting with '@') of the user to add to the group. Either this or the UserId but not both should be supplied.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20e1a8102ebb116812a039792796978c4a37447c38b08d12bcecfb1edd777626)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnUserMemberOfGroupProps(
            access_level=access_level,
            group_id=group_id,
            user_id=user_id,
            username=username,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrMembershipId")
    def attr_membership_id(self) -> builtins.str:
        '''Attribute ``GitLab::Groups::UserMemberOfGroup.MembershipId``.

        :link: https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMembershipId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnUserMemberOfGroupProps":
        '''Resource props.'''
        return typing.cast("CfnUserMemberOfGroupProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/gitlab-groups-usermemberofgroup.CfnUserMemberOfGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_level": "accessLevel",
        "group_id": "groupId",
        "user_id": "userId",
        "username": "username",
    },
)
class CfnUserMemberOfGroupProps:
    def __init__(
        self,
        *,
        access_level: "CfnUserMemberOfGroupPropsAccessLevel",
        group_id: jsii.Number,
        user_id: typing.Optional[jsii.Number] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Adds a user as a member of a GitLab group.

        :param access_level: The access level to grant to this user in the group, e.g. 'Guest', 'Developer', or 'Maintainer'. Note the GitLab API may not allow all values.
        :param group_id: ID of the group to which the user should be added.
        :param user_id: ID (numeric) of the user to add to the group. Either this or Username but not both should be supplied.
        :param username: Username (handle, e.g. often written starting with '@') of the user to add to the group. Either this or the UserId but not both should be supplied.

        :schema: CfnUserMemberOfGroupProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de2338efc99905f737c483e95889aa4f83e9edc866b111b1f9f52a86073d44cd)
            check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_level": access_level,
            "group_id": group_id,
        }
        if user_id is not None:
            self._values["user_id"] = user_id
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def access_level(self) -> "CfnUserMemberOfGroupPropsAccessLevel":
        '''The access level to grant to this user in the group, e.g. 'Guest', 'Developer', or 'Maintainer'. Note the GitLab API may not allow all values.

        :schema: CfnUserMemberOfGroupProps#AccessLevel
        '''
        result = self._values.get("access_level")
        assert result is not None, "Required property 'access_level' is missing"
        return typing.cast("CfnUserMemberOfGroupPropsAccessLevel", result)

    @builtins.property
    def group_id(self) -> jsii.Number:
        '''ID of the group to which the user should be added.

        :schema: CfnUserMemberOfGroupProps#GroupId
        '''
        result = self._values.get("group_id")
        assert result is not None, "Required property 'group_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def user_id(self) -> typing.Optional[jsii.Number]:
        '''ID (numeric) of the user to add to the group.

        Either this or Username but not both should be supplied.

        :schema: CfnUserMemberOfGroupProps#UserId
        '''
        result = self._values.get("user_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username (handle, e.g. often written starting with '@') of the user to add to the group. Either this or the UserId but not both should be supplied.

        :schema: CfnUserMemberOfGroupProps#Username
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserMemberOfGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/gitlab-groups-usermemberofgroup.CfnUserMemberOfGroupPropsAccessLevel"
)
class CfnUserMemberOfGroupPropsAccessLevel(enum.Enum):
    '''The access level to grant to this user in the group, e.g. 'Guest', 'Developer', or 'Maintainer'. Note the GitLab API may not allow all values.

    :schema: CfnUserMemberOfGroupPropsAccessLevel
    '''

    NONE = "NONE"
    '''None.'''
    MINIMAL_ACCESS = "MINIMAL_ACCESS"
    '''Minimal Access.'''
    GUEST = "GUEST"
    '''Guest.'''
    REPORTER = "REPORTER"
    '''Reporter.'''
    DEVELOPER = "DEVELOPER"
    '''Developer.'''
    MAINTAINER = "MAINTAINER"
    '''Maintainer.'''
    OWNER = "OWNER"
    '''Owner.'''
    ADMIN = "ADMIN"
    '''Admin.'''


__all__ = [
    "CfnUserMemberOfGroup",
    "CfnUserMemberOfGroupProps",
    "CfnUserMemberOfGroupPropsAccessLevel",
]

publication.publish()

def _typecheckingstub__20e1a8102ebb116812a039792796978c4a37447c38b08d12bcecfb1edd777626(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_level: CfnUserMemberOfGroupPropsAccessLevel,
    group_id: jsii.Number,
    user_id: typing.Optional[jsii.Number] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de2338efc99905f737c483e95889aa4f83e9edc866b111b1f9f52a86073d44cd(
    *,
    access_level: CfnUserMemberOfGroupPropsAccessLevel,
    group_id: jsii.Number,
    user_id: typing.Optional[jsii.Number] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
