'''
# github-repositories-collaborator

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `GitHub::Repositories::Collaborator` v1.2.0.

## Description

The Collaborators resource allows you to add, invite, and remove collaborators from a repository.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-github-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-github-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name GitHub::Repositories::Collaborator \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/GitHub-Repositories-Collaborator \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `GitHub::Repositories::Collaborator`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fgithub-repositories-collaborator+v1.2.0).
* Issues related to `GitHub::Repositories::Collaborator` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-github-resource-providers).

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


class CfnCollaborator(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/github-repositories-collaborator.CfnCollaborator",
):
    '''A CloudFormation ``GitHub::Repositories::Collaborator``.

    :cloudformationResource: GitHub::Repositories::Collaborator
    :link: https://github.com/aws-ia/cloudformation-github-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        owner: builtins.str,
        repository: builtins.str,
        username: builtins.str,
        permission: typing.Optional["CfnCollaboratorPropsPermission"] = None,
    ) -> None:
        '''Create a new ``GitHub::Repositories::Collaborator``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param owner: The account owner of the repository. The name is not case sensitive.
        :param repository: The name of the repository. The name is not case sensitive.
        :param username: The login name for the GitHub user account.
        :param permission: The permission to grant the collaborator. Only valid on organization-owned repositories. In addition to the enumerated values, you can also specify a custom repository role name, if the owning organization has defined any..
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aeebb09afedba8b766c885d1b22b9e65e00e40dfd624b2bbc68110e4364039c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCollaboratorProps(
            owner=owner,
            repository=repository,
            username=username,
            permission=permission,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnCollaboratorProps":
        '''Resource props.'''
        return typing.cast("CfnCollaboratorProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/github-repositories-collaborator.CfnCollaboratorProps",
    jsii_struct_bases=[],
    name_mapping={
        "owner": "owner",
        "repository": "repository",
        "username": "username",
        "permission": "permission",
    },
)
class CfnCollaboratorProps:
    def __init__(
        self,
        *,
        owner: builtins.str,
        repository: builtins.str,
        username: builtins.str,
        permission: typing.Optional["CfnCollaboratorPropsPermission"] = None,
    ) -> None:
        '''The Collaborators resource allows you to add, invite, and remove collaborators from a repository.

        :param owner: The account owner of the repository. The name is not case sensitive.
        :param repository: The name of the repository. The name is not case sensitive.
        :param username: The login name for the GitHub user account.
        :param permission: The permission to grant the collaborator. Only valid on organization-owned repositories. In addition to the enumerated values, you can also specify a custom repository role name, if the owning organization has defined any..

        :schema: CfnCollaboratorProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62aa42e6821b63e0c2f456c634a1aa5a636bff95354645ee4cef01bdd51e6c04)
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "owner": owner,
            "repository": repository,
            "username": username,
        }
        if permission is not None:
            self._values["permission"] = permission

    @builtins.property
    def owner(self) -> builtins.str:
        '''The account owner of the repository.

        The name is not case sensitive.

        :schema: CfnCollaboratorProps#Owner
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository(self) -> builtins.str:
        '''The name of the repository.

        The name is not case sensitive.

        :schema: CfnCollaboratorProps#Repository
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''The login name for the GitHub user account.

        :schema: CfnCollaboratorProps#Username
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def permission(self) -> typing.Optional["CfnCollaboratorPropsPermission"]:
        '''The permission to grant the collaborator.

        Only valid on organization-owned repositories. In addition to the enumerated values, you can also specify a custom repository role name, if the owning organization has defined any..

        :schema: CfnCollaboratorProps#Permission
        '''
        result = self._values.get("permission")
        return typing.cast(typing.Optional["CfnCollaboratorPropsPermission"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCollaboratorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/github-repositories-collaborator.CfnCollaboratorPropsPermission"
)
class CfnCollaboratorPropsPermission(enum.Enum):
    '''The permission to grant the collaborator.

    Only valid on organization-owned repositories. In addition to the enumerated values, you can also specify a custom repository role name, if the owning organization has defined any..

    :schema: CfnCollaboratorPropsPermission
    '''

    PULL = "PULL"
    '''pull.'''
    PUSH = "PUSH"
    '''push.'''
    ADMIN = "ADMIN"
    '''admin.'''
    MAINTAIN = "MAINTAIN"
    '''maintain.'''
    TRIAGE = "TRIAGE"
    '''triage.'''


__all__ = [
    "CfnCollaborator",
    "CfnCollaboratorProps",
    "CfnCollaboratorPropsPermission",
]

publication.publish()

def _typecheckingstub__7aeebb09afedba8b766c885d1b22b9e65e00e40dfd624b2bbc68110e4364039c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    owner: builtins.str,
    repository: builtins.str,
    username: builtins.str,
    permission: typing.Optional[CfnCollaboratorPropsPermission] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62aa42e6821b63e0c2f456c634a1aa5a636bff95354645ee4cef01bdd51e6c04(
    *,
    owner: builtins.str,
    repository: builtins.str,
    username: builtins.str,
    permission: typing.Optional[CfnCollaboratorPropsPermission] = None,
) -> None:
    """Type checking stubs"""
    pass
