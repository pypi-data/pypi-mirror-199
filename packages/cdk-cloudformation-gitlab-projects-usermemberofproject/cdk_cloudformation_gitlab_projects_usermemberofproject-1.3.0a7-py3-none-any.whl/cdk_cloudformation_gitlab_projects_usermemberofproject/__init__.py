'''
# gitlab-projects-usermemberofproject

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `GitLab::Projects::UserMemberOfProject` v1.3.0.

## Description

Adds a user as a member of a GitLab project

## References

* [Documentation](https://github.com/aws-ia/cloudformation-gitlab-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name GitLab::Projects::UserMemberOfProject \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/GitLab-Projects-UserMemberOfProject \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `GitLab::Projects::UserMemberOfProject`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fgitlab-projects-usermemberofproject+v1.3.0).
* Issues related to `GitLab::Projects::UserMemberOfProject` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-gitlab-resource-providers).

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


class CfnUserMemberOfProject(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/gitlab-projects-usermemberofproject.CfnUserMemberOfProject",
):
    '''A CloudFormation ``GitLab::Projects::UserMemberOfProject``.

    :cloudformationResource: GitLab::Projects::UserMemberOfProject
    :link: https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_level: "CfnUserMemberOfProjectPropsAccessLevel",
        project_id: jsii.Number,
        user_id: typing.Optional[jsii.Number] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``GitLab::Projects::UserMemberOfProject``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param access_level: The access level to grant to this user on the project, e.g. 'Guest', 'Developer', or 'Maintainer'. Note the GitLab API may not allow all values.
        :param project_id: ID of the project to which the user should be added.
        :param user_id: ID (numeric) of the user to add to the project. Either this or Username but not both should be supplied.
        :param username: Username (handle, e.g. often written starting with '@') of the user to add to the project. Either this or the UserId but not both should be supplied.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac74fd32c65f184f563c3a46a66141754b8931fb3611fe96fbf541646606f238)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnUserMemberOfProjectProps(
            access_level=access_level,
            project_id=project_id,
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
        '''Attribute ``GitLab::Projects::UserMemberOfProject.MembershipId``.

        :link: https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMembershipId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnUserMemberOfProjectProps":
        '''Resource props.'''
        return typing.cast("CfnUserMemberOfProjectProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/gitlab-projects-usermemberofproject.CfnUserMemberOfProjectProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_level": "accessLevel",
        "project_id": "projectId",
        "user_id": "userId",
        "username": "username",
    },
)
class CfnUserMemberOfProjectProps:
    def __init__(
        self,
        *,
        access_level: "CfnUserMemberOfProjectPropsAccessLevel",
        project_id: jsii.Number,
        user_id: typing.Optional[jsii.Number] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Adds a user as a member of a GitLab project.

        :param access_level: The access level to grant to this user on the project, e.g. 'Guest', 'Developer', or 'Maintainer'. Note the GitLab API may not allow all values.
        :param project_id: ID of the project to which the user should be added.
        :param user_id: ID (numeric) of the user to add to the project. Either this or Username but not both should be supplied.
        :param username: Username (handle, e.g. often written starting with '@') of the user to add to the project. Either this or the UserId but not both should be supplied.

        :schema: CfnUserMemberOfProjectProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fcd95904d6b9a5d095a9b9d7f11a017b46c64280b04925b20e949485f5c983e)
            check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_level": access_level,
            "project_id": project_id,
        }
        if user_id is not None:
            self._values["user_id"] = user_id
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def access_level(self) -> "CfnUserMemberOfProjectPropsAccessLevel":
        '''The access level to grant to this user on the project, e.g. 'Guest', 'Developer', or 'Maintainer'. Note the GitLab API may not allow all values.

        :schema: CfnUserMemberOfProjectProps#AccessLevel
        '''
        result = self._values.get("access_level")
        assert result is not None, "Required property 'access_level' is missing"
        return typing.cast("CfnUserMemberOfProjectPropsAccessLevel", result)

    @builtins.property
    def project_id(self) -> jsii.Number:
        '''ID of the project to which the user should be added.

        :schema: CfnUserMemberOfProjectProps#ProjectId
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def user_id(self) -> typing.Optional[jsii.Number]:
        '''ID (numeric) of the user to add to the project.

        Either this or Username but not both should be supplied.

        :schema: CfnUserMemberOfProjectProps#UserId
        '''
        result = self._values.get("user_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username (handle, e.g. often written starting with '@') of the user to add to the project. Either this or the UserId but not both should be supplied.

        :schema: CfnUserMemberOfProjectProps#Username
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserMemberOfProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/gitlab-projects-usermemberofproject.CfnUserMemberOfProjectPropsAccessLevel"
)
class CfnUserMemberOfProjectPropsAccessLevel(enum.Enum):
    '''The access level to grant to this user on the project, e.g. 'Guest', 'Developer', or 'Maintainer'. Note the GitLab API may not allow all values.

    :schema: CfnUserMemberOfProjectPropsAccessLevel
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
    "CfnUserMemberOfProject",
    "CfnUserMemberOfProjectProps",
    "CfnUserMemberOfProjectPropsAccessLevel",
]

publication.publish()

def _typecheckingstub__ac74fd32c65f184f563c3a46a66141754b8931fb3611fe96fbf541646606f238(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_level: CfnUserMemberOfProjectPropsAccessLevel,
    project_id: jsii.Number,
    user_id: typing.Optional[jsii.Number] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fcd95904d6b9a5d095a9b9d7f11a017b46c64280b04925b20e949485f5c983e(
    *,
    access_level: CfnUserMemberOfProjectPropsAccessLevel,
    project_id: jsii.Number,
    user_id: typing.Optional[jsii.Number] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
