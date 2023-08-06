'''
# github-teams-repositoryaccess

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `GitHub::Teams::RepositoryAccess` v1.1.0.

## Description

Manage a team access to a repository in GitHub.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-github-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-github-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name GitHub::Teams::RepositoryAccess \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/GitHub-Teams-RepositoryAccess \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `GitHub::Teams::RepositoryAccess`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fgithub-teams-repositoryaccess+v1.1.0).
* Issues related to `GitHub::Teams::RepositoryAccess` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-github-resource-providers).

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


class CfnRepositoryAccess(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/github-teams-repositoryaccess.CfnRepositoryAccess",
):
    '''A CloudFormation ``GitHub::Teams::RepositoryAccess``.

    :cloudformationResource: GitHub::Teams::RepositoryAccess
    :link: https://github.com/aws-ia/cloudformation-github-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        org: builtins.str,
        owner: builtins.str,
        repository: builtins.str,
        team: builtins.str,
        permission: typing.Optional["CfnRepositoryAccessPropsPermission"] = None,
    ) -> None:
        '''Create a new ``GitHub::Teams::RepositoryAccess``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param org: The organization name. The name is not case sensitive.
        :param owner: The account owner of the repository. The name is not case sensitive.
        :param repository: The name of the repository. The name is not case sensitive.
        :param team: The slug of the team name.
        :param permission: The permission to grant the team on this repository. In addition to the enumerated values, you can also specify a custom repository role name, if the owning organization has defined any. If no permission is specified, the team's permission attribute will be used to determine what permission to grant the team on this repository.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc0a9c4b8b983e7fbbc5ef83091f21580d04f8f7f682bbba4574a1accc9d8b04)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRepositoryAccessProps(
            org=org,
            owner=owner,
            repository=repository,
            team=team,
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
    def props(self) -> "CfnRepositoryAccessProps":
        '''Resource props.'''
        return typing.cast("CfnRepositoryAccessProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/github-teams-repositoryaccess.CfnRepositoryAccessProps",
    jsii_struct_bases=[],
    name_mapping={
        "org": "org",
        "owner": "owner",
        "repository": "repository",
        "team": "team",
        "permission": "permission",
    },
)
class CfnRepositoryAccessProps:
    def __init__(
        self,
        *,
        org: builtins.str,
        owner: builtins.str,
        repository: builtins.str,
        team: builtins.str,
        permission: typing.Optional["CfnRepositoryAccessPropsPermission"] = None,
    ) -> None:
        '''Manage a team access to a repository in GitHub.

        :param org: The organization name. The name is not case sensitive.
        :param owner: The account owner of the repository. The name is not case sensitive.
        :param repository: The name of the repository. The name is not case sensitive.
        :param team: The slug of the team name.
        :param permission: The permission to grant the team on this repository. In addition to the enumerated values, you can also specify a custom repository role name, if the owning organization has defined any. If no permission is specified, the team's permission attribute will be used to determine what permission to grant the team on this repository.

        :schema: CfnRepositoryAccessProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8beb86d5cd11935580a672f8fb852ea10bc6b9bdc5d4e7f17bb0c4c845c7d294)
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument team", value=team, expected_type=type_hints["team"])
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "org": org,
            "owner": owner,
            "repository": repository,
            "team": team,
        }
        if permission is not None:
            self._values["permission"] = permission

    @builtins.property
    def org(self) -> builtins.str:
        '''The organization name.

        The name is not case sensitive.

        :schema: CfnRepositoryAccessProps#Org
        '''
        result = self._values.get("org")
        assert result is not None, "Required property 'org' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def owner(self) -> builtins.str:
        '''The account owner of the repository.

        The name is not case sensitive.

        :schema: CfnRepositoryAccessProps#Owner
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository(self) -> builtins.str:
        '''The name of the repository.

        The name is not case sensitive.

        :schema: CfnRepositoryAccessProps#Repository
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def team(self) -> builtins.str:
        '''The slug of the team name.

        :schema: CfnRepositoryAccessProps#Team
        '''
        result = self._values.get("team")
        assert result is not None, "Required property 'team' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def permission(self) -> typing.Optional["CfnRepositoryAccessPropsPermission"]:
        '''The permission to grant the team on this repository.

        In addition to the enumerated values, you can also specify a custom repository role name, if the owning organization has defined any. If no permission is specified, the team's permission attribute will be used to determine what permission to grant the team on this repository.

        :schema: CfnRepositoryAccessProps#Permission
        '''
        result = self._values.get("permission")
        return typing.cast(typing.Optional["CfnRepositoryAccessPropsPermission"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRepositoryAccessProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/github-teams-repositoryaccess.CfnRepositoryAccessPropsPermission"
)
class CfnRepositoryAccessPropsPermission(enum.Enum):
    '''The permission to grant the team on this repository.

    In addition to the enumerated values, you can also specify a custom repository role name, if the owning organization has defined any. If no permission is specified, the team's permission attribute will be used to determine what permission to grant the team on this repository.

    :schema: CfnRepositoryAccessPropsPermission
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
    "CfnRepositoryAccess",
    "CfnRepositoryAccessProps",
    "CfnRepositoryAccessPropsPermission",
]

publication.publish()

def _typecheckingstub__bc0a9c4b8b983e7fbbc5ef83091f21580d04f8f7f682bbba4574a1accc9d8b04(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    org: builtins.str,
    owner: builtins.str,
    repository: builtins.str,
    team: builtins.str,
    permission: typing.Optional[CfnRepositoryAccessPropsPermission] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8beb86d5cd11935580a672f8fb852ea10bc6b9bdc5d4e7f17bb0c4c845c7d294(
    *,
    org: builtins.str,
    owner: builtins.str,
    repository: builtins.str,
    team: builtins.str,
    permission: typing.Optional[CfnRepositoryAccessPropsPermission] = None,
) -> None:
    """Type checking stubs"""
    pass
