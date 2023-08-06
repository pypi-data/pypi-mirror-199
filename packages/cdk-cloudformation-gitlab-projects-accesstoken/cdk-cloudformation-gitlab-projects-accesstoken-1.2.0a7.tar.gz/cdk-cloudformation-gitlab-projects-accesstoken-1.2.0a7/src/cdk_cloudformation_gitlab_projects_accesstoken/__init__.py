'''
# gitlab-projects-accesstoken

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `GitLab::Projects::AccessToken` v1.2.0.

## Description

Creates a Project Access Token in GitLab

## References

* [Documentation](https://github.com/aws-ia/cloudformation-gitlab-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name GitLab::Projects::AccessToken \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/GitLab-Projects-AccessToken \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `GitLab::Projects::AccessToken`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fgitlab-projects-accesstoken+v1.2.0).
* Issues related to `GitLab::Projects::AccessToken` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-gitlab-resource-providers).

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


class CfnAccessToken(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/gitlab-projects-accesstoken.CfnAccessToken",
):
    '''A CloudFormation ``GitLab::Projects::AccessToken``.

    :cloudformationResource: GitLab::Projects::AccessToken
    :link: https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        project_id: jsii.Number,
        scopes: typing.Sequence[builtins.str],
        access_level: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``GitLab::Projects::AccessToken``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the Project Access Token to create.
        :param project_id: The ID (numeric) of the project for which this Access Token is created. The project should exist and the user creating the Access Token should have rights to do this on this project.
        :param scopes: The scopes this Project Access Token will be used for. The list of supported scopes is in the official GitLab documentation here: https://docs.gitlab.com/ee/user/project/settings/project_access_tokens.html#scopes-for-a-project-access-token .
        :param access_level: A valid access level. Default value is 40 (Maintainer). Other allowed values are 10 (Guest), 20 (Reporter), and 30 (Developer).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__068983b7243184576d7d24d9397e3140ec7e5ed93eac2cc6bd1e7d68b65b2882)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAccessTokenProps(
            name=name, project_id=project_id, scopes=scopes, access_level=access_level
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> jsii.Number:
        '''Attribute ``GitLab::Projects::AccessToken.Id``.

        :link: https://github.com/aws-ia/cloudformation-gitlab-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnAccessTokenProps":
        '''Resource props.'''
        return typing.cast("CfnAccessTokenProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/gitlab-projects-accesstoken.CfnAccessTokenProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "project_id": "projectId",
        "scopes": "scopes",
        "access_level": "accessLevel",
    },
)
class CfnAccessTokenProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        project_id: jsii.Number,
        scopes: typing.Sequence[builtins.str],
        access_level: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Creates a Project Access Token in GitLab.

        :param name: The name of the Project Access Token to create.
        :param project_id: The ID (numeric) of the project for which this Access Token is created. The project should exist and the user creating the Access Token should have rights to do this on this project.
        :param scopes: The scopes this Project Access Token will be used for. The list of supported scopes is in the official GitLab documentation here: https://docs.gitlab.com/ee/user/project/settings/project_access_tokens.html#scopes-for-a-project-access-token .
        :param access_level: A valid access level. Default value is 40 (Maintainer). Other allowed values are 10 (Guest), 20 (Reporter), and 30 (Developer).

        :schema: CfnAccessTokenProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce22fcb96a6d581c3cd1dead888997042815370ba63934eb5e8da6fe6f1e8378)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "project_id": project_id,
            "scopes": scopes,
        }
        if access_level is not None:
            self._values["access_level"] = access_level

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Project Access Token to create.

        :schema: CfnAccessTokenProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> jsii.Number:
        '''The ID (numeric) of the project for which this Access Token is created.

        The project should exist and the user creating the Access Token should have rights to do this on this project.

        :schema: CfnAccessTokenProps#ProjectId
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scopes(self) -> typing.List[builtins.str]:
        '''The scopes this Project Access Token will be used for.

        The list of supported scopes is in the official GitLab documentation here: https://docs.gitlab.com/ee/user/project/settings/project_access_tokens.html#scopes-for-a-project-access-token .

        :schema: CfnAccessTokenProps#Scopes
        '''
        result = self._values.get("scopes")
        assert result is not None, "Required property 'scopes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def access_level(self) -> typing.Optional[jsii.Number]:
        '''A valid access level.

        Default value is 40 (Maintainer). Other allowed values are 10 (Guest), 20 (Reporter), and 30 (Developer).

        :schema: CfnAccessTokenProps#AccessLevel
        '''
        result = self._values.get("access_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessTokenProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAccessToken",
    "CfnAccessTokenProps",
]

publication.publish()

def _typecheckingstub__068983b7243184576d7d24d9397e3140ec7e5ed93eac2cc6bd1e7d68b65b2882(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    project_id: jsii.Number,
    scopes: typing.Sequence[builtins.str],
    access_level: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce22fcb96a6d581c3cd1dead888997042815370ba63934eb5e8da6fe6f1e8378(
    *,
    name: builtins.str,
    project_id: jsii.Number,
    scopes: typing.Sequence[builtins.str],
    access_level: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
