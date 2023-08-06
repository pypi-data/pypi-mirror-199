'''
# github-repositories-repository

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `GitHub::Repositories::Repository` v1.2.0.

## Description

Manage a repository in GitHub.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-github-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-github-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name GitHub::Repositories::Repository \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/GitHub-Repositories-Repository \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `GitHub::Repositories::Repository`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fgithub-repositories-repository+v1.2.0).
* Issues related to `GitHub::Repositories::Repository` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-github-resource-providers).

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


@jsii.data_type(
    jsii_type="@cdk-cloudformation/github-repositories-repository.AdvanceSecurity",
    jsii_struct_bases=[],
    name_mapping={"status": "status"},
)
class AdvanceSecurity:
    def __init__(self, *, status: "AdvanceSecurityStatus") -> None:
        '''Use the status property to enable or disable GitHub Advanced Security for this repository.

        For more information, see "About GitHub Advanced Security." (https://docs.github.com/github/getting-started-with-github/learning-about-github/about-github-advanced-security)

        :param status: Can be enabled or disabled.

        :schema: AdvanceSecurity
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1d4f7957a29c6747a8d3b4168ea046440eb62dbae5a085904e543f920a3a611)
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status": status,
        }

    @builtins.property
    def status(self) -> "AdvanceSecurityStatus":
        '''Can be enabled or disabled.

        :schema: AdvanceSecurity#Status
        '''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast("AdvanceSecurityStatus", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvanceSecurity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/github-repositories-repository.AdvanceSecurityStatus"
)
class AdvanceSecurityStatus(enum.Enum):
    '''Can be enabled or disabled.

    :schema: AdvanceSecurityStatus
    '''

    ENABLED = "ENABLED"
    '''enabled.'''
    DISABLED = "DISABLED"
    '''disabled.'''


class CfnRepository(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/github-repositories-repository.CfnRepository",
):
    '''A CloudFormation ``GitHub::Repositories::Repository``.

    :cloudformationResource: GitHub::Repositories::Repository
    :link: https://github.com/aws-ia/cloudformation-github-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        allow_auto_merge: typing.Optional[builtins.bool] = None,
        allow_forking: typing.Optional[builtins.bool] = None,
        allow_merge_commit: typing.Optional[builtins.bool] = None,
        allow_rebase_merge: typing.Optional[builtins.bool] = None,
        allow_squash_merge: typing.Optional[builtins.bool] = None,
        archived: typing.Optional[builtins.bool] = None,
        auto_init: typing.Optional[builtins.bool] = None,
        delete_branch_on_merge: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        git_ignore_template: typing.Optional[builtins.str] = None,
        has_issues: typing.Optional[builtins.bool] = None,
        has_projects: typing.Optional[builtins.bool] = None,
        has_wiki: typing.Optional[builtins.bool] = None,
        homepage: typing.Optional[builtins.str] = None,
        is_template: typing.Optional[builtins.bool] = None,
        license_template: typing.Optional[builtins.str] = None,
        organization: typing.Optional[builtins.str] = None,
        private: typing.Optional[builtins.bool] = None,
        security_and_analysis: typing.Optional[typing.Union["SecurityAndAnalysis", typing.Dict[builtins.str, typing.Any]]] = None,
        team_id: typing.Optional[jsii.Number] = None,
        visibility: typing.Optional["CfnRepositoryPropsVisibility"] = None,
    ) -> None:
        '''Create a new ``GitHub::Repositories::Repository``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the repository.
        :param allow_auto_merge: Either true to allow auto-merge on pull requests, or false to disallow auto-merge.
        :param allow_forking: Either true to allow private forks, or false to prevent private forks.
        :param allow_merge_commit: Either true to allow merging pull requests with a merge commit, or false to prevent merging pull requests with merge commits.
        :param allow_rebase_merge: Either true to allow rebase-merging pull requests, or false to prevent rebase-merging.
        :param allow_squash_merge: Either true to allow squash-merging pull requests, or false to prevent squash-merging.
        :param archived: true to archive this repository. Note: You cannot unarchive repositories through the API.
        :param auto_init: Pass true to create an initial commit with empty README.
        :param delete_branch_on_merge: Either true to allow automatically deleting head branches when pull requests are merged, or false to prevent automatic deletion.
        :param description: A short description of the repository.
        :param git_ignore_template: Desired language or platform .gitignore template to apply. Use the name of the template without the extension (https://github.com/github/gitignore). For example, "Haskell".
        :param has_issues: Either true to enable issues for this repository or false to disable them.
        :param has_projects: Either true to enable projects for this repository or false to disable them. Note: If you're creating a repository in an organization that has disabled repository projects, the default is false, and if you pass true, the API returns an error.
        :param has_wiki: Either true to enable the wiki for this repository or false to disable it.
        :param homepage: A URL with more information about the repository.
        :param is_template: Either true to make this repo available as a template repository or false to prevent it.
        :param license_template: Choose an open source license template (https://choosealicense.com/) that best suits your needs, and then use the license keyword (https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository#searching-github-by-license-type) as the license_template string. For example, "mit" or "mpl-2.0".
        :param organization: The organization name. The name is not case sensitive. If not specified, then the managed repository will be within the currently logged-in user account.
        :param private: Whether the repository is private.
        :param security_and_analysis: 
        :param team_id: The id of the team that will be granted access to this repository. This is only valid when creating a repository in an organization.
        :param visibility: Can be public or private. If your organization is associated with an enterprise account using GitHub Enterprise Cloud or GitHub Enterprise Server 2.20+, visibility can also be internal. Note: For GitHub Enterprise Server and GitHub AE, this endpoint will only list repositories available to all users on the enterprise. For more information, see "Creating an internal repository" (https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories#about-internal-repositories) in the GitHub Help documentation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a881886ea59e87aabeba49cf6af07ac5925aec89e6caf0469c7072f0cb65100)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRepositoryProps(
            name=name,
            allow_auto_merge=allow_auto_merge,
            allow_forking=allow_forking,
            allow_merge_commit=allow_merge_commit,
            allow_rebase_merge=allow_rebase_merge,
            allow_squash_merge=allow_squash_merge,
            archived=archived,
            auto_init=auto_init,
            delete_branch_on_merge=delete_branch_on_merge,
            description=description,
            git_ignore_template=git_ignore_template,
            has_issues=has_issues,
            has_projects=has_projects,
            has_wiki=has_wiki,
            homepage=homepage,
            is_template=is_template,
            license_template=license_template,
            organization=organization,
            private=private,
            security_and_analysis=security_and_analysis,
            team_id=team_id,
            visibility=visibility,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrDefaultBranch")
    def attr_default_branch(self) -> builtins.str:
        '''Attribute ``GitHub::Repositories::Repository.DefaultBranch``.

        :link: https://github.com/aws-ia/cloudformation-github-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDefaultBranch"))

    @builtins.property
    @jsii.member(jsii_name="attrForksCount")
    def attr_forks_count(self) -> jsii.Number:
        '''Attribute ``GitHub::Repositories::Repository.ForksCount``.

        :link: https://github.com/aws-ia/cloudformation-github-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrForksCount"))

    @builtins.property
    @jsii.member(jsii_name="attrGitUrl")
    def attr_git_url(self) -> builtins.str:
        '''Attribute ``GitHub::Repositories::Repository.GitUrl``.

        :link: https://github.com/aws-ia/cloudformation-github-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrGitUrl"))

    @builtins.property
    @jsii.member(jsii_name="attrHtmlUrl")
    def attr_html_url(self) -> builtins.str:
        '''Attribute ``GitHub::Repositories::Repository.HtmlUrl``.

        :link: https://github.com/aws-ia/cloudformation-github-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrHtmlUrl"))

    @builtins.property
    @jsii.member(jsii_name="attrIssuesCount")
    def attr_issues_count(self) -> jsii.Number:
        '''Attribute ``GitHub::Repositories::Repository.IssuesCount``.

        :link: https://github.com/aws-ia/cloudformation-github-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrIssuesCount"))

    @builtins.property
    @jsii.member(jsii_name="attrLanguage")
    def attr_language(self) -> builtins.str:
        '''Attribute ``GitHub::Repositories::Repository.Language``.

        :link: https://github.com/aws-ia/cloudformation-github-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLanguage"))

    @builtins.property
    @jsii.member(jsii_name="attrOwner")
    def attr_owner(self) -> builtins.str:
        '''Attribute ``GitHub::Repositories::Repository.Owner``.

        :link: https://github.com/aws-ia/cloudformation-github-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrOwner"))

    @builtins.property
    @jsii.member(jsii_name="attrStarsCount")
    def attr_stars_count(self) -> jsii.Number:
        '''Attribute ``GitHub::Repositories::Repository.StarsCount``.

        :link: https://github.com/aws-ia/cloudformation-github-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrStarsCount"))

    @builtins.property
    @jsii.member(jsii_name="attrWatchersCount")
    def attr_watchers_count(self) -> jsii.Number:
        '''Attribute ``GitHub::Repositories::Repository.WatchersCount``.

        :link: https://github.com/aws-ia/cloudformation-github-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrWatchersCount"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnRepositoryProps":
        '''Resource props.'''
        return typing.cast("CfnRepositoryProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/github-repositories-repository.CfnRepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allow_auto_merge": "allowAutoMerge",
        "allow_forking": "allowForking",
        "allow_merge_commit": "allowMergeCommit",
        "allow_rebase_merge": "allowRebaseMerge",
        "allow_squash_merge": "allowSquashMerge",
        "archived": "archived",
        "auto_init": "autoInit",
        "delete_branch_on_merge": "deleteBranchOnMerge",
        "description": "description",
        "git_ignore_template": "gitIgnoreTemplate",
        "has_issues": "hasIssues",
        "has_projects": "hasProjects",
        "has_wiki": "hasWiki",
        "homepage": "homepage",
        "is_template": "isTemplate",
        "license_template": "licenseTemplate",
        "organization": "organization",
        "private": "private",
        "security_and_analysis": "securityAndAnalysis",
        "team_id": "teamId",
        "visibility": "visibility",
    },
)
class CfnRepositoryProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        allow_auto_merge: typing.Optional[builtins.bool] = None,
        allow_forking: typing.Optional[builtins.bool] = None,
        allow_merge_commit: typing.Optional[builtins.bool] = None,
        allow_rebase_merge: typing.Optional[builtins.bool] = None,
        allow_squash_merge: typing.Optional[builtins.bool] = None,
        archived: typing.Optional[builtins.bool] = None,
        auto_init: typing.Optional[builtins.bool] = None,
        delete_branch_on_merge: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        git_ignore_template: typing.Optional[builtins.str] = None,
        has_issues: typing.Optional[builtins.bool] = None,
        has_projects: typing.Optional[builtins.bool] = None,
        has_wiki: typing.Optional[builtins.bool] = None,
        homepage: typing.Optional[builtins.str] = None,
        is_template: typing.Optional[builtins.bool] = None,
        license_template: typing.Optional[builtins.str] = None,
        organization: typing.Optional[builtins.str] = None,
        private: typing.Optional[builtins.bool] = None,
        security_and_analysis: typing.Optional[typing.Union["SecurityAndAnalysis", typing.Dict[builtins.str, typing.Any]]] = None,
        team_id: typing.Optional[jsii.Number] = None,
        visibility: typing.Optional["CfnRepositoryPropsVisibility"] = None,
    ) -> None:
        '''Manage a repository in GitHub.

        :param name: The name of the repository.
        :param allow_auto_merge: Either true to allow auto-merge on pull requests, or false to disallow auto-merge.
        :param allow_forking: Either true to allow private forks, or false to prevent private forks.
        :param allow_merge_commit: Either true to allow merging pull requests with a merge commit, or false to prevent merging pull requests with merge commits.
        :param allow_rebase_merge: Either true to allow rebase-merging pull requests, or false to prevent rebase-merging.
        :param allow_squash_merge: Either true to allow squash-merging pull requests, or false to prevent squash-merging.
        :param archived: true to archive this repository. Note: You cannot unarchive repositories through the API.
        :param auto_init: Pass true to create an initial commit with empty README.
        :param delete_branch_on_merge: Either true to allow automatically deleting head branches when pull requests are merged, or false to prevent automatic deletion.
        :param description: A short description of the repository.
        :param git_ignore_template: Desired language or platform .gitignore template to apply. Use the name of the template without the extension (https://github.com/github/gitignore). For example, "Haskell".
        :param has_issues: Either true to enable issues for this repository or false to disable them.
        :param has_projects: Either true to enable projects for this repository or false to disable them. Note: If you're creating a repository in an organization that has disabled repository projects, the default is false, and if you pass true, the API returns an error.
        :param has_wiki: Either true to enable the wiki for this repository or false to disable it.
        :param homepage: A URL with more information about the repository.
        :param is_template: Either true to make this repo available as a template repository or false to prevent it.
        :param license_template: Choose an open source license template (https://choosealicense.com/) that best suits your needs, and then use the license keyword (https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository#searching-github-by-license-type) as the license_template string. For example, "mit" or "mpl-2.0".
        :param organization: The organization name. The name is not case sensitive. If not specified, then the managed repository will be within the currently logged-in user account.
        :param private: Whether the repository is private.
        :param security_and_analysis: 
        :param team_id: The id of the team that will be granted access to this repository. This is only valid when creating a repository in an organization.
        :param visibility: Can be public or private. If your organization is associated with an enterprise account using GitHub Enterprise Cloud or GitHub Enterprise Server 2.20+, visibility can also be internal. Note: For GitHub Enterprise Server and GitHub AE, this endpoint will only list repositories available to all users on the enterprise. For more information, see "Creating an internal repository" (https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories#about-internal-repositories) in the GitHub Help documentation.

        :schema: CfnRepositoryProps
        '''
        if isinstance(security_and_analysis, dict):
            security_and_analysis = SecurityAndAnalysis(**security_and_analysis)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ee8254cffe85354d86164fcb9559f4574414109c2c5f1c65245332afb5f0347)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allow_auto_merge", value=allow_auto_merge, expected_type=type_hints["allow_auto_merge"])
            check_type(argname="argument allow_forking", value=allow_forking, expected_type=type_hints["allow_forking"])
            check_type(argname="argument allow_merge_commit", value=allow_merge_commit, expected_type=type_hints["allow_merge_commit"])
            check_type(argname="argument allow_rebase_merge", value=allow_rebase_merge, expected_type=type_hints["allow_rebase_merge"])
            check_type(argname="argument allow_squash_merge", value=allow_squash_merge, expected_type=type_hints["allow_squash_merge"])
            check_type(argname="argument archived", value=archived, expected_type=type_hints["archived"])
            check_type(argname="argument auto_init", value=auto_init, expected_type=type_hints["auto_init"])
            check_type(argname="argument delete_branch_on_merge", value=delete_branch_on_merge, expected_type=type_hints["delete_branch_on_merge"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument git_ignore_template", value=git_ignore_template, expected_type=type_hints["git_ignore_template"])
            check_type(argname="argument has_issues", value=has_issues, expected_type=type_hints["has_issues"])
            check_type(argname="argument has_projects", value=has_projects, expected_type=type_hints["has_projects"])
            check_type(argname="argument has_wiki", value=has_wiki, expected_type=type_hints["has_wiki"])
            check_type(argname="argument homepage", value=homepage, expected_type=type_hints["homepage"])
            check_type(argname="argument is_template", value=is_template, expected_type=type_hints["is_template"])
            check_type(argname="argument license_template", value=license_template, expected_type=type_hints["license_template"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument private", value=private, expected_type=type_hints["private"])
            check_type(argname="argument security_and_analysis", value=security_and_analysis, expected_type=type_hints["security_and_analysis"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allow_auto_merge is not None:
            self._values["allow_auto_merge"] = allow_auto_merge
        if allow_forking is not None:
            self._values["allow_forking"] = allow_forking
        if allow_merge_commit is not None:
            self._values["allow_merge_commit"] = allow_merge_commit
        if allow_rebase_merge is not None:
            self._values["allow_rebase_merge"] = allow_rebase_merge
        if allow_squash_merge is not None:
            self._values["allow_squash_merge"] = allow_squash_merge
        if archived is not None:
            self._values["archived"] = archived
        if auto_init is not None:
            self._values["auto_init"] = auto_init
        if delete_branch_on_merge is not None:
            self._values["delete_branch_on_merge"] = delete_branch_on_merge
        if description is not None:
            self._values["description"] = description
        if git_ignore_template is not None:
            self._values["git_ignore_template"] = git_ignore_template
        if has_issues is not None:
            self._values["has_issues"] = has_issues
        if has_projects is not None:
            self._values["has_projects"] = has_projects
        if has_wiki is not None:
            self._values["has_wiki"] = has_wiki
        if homepage is not None:
            self._values["homepage"] = homepage
        if is_template is not None:
            self._values["is_template"] = is_template
        if license_template is not None:
            self._values["license_template"] = license_template
        if organization is not None:
            self._values["organization"] = organization
        if private is not None:
            self._values["private"] = private
        if security_and_analysis is not None:
            self._values["security_and_analysis"] = security_and_analysis
        if team_id is not None:
            self._values["team_id"] = team_id
        if visibility is not None:
            self._values["visibility"] = visibility

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the repository.

        :schema: CfnRepositoryProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_auto_merge(self) -> typing.Optional[builtins.bool]:
        '''Either true to allow auto-merge on pull requests, or false to disallow auto-merge.

        :schema: CfnRepositoryProps#AllowAutoMerge
        '''
        result = self._values.get("allow_auto_merge")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_forking(self) -> typing.Optional[builtins.bool]:
        '''Either true to allow private forks, or false to prevent private forks.

        :schema: CfnRepositoryProps#AllowForking
        '''
        result = self._values.get("allow_forking")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_merge_commit(self) -> typing.Optional[builtins.bool]:
        '''Either true to allow merging pull requests with a merge commit, or false to prevent merging pull requests with merge commits.

        :schema: CfnRepositoryProps#AllowMergeCommit
        '''
        result = self._values.get("allow_merge_commit")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_rebase_merge(self) -> typing.Optional[builtins.bool]:
        '''Either true to allow rebase-merging pull requests, or false to prevent rebase-merging.

        :schema: CfnRepositoryProps#AllowRebaseMerge
        '''
        result = self._values.get("allow_rebase_merge")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_squash_merge(self) -> typing.Optional[builtins.bool]:
        '''Either true to allow squash-merging pull requests, or false to prevent squash-merging.

        :schema: CfnRepositoryProps#AllowSquashMerge
        '''
        result = self._values.get("allow_squash_merge")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def archived(self) -> typing.Optional[builtins.bool]:
        '''true to archive this repository.

        Note: You cannot unarchive repositories through the API.

        :schema: CfnRepositoryProps#Archived
        '''
        result = self._values.get("archived")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_init(self) -> typing.Optional[builtins.bool]:
        '''Pass true to create an initial commit with empty README.

        :schema: CfnRepositoryProps#AutoInit
        '''
        result = self._values.get("auto_init")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def delete_branch_on_merge(self) -> typing.Optional[builtins.bool]:
        '''Either true to allow automatically deleting head branches when pull requests are merged, or false to prevent automatic deletion.

        :schema: CfnRepositoryProps#DeleteBranchOnMerge
        '''
        result = self._values.get("delete_branch_on_merge")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A short description of the repository.

        :schema: CfnRepositoryProps#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def git_ignore_template(self) -> typing.Optional[builtins.str]:
        '''Desired language or platform .gitignore template to apply. Use the name of the template without the extension (https://github.com/github/gitignore). For example, "Haskell".

        :schema: CfnRepositoryProps#GitIgnoreTemplate
        '''
        result = self._values.get("git_ignore_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def has_issues(self) -> typing.Optional[builtins.bool]:
        '''Either true to enable issues for this repository or false to disable them.

        :schema: CfnRepositoryProps#HasIssues
        '''
        result = self._values.get("has_issues")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def has_projects(self) -> typing.Optional[builtins.bool]:
        '''Either true to enable projects for this repository or false to disable them.

        Note: If you're creating a repository in an organization that has disabled repository projects, the default is false, and if you pass true, the API returns an error.

        :schema: CfnRepositoryProps#HasProjects
        '''
        result = self._values.get("has_projects")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def has_wiki(self) -> typing.Optional[builtins.bool]:
        '''Either true to enable the wiki for this repository or false to disable it.

        :schema: CfnRepositoryProps#HasWiki
        '''
        result = self._values.get("has_wiki")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def homepage(self) -> typing.Optional[builtins.str]:
        '''A URL with more information about the repository.

        :schema: CfnRepositoryProps#Homepage
        '''
        result = self._values.get("homepage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_template(self) -> typing.Optional[builtins.bool]:
        '''Either true to make this repo available as a template repository or false to prevent it.

        :schema: CfnRepositoryProps#IsTemplate
        '''
        result = self._values.get("is_template")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def license_template(self) -> typing.Optional[builtins.str]:
        '''Choose an open source license template (https://choosealicense.com/) that best suits your needs, and then use the license keyword (https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository#searching-github-by-license-type) as the license_template string. For example, "mit" or "mpl-2.0".

        :schema: CfnRepositoryProps#LicenseTemplate
        '''
        result = self._values.get("license_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization(self) -> typing.Optional[builtins.str]:
        '''The organization name.

        The name is not case sensitive. If not specified, then the managed repository will be within the currently logged-in user account.

        :schema: CfnRepositoryProps#Organization
        '''
        result = self._values.get("organization")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private(self) -> typing.Optional[builtins.bool]:
        '''Whether the repository is private.

        :schema: CfnRepositoryProps#Private
        '''
        result = self._values.get("private")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def security_and_analysis(self) -> typing.Optional["SecurityAndAnalysis"]:
        '''
        :schema: CfnRepositoryProps#SecurityAndAnalysis
        '''
        result = self._values.get("security_and_analysis")
        return typing.cast(typing.Optional["SecurityAndAnalysis"], result)

    @builtins.property
    def team_id(self) -> typing.Optional[jsii.Number]:
        '''The id of the team that will be granted access to this repository.

        This is only valid when creating a repository in an organization.

        :schema: CfnRepositoryProps#TeamId
        '''
        result = self._values.get("team_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def visibility(self) -> typing.Optional["CfnRepositoryPropsVisibility"]:
        '''Can be public or private.

        If your organization is associated with an enterprise account using GitHub Enterprise Cloud or GitHub Enterprise Server 2.20+, visibility can also be internal. Note: For GitHub Enterprise Server and GitHub AE, this endpoint will only list repositories available to all users on the enterprise. For more information, see "Creating an internal repository" (https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories#about-internal-repositories) in the GitHub Help documentation.

        :schema: CfnRepositoryProps#Visibility
        '''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional["CfnRepositoryPropsVisibility"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/github-repositories-repository.CfnRepositoryPropsVisibility"
)
class CfnRepositoryPropsVisibility(enum.Enum):
    '''Can be public or private.

    If your organization is associated with an enterprise account using GitHub Enterprise Cloud or GitHub Enterprise Server 2.20+, visibility can also be internal. Note: For GitHub Enterprise Server and GitHub AE, this endpoint will only list repositories available to all users on the enterprise. For more information, see "Creating an internal repository" (https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories#about-internal-repositories) in the GitHub Help documentation.

    :schema: CfnRepositoryPropsVisibility
    '''

    PUBLIC = "PUBLIC"
    '''public.'''
    PRIVATE = "PRIVATE"
    '''private.'''
    INTERNAL = "INTERNAL"
    '''internal.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/github-repositories-repository.SecretScanning",
    jsii_struct_bases=[],
    name_mapping={"status": "status"},
)
class SecretScanning:
    def __init__(self, *, status: "SecretScanningStatus") -> None:
        '''Use the status property to enable or disable secret scanning for this repository.

        For more information, see "About secret scanning." (https://docs.github.com/code-security/secret-security/about-secret-scanning)

        :param status: Can be enabled or disabled.

        :schema: SecretScanning
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8698974f3794a8c35e7f5e677157d4c9e2f6fefb5e7569dc8d26c205adf203da)
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status": status,
        }

    @builtins.property
    def status(self) -> "SecretScanningStatus":
        '''Can be enabled or disabled.

        :schema: SecretScanning#Status
        '''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast("SecretScanningStatus", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretScanning(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/github-repositories-repository.SecretScanningPushProtection",
    jsii_struct_bases=[],
    name_mapping={"status": "status"},
)
class SecretScanningPushProtection:
    def __init__(self, *, status: "SecretScanningPushProtectionStatus") -> None:
        '''Use the status property to enable or disable secret scanning push protection for this repository.

        For more information, see "Protecting pushes with secret scanning." (https://docs.github.com/code-security/secret-scanning/protecting-pushes-with-secret-scanning)

        :param status: Can be enabled or disabled.

        :schema: SecretScanningPushProtection
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9feaf9671913c86e6789d6a299b6f8347736c0b498fb527fd2298b3c52ba8027)
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status": status,
        }

    @builtins.property
    def status(self) -> "SecretScanningPushProtectionStatus":
        '''Can be enabled or disabled.

        :schema: SecretScanningPushProtection#Status
        '''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast("SecretScanningPushProtectionStatus", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretScanningPushProtection(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/github-repositories-repository.SecretScanningPushProtectionStatus"
)
class SecretScanningPushProtectionStatus(enum.Enum):
    '''Can be enabled or disabled.

    :schema: SecretScanningPushProtectionStatus
    '''

    ENABLED = "ENABLED"
    '''enabled.'''
    DISABLED = "DISABLED"
    '''disabled.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/github-repositories-repository.SecretScanningStatus"
)
class SecretScanningStatus(enum.Enum):
    '''Can be enabled or disabled.

    :schema: SecretScanningStatus
    '''

    ENABLED = "ENABLED"
    '''enabled.'''
    DISABLED = "DISABLED"
    '''disabled.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/github-repositories-repository.SecurityAndAnalysis",
    jsii_struct_bases=[],
    name_mapping={
        "advance_security": "advanceSecurity",
        "secret_scanning": "secretScanning",
        "secret_scanning_push_protection": "secretScanningPushProtection",
    },
)
class SecurityAndAnalysis:
    def __init__(
        self,
        *,
        advance_security: typing.Optional[typing.Union[AdvanceSecurity, typing.Dict[builtins.str, typing.Any]]] = None,
        secret_scanning: typing.Optional[typing.Union[SecretScanning, typing.Dict[builtins.str, typing.Any]]] = None,
        secret_scanning_push_protection: typing.Optional[typing.Union[SecretScanningPushProtection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Specify which security and analysis features to enable or disable.

        For example, to enable GitHub Advanced Security, use this data in the body of the PATCH request: {"security_and_analysis": {"advanced_security": {"status": "enabled"}}}. If you have admin permissions for a private repository covered by an Advanced Security license, you can check which security and analysis features are currently enabled by using a GET /repos/{owner}/{repo} request.

        :param advance_security: 
        :param secret_scanning: 
        :param secret_scanning_push_protection: 

        :schema: SecurityAndAnalysis
        '''
        if isinstance(advance_security, dict):
            advance_security = AdvanceSecurity(**advance_security)
        if isinstance(secret_scanning, dict):
            secret_scanning = SecretScanning(**secret_scanning)
        if isinstance(secret_scanning_push_protection, dict):
            secret_scanning_push_protection = SecretScanningPushProtection(**secret_scanning_push_protection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__465f3edb1ea3c1f2a9babcd1ac9bf5dcfdc88377f2ba89fbd7a122289b17c45f)
            check_type(argname="argument advance_security", value=advance_security, expected_type=type_hints["advance_security"])
            check_type(argname="argument secret_scanning", value=secret_scanning, expected_type=type_hints["secret_scanning"])
            check_type(argname="argument secret_scanning_push_protection", value=secret_scanning_push_protection, expected_type=type_hints["secret_scanning_push_protection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if advance_security is not None:
            self._values["advance_security"] = advance_security
        if secret_scanning is not None:
            self._values["secret_scanning"] = secret_scanning
        if secret_scanning_push_protection is not None:
            self._values["secret_scanning_push_protection"] = secret_scanning_push_protection

    @builtins.property
    def advance_security(self) -> typing.Optional[AdvanceSecurity]:
        '''
        :schema: SecurityAndAnalysis#AdvanceSecurity
        '''
        result = self._values.get("advance_security")
        return typing.cast(typing.Optional[AdvanceSecurity], result)

    @builtins.property
    def secret_scanning(self) -> typing.Optional[SecretScanning]:
        '''
        :schema: SecurityAndAnalysis#SecretScanning
        '''
        result = self._values.get("secret_scanning")
        return typing.cast(typing.Optional[SecretScanning], result)

    @builtins.property
    def secret_scanning_push_protection(
        self,
    ) -> typing.Optional[SecretScanningPushProtection]:
        '''
        :schema: SecurityAndAnalysis#SecretScanningPushProtection
        '''
        result = self._values.get("secret_scanning_push_protection")
        return typing.cast(typing.Optional[SecretScanningPushProtection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityAndAnalysis(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AdvanceSecurity",
    "AdvanceSecurityStatus",
    "CfnRepository",
    "CfnRepositoryProps",
    "CfnRepositoryPropsVisibility",
    "SecretScanning",
    "SecretScanningPushProtection",
    "SecretScanningPushProtectionStatus",
    "SecretScanningStatus",
    "SecurityAndAnalysis",
]

publication.publish()

def _typecheckingstub__d1d4f7957a29c6747a8d3b4168ea046440eb62dbae5a085904e543f920a3a611(
    *,
    status: AdvanceSecurityStatus,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a881886ea59e87aabeba49cf6af07ac5925aec89e6caf0469c7072f0cb65100(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    allow_auto_merge: typing.Optional[builtins.bool] = None,
    allow_forking: typing.Optional[builtins.bool] = None,
    allow_merge_commit: typing.Optional[builtins.bool] = None,
    allow_rebase_merge: typing.Optional[builtins.bool] = None,
    allow_squash_merge: typing.Optional[builtins.bool] = None,
    archived: typing.Optional[builtins.bool] = None,
    auto_init: typing.Optional[builtins.bool] = None,
    delete_branch_on_merge: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    git_ignore_template: typing.Optional[builtins.str] = None,
    has_issues: typing.Optional[builtins.bool] = None,
    has_projects: typing.Optional[builtins.bool] = None,
    has_wiki: typing.Optional[builtins.bool] = None,
    homepage: typing.Optional[builtins.str] = None,
    is_template: typing.Optional[builtins.bool] = None,
    license_template: typing.Optional[builtins.str] = None,
    organization: typing.Optional[builtins.str] = None,
    private: typing.Optional[builtins.bool] = None,
    security_and_analysis: typing.Optional[typing.Union[SecurityAndAnalysis, typing.Dict[builtins.str, typing.Any]]] = None,
    team_id: typing.Optional[jsii.Number] = None,
    visibility: typing.Optional[CfnRepositoryPropsVisibility] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee8254cffe85354d86164fcb9559f4574414109c2c5f1c65245332afb5f0347(
    *,
    name: builtins.str,
    allow_auto_merge: typing.Optional[builtins.bool] = None,
    allow_forking: typing.Optional[builtins.bool] = None,
    allow_merge_commit: typing.Optional[builtins.bool] = None,
    allow_rebase_merge: typing.Optional[builtins.bool] = None,
    allow_squash_merge: typing.Optional[builtins.bool] = None,
    archived: typing.Optional[builtins.bool] = None,
    auto_init: typing.Optional[builtins.bool] = None,
    delete_branch_on_merge: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    git_ignore_template: typing.Optional[builtins.str] = None,
    has_issues: typing.Optional[builtins.bool] = None,
    has_projects: typing.Optional[builtins.bool] = None,
    has_wiki: typing.Optional[builtins.bool] = None,
    homepage: typing.Optional[builtins.str] = None,
    is_template: typing.Optional[builtins.bool] = None,
    license_template: typing.Optional[builtins.str] = None,
    organization: typing.Optional[builtins.str] = None,
    private: typing.Optional[builtins.bool] = None,
    security_and_analysis: typing.Optional[typing.Union[SecurityAndAnalysis, typing.Dict[builtins.str, typing.Any]]] = None,
    team_id: typing.Optional[jsii.Number] = None,
    visibility: typing.Optional[CfnRepositoryPropsVisibility] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8698974f3794a8c35e7f5e677157d4c9e2f6fefb5e7569dc8d26c205adf203da(
    *,
    status: SecretScanningStatus,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9feaf9671913c86e6789d6a299b6f8347736c0b498fb527fd2298b3c52ba8027(
    *,
    status: SecretScanningPushProtectionStatus,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__465f3edb1ea3c1f2a9babcd1ac9bf5dcfdc88377f2ba89fbd7a122289b17c45f(
    *,
    advance_security: typing.Optional[typing.Union[AdvanceSecurity, typing.Dict[builtins.str, typing.Any]]] = None,
    secret_scanning: typing.Optional[typing.Union[SecretScanning, typing.Dict[builtins.str, typing.Any]]] = None,
    secret_scanning_push_protection: typing.Optional[typing.Union[SecretScanningPushProtection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
