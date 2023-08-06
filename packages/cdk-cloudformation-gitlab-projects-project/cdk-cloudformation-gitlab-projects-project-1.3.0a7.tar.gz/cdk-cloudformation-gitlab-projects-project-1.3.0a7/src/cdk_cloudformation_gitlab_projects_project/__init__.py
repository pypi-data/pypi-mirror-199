'''
# gitlab-projects-project

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `GitLab::Projects::Project` v1.3.0.

## Description

Creates a project in GitLab

## References

* [Documentation](https://github.com/aws-ia/cloudformation-gitlab-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name GitLab::Projects::Project \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/GitLab-Projects-Project \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `GitLab::Projects::Project`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fgitlab-projects-project+v1.3.0).
* Issues related to `GitLab::Projects::Project` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-gitlab-resource-providers).

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


class CfnProject(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/gitlab-projects-project.CfnProject",
):
    '''A CloudFormation ``GitLab::Projects::Project``.

    :cloudformationResource: GitLab::Projects::Project
    :link: https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        path: typing.Optional[builtins.str] = None,
        public: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Create a new ``GitLab::Projects::Project``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the project to create.
        :param path: The path of the project.
        :param public: Whether the project should be public (default false).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f02bf1b3de79d94739dbcac6bc28e04664cc4fe692294361ff95100fa6fb9c6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnProjectProps(name=name, path=path, public=public)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> jsii.Number:
        '''Attribute ``GitLab::Projects::Project.Id``.

        :link: https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnProjectProps":
        '''Resource props.'''
        return typing.cast("CfnProjectProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/gitlab-projects-project.CfnProjectProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path", "public": "public"},
)
class CfnProjectProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        path: typing.Optional[builtins.str] = None,
        public: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Creates a project in GitLab.

        :param name: The name of the project to create.
        :param path: The path of the project.
        :param public: Whether the project should be public (default false).

        :schema: CfnProjectProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07696aec39f5f36c8de37adec7070e784ed510e09de6ddfa887e0c47f8a4258f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument public", value=public, expected_type=type_hints["public"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if path is not None:
            self._values["path"] = path
        if public is not None:
            self._values["public"] = public

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the project to create.

        :schema: CfnProjectProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path of the project.

        :schema: CfnProjectProps#Path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public(self) -> typing.Optional[builtins.bool]:
        '''Whether the project should be public (default false).

        :schema: CfnProjectProps#Public
        '''
        result = self._values.get("public")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnProject",
    "CfnProjectProps",
]

publication.publish()

def _typecheckingstub__6f02bf1b3de79d94739dbcac6bc28e04664cc4fe692294361ff95100fa6fb9c6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    path: typing.Optional[builtins.str] = None,
    public: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07696aec39f5f36c8de37adec7070e784ed510e09de6ddfa887e0c47f8a4258f(
    *,
    name: builtins.str,
    path: typing.Optional[builtins.str] = None,
    public: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
