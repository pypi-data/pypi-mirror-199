'''
# github-git-tag

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `GitHub::Git::Tag` v1.2.0.

## Description

Manage a git tag on GitHub

## References

* [Documentation](https://github.com/aws-ia/cloudformation-github-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-github-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name GitHub::Git::Tag \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/GitHub-Git-Tag \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `GitHub::Git::Tag`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fgithub-git-tag+v1.2.0).
* Issues related to `GitHub::Git::Tag` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-github-resource-providers).

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


class CfnTag(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/github-git-tag.CfnTag",
):
    '''A CloudFormation ``GitHub::Git::Tag``.

    :cloudformationResource: GitHub::Git::Tag
    :link: https://github.com/aws-ia/cloudformation-github-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        owner: builtins.str,
        repository: builtins.str,
        sha: builtins.str,
        tag: builtins.str,
        force: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Create a new ``GitHub::Git::Tag``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param owner: The account owner of the repository. The name is not case sensitive.
        :param repository: The name of the repository. The name is not case sensitive.
        :param sha: The SHA1 value for this reference.
        :param tag: The name of git tag.
        :param force: Indicates whether to force the update or to make sure the update is a fast-forward update. Leaving this out or setting it to false will make sure you're not overwriting work. This is used only during updates
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1291060abc443f5eb6c4c7a6941160593ad94151b6110f3cfc114a93a99326e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTagProps(
            owner=owner, repository=repository, sha=sha, tag=tag, force=force
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnTagProps":
        '''Resource props.'''
        return typing.cast("CfnTagProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/github-git-tag.CfnTagProps",
    jsii_struct_bases=[],
    name_mapping={
        "owner": "owner",
        "repository": "repository",
        "sha": "sha",
        "tag": "tag",
        "force": "force",
    },
)
class CfnTagProps:
    def __init__(
        self,
        *,
        owner: builtins.str,
        repository: builtins.str,
        sha: builtins.str,
        tag: builtins.str,
        force: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Manage a git tag on GitHub.

        :param owner: The account owner of the repository. The name is not case sensitive.
        :param repository: The name of the repository. The name is not case sensitive.
        :param sha: The SHA1 value for this reference.
        :param tag: The name of git tag.
        :param force: Indicates whether to force the update or to make sure the update is a fast-forward update. Leaving this out or setting it to false will make sure you're not overwriting work. This is used only during updates

        :schema: CfnTagProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7604eb91376ba894281a3961c9dc14f27eac6e3908c5ca55134438531a83416)
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument sha", value=sha, expected_type=type_hints["sha"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument force", value=force, expected_type=type_hints["force"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "owner": owner,
            "repository": repository,
            "sha": sha,
            "tag": tag,
        }
        if force is not None:
            self._values["force"] = force

    @builtins.property
    def owner(self) -> builtins.str:
        '''The account owner of the repository.

        The name is not case sensitive.

        :schema: CfnTagProps#Owner
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository(self) -> builtins.str:
        '''The name of the repository.

        The name is not case sensitive.

        :schema: CfnTagProps#Repository
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha(self) -> builtins.str:
        '''The SHA1 value for this reference.

        :schema: CfnTagProps#Sha
        '''
        result = self._values.get("sha")
        assert result is not None, "Required property 'sha' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag(self) -> builtins.str:
        '''The name of git tag.

        :schema: CfnTagProps#Tag
        '''
        result = self._values.get("tag")
        assert result is not None, "Required property 'tag' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def force(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether to force the update or to make sure the update is a fast-forward update.

        Leaving this out or setting it to false will make sure you're not overwriting work. This is used only during updates

        :schema: CfnTagProps#Force
        '''
        result = self._values.get("force")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTagProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnTag",
    "CfnTagProps",
]

publication.publish()

def _typecheckingstub__f1291060abc443f5eb6c4c7a6941160593ad94151b6110f3cfc114a93a99326e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    owner: builtins.str,
    repository: builtins.str,
    sha: builtins.str,
    tag: builtins.str,
    force: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7604eb91376ba894281a3961c9dc14f27eac6e3908c5ca55134438531a83416(
    *,
    owner: builtins.str,
    repository: builtins.str,
    sha: builtins.str,
    tag: builtins.str,
    force: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
