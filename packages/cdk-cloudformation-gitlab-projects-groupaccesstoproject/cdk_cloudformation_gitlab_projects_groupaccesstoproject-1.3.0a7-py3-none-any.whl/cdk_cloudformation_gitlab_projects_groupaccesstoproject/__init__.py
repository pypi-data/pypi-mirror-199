'''
# gitlab-projects-groupaccesstoproject

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `GitLab::Projects::GroupAccessToProject` v1.3.0.

## Description

Adds a group as a member of a GitLab project

## References

* [Documentation](https://github.com/aws-ia/cloudformation-gitlab-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name GitLab::Projects::GroupAccessToProject \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/GitLab-Projects-GroupAccessToProject \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `GitLab::Projects::GroupAccessToProject`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fgitlab-projects-groupaccesstoproject+v1.3.0).
* Issues related to `GitLab::Projects::GroupAccessToProject` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-gitlab-resource-providers).

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


class CfnGroupAccessToProject(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/gitlab-projects-groupaccesstoproject.CfnGroupAccessToProject",
):
    '''A CloudFormation ``GitLab::Projects::GroupAccessToProject``.

    :cloudformationResource: GitLab::Projects::GroupAccessToProject
    :link: https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_level: "CfnGroupAccessToProjectPropsAccessLevel",
        group_id: jsii.Number,
        project_id: jsii.Number,
    ) -> None:
        '''Create a new ``GitLab::Projects::GroupAccessToProject``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param access_level: The access level to grant to this group for the project, e.g. 'guest', 'developer', or 'maintainer'. Note the GitLab API may not allow all values.
        :param group_id: ID of the group which should be added to the project.
        :param project_id: ID of the project to which the group should be added.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__756f96d18ddd7ff186be35aea7662bfe871a1b0b78759ce7c428dda2dfa9e1bf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGroupAccessToProjectProps(
            access_level=access_level, group_id=group_id, project_id=project_id
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
        '''Attribute ``GitLab::Projects::GroupAccessToProject.MembershipId``.

        :link: https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMembershipId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnGroupAccessToProjectProps":
        '''Resource props.'''
        return typing.cast("CfnGroupAccessToProjectProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/gitlab-projects-groupaccesstoproject.CfnGroupAccessToProjectProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_level": "accessLevel",
        "group_id": "groupId",
        "project_id": "projectId",
    },
)
class CfnGroupAccessToProjectProps:
    def __init__(
        self,
        *,
        access_level: "CfnGroupAccessToProjectPropsAccessLevel",
        group_id: jsii.Number,
        project_id: jsii.Number,
    ) -> None:
        '''Adds a group as a member of a GitLab project.

        :param access_level: The access level to grant to this group for the project, e.g. 'guest', 'developer', or 'maintainer'. Note the GitLab API may not allow all values.
        :param group_id: ID of the group which should be added to the project.
        :param project_id: ID of the project to which the group should be added.

        :schema: CfnGroupAccessToProjectProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d927bd845d0271f9c04062da6afd48cd0faefb8e5058109a4c9b6b246bb8d32)
            check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_level": access_level,
            "group_id": group_id,
            "project_id": project_id,
        }

    @builtins.property
    def access_level(self) -> "CfnGroupAccessToProjectPropsAccessLevel":
        '''The access level to grant to this group for the project, e.g. 'guest', 'developer', or 'maintainer'. Note the GitLab API may not allow all values.

        :schema: CfnGroupAccessToProjectProps#AccessLevel
        '''
        result = self._values.get("access_level")
        assert result is not None, "Required property 'access_level' is missing"
        return typing.cast("CfnGroupAccessToProjectPropsAccessLevel", result)

    @builtins.property
    def group_id(self) -> jsii.Number:
        '''ID of the group which should be added to the project.

        :schema: CfnGroupAccessToProjectProps#GroupId
        '''
        result = self._values.get("group_id")
        assert result is not None, "Required property 'group_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def project_id(self) -> jsii.Number:
        '''ID of the project to which the group should be added.

        :schema: CfnGroupAccessToProjectProps#ProjectId
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupAccessToProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/gitlab-projects-groupaccesstoproject.CfnGroupAccessToProjectPropsAccessLevel"
)
class CfnGroupAccessToProjectPropsAccessLevel(enum.Enum):
    '''The access level to grant to this group for the project, e.g. 'guest', 'developer', or 'maintainer'. Note the GitLab API may not allow all values.

    :schema: CfnGroupAccessToProjectPropsAccessLevel
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
    "CfnGroupAccessToProject",
    "CfnGroupAccessToProjectProps",
    "CfnGroupAccessToProjectPropsAccessLevel",
]

publication.publish()

def _typecheckingstub__756f96d18ddd7ff186be35aea7662bfe871a1b0b78759ce7c428dda2dfa9e1bf(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_level: CfnGroupAccessToProjectPropsAccessLevel,
    group_id: jsii.Number,
    project_id: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d927bd845d0271f9c04062da6afd48cd0faefb8e5058109a4c9b6b246bb8d32(
    *,
    access_level: CfnGroupAccessToProjectPropsAccessLevel,
    group_id: jsii.Number,
    project_id: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass
