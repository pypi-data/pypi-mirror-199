'''
# gitlab-code-tag

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `GitLab::Code::Tag` v1.3.0.

## Description

Creates a tag against a code ref in GitLab

## References

* [Documentation](https://github.com/aws-ia/cloudformation-gitlab-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name GitLab::Code::Tag \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/GitLab-Code-Tag \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `GitLab::Code::Tag`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fgitlab-code-tag+v1.3.0).
* Issues related to `GitLab::Code::Tag` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-gitlab-resource-providers).

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
    jsii_type="@cdk-cloudformation/gitlab-code-tag.CfnTag",
):
    '''A CloudFormation ``GitLab::Code::Tag``.

    :cloudformationResource: GitLab::Code::Tag
    :link: https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        project_id: jsii.Number,
        ref: builtins.str,
        message: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``GitLab::Code::Tag``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the tag to create.
        :param project_id: The ID of the project which will be tagged.
        :param ref: The reference to the code commit to be tagged, either a commit SHA ID or a branch name (to use the commit which is head of that branch at time of tag creation).
        :param message: A message to attach to the tag.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9098fb74572357ca21b560e3d2e52604a87f89dcc38eca4ab62db7e55be3d0de)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTagProps(name=name, project_id=project_id, ref=ref, message=message)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCommitId")
    def attr_commit_id(self) -> builtins.str:
        '''Attribute ``GitLab::Code::Tag.CommitId``.

        :link: https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCommitId"))

    @builtins.property
    @jsii.member(jsii_name="attrTagId")
    def attr_tag_id(self) -> builtins.str:
        '''Attribute ``GitLab::Code::Tag.TagId``.

        :link: https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTagId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnTagProps":
        '''Resource props.'''
        return typing.cast("CfnTagProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/gitlab-code-tag.CfnTagProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "project_id": "projectId",
        "ref": "ref",
        "message": "message",
    },
)
class CfnTagProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        project_id: jsii.Number,
        ref: builtins.str,
        message: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a tag against a code ref in GitLab.

        :param name: The name of the tag to create.
        :param project_id: The ID of the project which will be tagged.
        :param ref: The reference to the code commit to be tagged, either a commit SHA ID or a branch name (to use the commit which is head of that branch at time of tag creation).
        :param message: A message to attach to the tag.

        :schema: CfnTagProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b055cbe568267ef43d3bb7df04ef3663bdca9e6c1f22aa93e2842383e6ae6ac)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "project_id": project_id,
            "ref": ref,
        }
        if message is not None:
            self._values["message"] = message

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the tag to create.

        :schema: CfnTagProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> jsii.Number:
        '''The ID of the project which will be tagged.

        :schema: CfnTagProps#ProjectId
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def ref(self) -> builtins.str:
        '''The reference to the code commit to be tagged, either a commit SHA ID or a branch name (to use the commit which is head of that branch at time of tag creation).

        :schema: CfnTagProps#Ref
        '''
        result = self._values.get("ref")
        assert result is not None, "Required property 'ref' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''A message to attach to the tag.

        :schema: CfnTagProps#Message
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

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

def _typecheckingstub__9098fb74572357ca21b560e3d2e52604a87f89dcc38eca4ab62db7e55be3d0de(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    project_id: jsii.Number,
    ref: builtins.str,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b055cbe568267ef43d3bb7df04ef3663bdca9e6c1f22aa93e2842383e6ae6ac(
    *,
    name: builtins.str,
    project_id: jsii.Number,
    ref: builtins.str,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
