'''
# gitlab-groups-groupaccesstogroup

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `GitLab::Groups::GroupAccessToGroup` v1.2.0.

## Description

Adds a group as a member of another GitLab group

## References

* [Documentation](https://github.com/aws-ia/cloudformation-gitlab-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name GitLab::Groups::GroupAccessToGroup \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/GitLab-Groups-GroupAccessToGroup \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `GitLab::Groups::GroupAccessToGroup`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fgitlab-groups-groupaccesstogroup+v1.2.0).
* Issues related to `GitLab::Groups::GroupAccessToGroup` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-gitlab-resource-providers).

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


class CfnGroupAccessToGroup(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/gitlab-groups-groupaccesstogroup.CfnGroupAccessToGroup",
):
    '''A CloudFormation ``GitLab::Groups::GroupAccessToGroup``.

    :cloudformationResource: GitLab::Groups::GroupAccessToGroup
    :link: https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_level: "CfnGroupAccessToGroupPropsAccessLevel",
        shared_group_id: jsii.Number,
        shared_with_group_id: jsii.Number,
    ) -> None:
        '''Create a new ``GitLab::Groups::GroupAccessToGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param access_level: The access level to grant to the shared-with group for acessing the shared group, e.g. 'Guest', 'Developer', or 'Maintainer'. Note the GitLab API may not allow all values.
        :param shared_group_id: ID of the group which should be shared, i.e. the group to which access is being granted.
        :param shared_with_group_id: ID of the group to share with, i.e. the group being given access to another group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9135a7db21f79d3970975956d6c47bb71bd886b124699eaa788bb95926209f2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGroupAccessToGroupProps(
            access_level=access_level,
            shared_group_id=shared_group_id,
            shared_with_group_id=shared_with_group_id,
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
        '''Attribute ``GitLab::Groups::GroupAccessToGroup.MembershipId``.

        :link: https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMembershipId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnGroupAccessToGroupProps":
        '''Resource props.'''
        return typing.cast("CfnGroupAccessToGroupProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/gitlab-groups-groupaccesstogroup.CfnGroupAccessToGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_level": "accessLevel",
        "shared_group_id": "sharedGroupId",
        "shared_with_group_id": "sharedWithGroupId",
    },
)
class CfnGroupAccessToGroupProps:
    def __init__(
        self,
        *,
        access_level: "CfnGroupAccessToGroupPropsAccessLevel",
        shared_group_id: jsii.Number,
        shared_with_group_id: jsii.Number,
    ) -> None:
        '''Adds a group as a member of another GitLab group.

        :param access_level: The access level to grant to the shared-with group for acessing the shared group, e.g. 'Guest', 'Developer', or 'Maintainer'. Note the GitLab API may not allow all values.
        :param shared_group_id: ID of the group which should be shared, i.e. the group to which access is being granted.
        :param shared_with_group_id: ID of the group to share with, i.e. the group being given access to another group.

        :schema: CfnGroupAccessToGroupProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d74b6012b42ec09ec27835bb813913f51604804b45c6e95cce180732f4d3c6f)
            check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
            check_type(argname="argument shared_group_id", value=shared_group_id, expected_type=type_hints["shared_group_id"])
            check_type(argname="argument shared_with_group_id", value=shared_with_group_id, expected_type=type_hints["shared_with_group_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_level": access_level,
            "shared_group_id": shared_group_id,
            "shared_with_group_id": shared_with_group_id,
        }

    @builtins.property
    def access_level(self) -> "CfnGroupAccessToGroupPropsAccessLevel":
        '''The access level to grant to the shared-with group for acessing the shared group, e.g. 'Guest', 'Developer', or 'Maintainer'. Note the GitLab API may not allow all values.

        :schema: CfnGroupAccessToGroupProps#AccessLevel
        '''
        result = self._values.get("access_level")
        assert result is not None, "Required property 'access_level' is missing"
        return typing.cast("CfnGroupAccessToGroupPropsAccessLevel", result)

    @builtins.property
    def shared_group_id(self) -> jsii.Number:
        '''ID of the group which should be shared, i.e. the group to which access is being granted.

        :schema: CfnGroupAccessToGroupProps#SharedGroupId
        '''
        result = self._values.get("shared_group_id")
        assert result is not None, "Required property 'shared_group_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def shared_with_group_id(self) -> jsii.Number:
        '''ID of the group to share with, i.e. the group being given access to another group.

        :schema: CfnGroupAccessToGroupProps#SharedWithGroupId
        '''
        result = self._values.get("shared_with_group_id")
        assert result is not None, "Required property 'shared_with_group_id' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupAccessToGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/gitlab-groups-groupaccesstogroup.CfnGroupAccessToGroupPropsAccessLevel"
)
class CfnGroupAccessToGroupPropsAccessLevel(enum.Enum):
    '''The access level to grant to the shared-with group for acessing the shared group, e.g. 'Guest', 'Developer', or 'Maintainer'. Note the GitLab API may not allow all values.

    :schema: CfnGroupAccessToGroupPropsAccessLevel
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
    "CfnGroupAccessToGroup",
    "CfnGroupAccessToGroupProps",
    "CfnGroupAccessToGroupPropsAccessLevel",
]

publication.publish()

def _typecheckingstub__d9135a7db21f79d3970975956d6c47bb71bd886b124699eaa788bb95926209f2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_level: CfnGroupAccessToGroupPropsAccessLevel,
    shared_group_id: jsii.Number,
    shared_with_group_id: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d74b6012b42ec09ec27835bb813913f51604804b45c6e95cce180732f4d3c6f(
    *,
    access_level: CfnGroupAccessToGroupPropsAccessLevel,
    shared_group_id: jsii.Number,
    shared_with_group_id: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass
