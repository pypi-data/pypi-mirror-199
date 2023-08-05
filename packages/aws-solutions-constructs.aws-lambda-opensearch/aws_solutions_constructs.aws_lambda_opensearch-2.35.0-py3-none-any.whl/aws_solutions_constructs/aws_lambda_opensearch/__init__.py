'''
# aws-lambda-opensearch module

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **Reference Documentation**:| <span style="font-weight: normal">https://docs.aws.amazon.com/solutions/latest/constructs/</span>|
|:-------------|:-------------|

<div style="height:8px"></div>

| **Language**     | **Package**        |
|:-------------|-----------------|
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_lambda_opensearch`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-lambda-opensearch`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.lambdaopensearch`|

## Overview

This AWS Solutions Construct implements an AWS Lambda function and Amazon OpenSearch Service with the least privileged permissions.

Here is a minimal deployable pattern definition:

Typescript

```python
import { Construct } from 'constructs';
import { Stack, StackProps, Aws } from 'aws-cdk-lib';
import { LambdaToOpenSearch } from '@aws-solutions-constructs/aws-lambda-opensearch';
import * as lambda from "aws-cdk-lib/aws-lambda";

const lambdaProps: lambda.FunctionProps = {
  code: lambda.Code.fromAsset(`lambda`),
  runtime: lambda.Runtime.NODEJS_14_X,
  handler: 'index.handler'
};

new LambdaToOpenSearch(this, 'sample', {
  lambdaFunctionProps: lambdaProps,
  openSearchDomainName: 'testdomain',
  // TODO: Ensure the Cognito domain name is globally unique
  cognitoDomainName: 'globallyuniquedomain' + Aws.ACCOUNT_ID
});
```

Python

```python
from aws_solutions_constructs.aws_lambda_opensearch import LambdaToOpenSearch
from aws_cdk import (
    aws_lambda as _lambda,
    Aws,
    Stack
)
from constructs import Construct

lambda_props = _lambda.FunctionProps(
    code=_lambda.Code.from_asset('lambda'),
    runtime=_lambda.Runtime.PYTHON_3_9,
    handler='index.handler'
)

LambdaToOpenSearch(self, 'sample',
                            lambda_function_props=lambda_props,
                            open_search_domain_name='testdomain',
                            # TODO: Ensure the Cognito domain name is globally unique
                            cognito_domain_name='globallyuniquedomain' + Aws.ACCOUNT_ID
                            )
```

Java

```java
import software.constructs.Construct;

import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;
import software.amazon.awscdk.Aws;
import software.amazon.awscdk.services.lambda.*;
import software.amazon.awscdk.services.lambda.Runtime;
import software.amazon.awsconstructs.services.lambdaopensearch.*;

new LambdaToOpenSearch(this, "sample",
        new LambdaToOpenSearchProps.Builder()
                .lambdaFunctionProps(new FunctionProps.Builder()
                        .runtime(Runtime.NODEJS_14_X)
                        .code(Code.fromAsset("lambda"))
                        .handler("index.handler")
                        .build())
                .openSearchDomainName("testdomain")
                // TODO: Ensure the Cognito domain name is globally unique
                .cognitoDomainName("globallyuniquedomain" + Aws.ACCOUNT_ID)
                .build());
```

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|existingLambdaObj?|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_lambda.Function.html)|Existing instance of Lambda Function object, providing both this and `lambdaFunctionProps` will cause an error.|
|lambdaFunctionProps?|[`lambda.FunctionProps`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_lambda.FunctionProps.html)|User provided props to override the default props for the Lambda function.|
|openSearchDomainProps?|[`opensearchservice.CfnDomainProps`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_opensearchservice.CfnDomainProps.html)|Optional user provided props to override the default props for the OpenSearch Service.|
|openSearchDomainName|`string`|Domain name for the OpenSearch Service.|
|cognitoDomainName?|`string`|Optional Amazon Cognito domain name. If omitted the Amazon Cognito domain will default to the OpenSearch Service domain name.|
|createCloudWatchAlarms?|`boolean`|Whether to create the recommended CloudWatch alarms.|
|domainEndpointEnvironmentVariableName?|`string`|Optional name for the OpenSearch domain endpoint environment variable set for the Lambda function. Default is `DOMAIN_ENDPOINT`.|
|existingVpc?|[`ec2.IVpc`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.IVpc.html)|An optional, existing VPC into which this pattern should be deployed. When deployed in a VPC, the Lambda function will use ENIs in the VPC to access network resources. If an existing VPC is provided, the `deployVpc` property cannot be `true`. This uses `ec2.IVpc` to allow clients to supply VPCs that exist outside the stack using the [`ec2.Vpc.fromLookup()`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.Vpc.html#static-fromwbrlookupscope-id-options) method.|
|vpcProps?|[`ec2.VpcProps`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.VpcProps.html)|Optional user provided properties to override the default properties for the new VPC. `enableDnsHostnames`, `enableDnsSupport`, `natGateways` and `subnetConfiguration` are set by the pattern, so any values for those properties supplied here will be overridden. If `deployVpc` is not `true` then this property will be ignored.|
|deployVpc?|`boolean`|Whether to create a new VPC based on `vpcProps` into which to deploy this pattern. Setting this to true will deploy the minimal, most private VPC to run the pattern:<ul><li> One isolated subnet in each Availability Zone used by the CDK program</li><li>`enableDnsHostnames` and `enableDnsSupport` will both be set to true</li></ul>If this property is `true` then `existingVpc` cannot be specified. Defaults to `false`.|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|lambdaFunction|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_lambda.Function.html)|Returns an instance of `lambda.Function` created by the construct|
|userPool|[`cognito.UserPool`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_cognito.UserPool.html)|Returns an instance of `cognito.UserPool` created by the construct|
|userPoolClient|[`cognito.UserPoolClient`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_cognito.UserPoolClient.html)|Returns an instance of `cognito.UserPoolClient` created by the construct|
|identityPool|[`cognito.CfnIdentityPool`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_cognito.CfnIdentityPool.html)|Returns an instance of `cognito.CfnIdentityPool` created by the construct|
|openSearchDomain|[`opensearchservice.CfnDomain`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_opensearchservice.CfnDomain.html)|Returns an instance of `opensearch.CfnDomain` created by the construct|
|openSearchRole|[`iam.Role`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_iam.Role.html)|Returns an instance of `iam.Role` created by the construct for `opensearch.CfnDomain`|
|cloudWatchAlarms?|[`cloudwatch.Alarm[]`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_cloudwatch.Alarm.html)|Returns a list of `cloudwatch.Alarm` created by the construct|
|vpc?|[`ec2.IVpc`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.IVpc.html)|Returns an interface on the VPC used by the pattern (if any). This may be a VPC created by the pattern or the VPC supplied to the pattern constructor.|

## Lambda Function

This pattern requires a lambda function that can post data into the OpenSearch. A sample function is provided [here](https://github.com/awslabs/aws-solutions-constructs/blob/master/source/patterns/%40aws-solutions-constructs/aws-lambda-opensearch/test/lambda/index.js).

## Default settings

Out of the box implementation of the Construct without any overrides will set the following defaults:

### AWS Lambda Function

* Configure limited privilege access IAM role for Lambda function
* Enable reusing connections with Keep-Alive for Node.js Lambda function
* Enable X-Ray Tracing
* Set Environment Variables

  * (default) DOMAIN_ENDPOINT
  * AWS_NODEJS_CONNECTION_REUSE_ENABLED

### Amazon Cognito

* Set password policy for User Pools
* Enforce the advanced security mode for User Pools

### Amazon OpenSearch Service

* Deploy best practices CloudWatch Alarms for the OpenSearch Service domain
* Secure the OpenSearch Service dashboard access with Cognito User Pools
* Enable server-side encryption for OpenSearch Service domain using AWS managed KMS Key
* Enable node-to-node encryption for the OpenSearch Service domain
* Configure the cluster for the OpenSearch Service domain

## Architecture

![Architecture Diagram](architecture.png)

---


© Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_ceddda9d
import aws_cdk.aws_cognito as _aws_cdk_aws_cognito_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_opensearchservice as _aws_cdk_aws_opensearchservice_ceddda9d
import constructs as _constructs_77d1e7e8


class LambdaToOpenSearch(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-solutions-constructs/aws-lambda-opensearch.LambdaToOpenSearch",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        open_search_domain_name: builtins.str,
        cognito_domain_name: typing.Optional[builtins.str] = None,
        create_cloud_watch_alarms: typing.Optional[builtins.bool] = None,
        deploy_vpc: typing.Optional[builtins.bool] = None,
        domain_endpoint_environment_variable_name: typing.Optional[builtins.str] = None,
        existing_lambda_obj: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Function] = None,
        existing_vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        lambda_function_props: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.FunctionProps, typing.Dict[builtins.str, typing.Any]]] = None,
        open_search_domain_props: typing.Optional[typing.Union[_aws_cdk_aws_opensearchservice_ceddda9d.CfnDomainProps, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_props: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpcProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param open_search_domain_name: Domain name for the OpenSearch Service. Default: - None
        :param cognito_domain_name: Optional Amazon Cognito domain name. If omitted the Amazon Cognito domain will default to the OpenSearch Service domain name. Default: - the OpenSearch Service domain name
        :param create_cloud_watch_alarms: Whether to create recommended CloudWatch alarms. Default: - Alarms are created
        :param deploy_vpc: Whether to deploy a new VPC. Default: - false
        :param domain_endpoint_environment_variable_name: Optional Name for the Lambda function environment variable set to the domain endpoint. Default: - DOMAIN_ENDPOINT
        :param existing_lambda_obj: Existing instance of Lambda Function object, providing both this and ``lambdaFunctionProps`` will cause an error. Default: - None
        :param existing_vpc: An existing VPC for the construct to use (construct will NOT create a new VPC in this case). Default: - None
        :param lambda_function_props: User provided props to override the default props for the Lambda function. Default: - Default props are used
        :param open_search_domain_props: Optional user provided props to override the default props for the OpenSearch Service. Default: - Default props are used
        :param vpc_props: Properties to override default properties if deployVpc is true. Default: - DefaultIsolatedVpcProps() in vpc-defaults.ts

        :access: public
        :since: 0.8.0
        :summary: Constructs a new instance of the LambdaToOpenSearch class.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__795a9339512603411cd2038ac2faf28439b41fd07f032699bf5b15a06cdac7f4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LambdaToOpenSearchProps(
            open_search_domain_name=open_search_domain_name,
            cognito_domain_name=cognito_domain_name,
            create_cloud_watch_alarms=create_cloud_watch_alarms,
            deploy_vpc=deploy_vpc,
            domain_endpoint_environment_variable_name=domain_endpoint_environment_variable_name,
            existing_lambda_obj=existing_lambda_obj,
            existing_vpc=existing_vpc,
            lambda_function_props=lambda_function_props,
            open_search_domain_props=open_search_domain_props,
            vpc_props=vpc_props,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="identityPool")
    def identity_pool(self) -> _aws_cdk_aws_cognito_ceddda9d.CfnIdentityPool:
        return typing.cast(_aws_cdk_aws_cognito_ceddda9d.CfnIdentityPool, jsii.get(self, "identityPool"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.get(self, "lambdaFunction"))

    @builtins.property
    @jsii.member(jsii_name="openSearchDomain")
    def open_search_domain(self) -> _aws_cdk_aws_opensearchservice_ceddda9d.CfnDomain:
        return typing.cast(_aws_cdk_aws_opensearchservice_ceddda9d.CfnDomain, jsii.get(self, "openSearchDomain"))

    @builtins.property
    @jsii.member(jsii_name="openSearchRole")
    def open_search_role(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.get(self, "openSearchRole"))

    @builtins.property
    @jsii.member(jsii_name="userPool")
    def user_pool(self) -> _aws_cdk_aws_cognito_ceddda9d.UserPool:
        return typing.cast(_aws_cdk_aws_cognito_ceddda9d.UserPool, jsii.get(self, "userPool"))

    @builtins.property
    @jsii.member(jsii_name="userPoolClient")
    def user_pool_client(self) -> _aws_cdk_aws_cognito_ceddda9d.UserPoolClient:
        return typing.cast(_aws_cdk_aws_cognito_ceddda9d.UserPoolClient, jsii.get(self, "userPoolClient"))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchAlarms")
    def cloud_watch_alarms(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.Alarm]]:
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_cloudwatch_ceddda9d.Alarm]], jsii.get(self, "cloudWatchAlarms"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], jsii.get(self, "vpc"))


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-lambda-opensearch.LambdaToOpenSearchProps",
    jsii_struct_bases=[],
    name_mapping={
        "open_search_domain_name": "openSearchDomainName",
        "cognito_domain_name": "cognitoDomainName",
        "create_cloud_watch_alarms": "createCloudWatchAlarms",
        "deploy_vpc": "deployVpc",
        "domain_endpoint_environment_variable_name": "domainEndpointEnvironmentVariableName",
        "existing_lambda_obj": "existingLambdaObj",
        "existing_vpc": "existingVpc",
        "lambda_function_props": "lambdaFunctionProps",
        "open_search_domain_props": "openSearchDomainProps",
        "vpc_props": "vpcProps",
    },
)
class LambdaToOpenSearchProps:
    def __init__(
        self,
        *,
        open_search_domain_name: builtins.str,
        cognito_domain_name: typing.Optional[builtins.str] = None,
        create_cloud_watch_alarms: typing.Optional[builtins.bool] = None,
        deploy_vpc: typing.Optional[builtins.bool] = None,
        domain_endpoint_environment_variable_name: typing.Optional[builtins.str] = None,
        existing_lambda_obj: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Function] = None,
        existing_vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        lambda_function_props: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.FunctionProps, typing.Dict[builtins.str, typing.Any]]] = None,
        open_search_domain_props: typing.Optional[typing.Union[_aws_cdk_aws_opensearchservice_ceddda9d.CfnDomainProps, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_props: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpcProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param open_search_domain_name: Domain name for the OpenSearch Service. Default: - None
        :param cognito_domain_name: Optional Amazon Cognito domain name. If omitted the Amazon Cognito domain will default to the OpenSearch Service domain name. Default: - the OpenSearch Service domain name
        :param create_cloud_watch_alarms: Whether to create recommended CloudWatch alarms. Default: - Alarms are created
        :param deploy_vpc: Whether to deploy a new VPC. Default: - false
        :param domain_endpoint_environment_variable_name: Optional Name for the Lambda function environment variable set to the domain endpoint. Default: - DOMAIN_ENDPOINT
        :param existing_lambda_obj: Existing instance of Lambda Function object, providing both this and ``lambdaFunctionProps`` will cause an error. Default: - None
        :param existing_vpc: An existing VPC for the construct to use (construct will NOT create a new VPC in this case). Default: - None
        :param lambda_function_props: User provided props to override the default props for the Lambda function. Default: - Default props are used
        :param open_search_domain_props: Optional user provided props to override the default props for the OpenSearch Service. Default: - Default props are used
        :param vpc_props: Properties to override default properties if deployVpc is true. Default: - DefaultIsolatedVpcProps() in vpc-defaults.ts

        :summary: The properties for the LambdaToOpenSearch Construct
        '''
        if isinstance(lambda_function_props, dict):
            lambda_function_props = _aws_cdk_aws_lambda_ceddda9d.FunctionProps(**lambda_function_props)
        if isinstance(open_search_domain_props, dict):
            open_search_domain_props = _aws_cdk_aws_opensearchservice_ceddda9d.CfnDomainProps(**open_search_domain_props)
        if isinstance(vpc_props, dict):
            vpc_props = _aws_cdk_aws_ec2_ceddda9d.VpcProps(**vpc_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c1e6c42a48f3546216e3a2b9be25f3621705c14d127c8ce6fcef0af38ca1318)
            check_type(argname="argument open_search_domain_name", value=open_search_domain_name, expected_type=type_hints["open_search_domain_name"])
            check_type(argname="argument cognito_domain_name", value=cognito_domain_name, expected_type=type_hints["cognito_domain_name"])
            check_type(argname="argument create_cloud_watch_alarms", value=create_cloud_watch_alarms, expected_type=type_hints["create_cloud_watch_alarms"])
            check_type(argname="argument deploy_vpc", value=deploy_vpc, expected_type=type_hints["deploy_vpc"])
            check_type(argname="argument domain_endpoint_environment_variable_name", value=domain_endpoint_environment_variable_name, expected_type=type_hints["domain_endpoint_environment_variable_name"])
            check_type(argname="argument existing_lambda_obj", value=existing_lambda_obj, expected_type=type_hints["existing_lambda_obj"])
            check_type(argname="argument existing_vpc", value=existing_vpc, expected_type=type_hints["existing_vpc"])
            check_type(argname="argument lambda_function_props", value=lambda_function_props, expected_type=type_hints["lambda_function_props"])
            check_type(argname="argument open_search_domain_props", value=open_search_domain_props, expected_type=type_hints["open_search_domain_props"])
            check_type(argname="argument vpc_props", value=vpc_props, expected_type=type_hints["vpc_props"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "open_search_domain_name": open_search_domain_name,
        }
        if cognito_domain_name is not None:
            self._values["cognito_domain_name"] = cognito_domain_name
        if create_cloud_watch_alarms is not None:
            self._values["create_cloud_watch_alarms"] = create_cloud_watch_alarms
        if deploy_vpc is not None:
            self._values["deploy_vpc"] = deploy_vpc
        if domain_endpoint_environment_variable_name is not None:
            self._values["domain_endpoint_environment_variable_name"] = domain_endpoint_environment_variable_name
        if existing_lambda_obj is not None:
            self._values["existing_lambda_obj"] = existing_lambda_obj
        if existing_vpc is not None:
            self._values["existing_vpc"] = existing_vpc
        if lambda_function_props is not None:
            self._values["lambda_function_props"] = lambda_function_props
        if open_search_domain_props is not None:
            self._values["open_search_domain_props"] = open_search_domain_props
        if vpc_props is not None:
            self._values["vpc_props"] = vpc_props

    @builtins.property
    def open_search_domain_name(self) -> builtins.str:
        '''Domain name for the OpenSearch Service.

        :default: - None
        '''
        result = self._values.get("open_search_domain_name")
        assert result is not None, "Required property 'open_search_domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cognito_domain_name(self) -> typing.Optional[builtins.str]:
        '''Optional Amazon Cognito domain name.

        If omitted the Amazon Cognito domain will default to the OpenSearch Service domain name.

        :default: - the OpenSearch Service domain name
        '''
        result = self._values.get("cognito_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_cloud_watch_alarms(self) -> typing.Optional[builtins.bool]:
        '''Whether to create recommended CloudWatch alarms.

        :default: - Alarms are created
        '''
        result = self._values.get("create_cloud_watch_alarms")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def deploy_vpc(self) -> typing.Optional[builtins.bool]:
        '''Whether to deploy a new VPC.

        :default: - false
        '''
        result = self._values.get("deploy_vpc")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def domain_endpoint_environment_variable_name(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Optional Name for the Lambda function environment variable set to the domain endpoint.

        :default: - DOMAIN_ENDPOINT
        '''
        result = self._values.get("domain_endpoint_environment_variable_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def existing_lambda_obj(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Function]:
        '''Existing instance of Lambda Function object, providing both this and ``lambdaFunctionProps`` will cause an error.

        :default: - None
        '''
        result = self._values.get("existing_lambda_obj")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Function], result)

    @builtins.property
    def existing_vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''An existing VPC for the construct to use (construct will NOT create a new VPC in this case).

        :default: - None
        '''
        result = self._values.get("existing_vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    @builtins.property
    def lambda_function_props(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FunctionProps]:
        '''User provided props to override the default props for the Lambda function.

        :default: - Default props are used
        '''
        result = self._values.get("lambda_function_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FunctionProps], result)

    @builtins.property
    def open_search_domain_props(
        self,
    ) -> typing.Optional[_aws_cdk_aws_opensearchservice_ceddda9d.CfnDomainProps]:
        '''Optional user provided props to override the default props for the OpenSearch Service.

        :default: - Default props are used
        '''
        result = self._values.get("open_search_domain_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_opensearchservice_ceddda9d.CfnDomainProps], result)

    @builtins.property
    def vpc_props(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.VpcProps]:
        '''Properties to override default properties if deployVpc is true.

        :default: - DefaultIsolatedVpcProps() in vpc-defaults.ts
        '''
        result = self._values.get("vpc_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.VpcProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaToOpenSearchProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "LambdaToOpenSearch",
    "LambdaToOpenSearchProps",
]

publication.publish()

def _typecheckingstub__795a9339512603411cd2038ac2faf28439b41fd07f032699bf5b15a06cdac7f4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    open_search_domain_name: builtins.str,
    cognito_domain_name: typing.Optional[builtins.str] = None,
    create_cloud_watch_alarms: typing.Optional[builtins.bool] = None,
    deploy_vpc: typing.Optional[builtins.bool] = None,
    domain_endpoint_environment_variable_name: typing.Optional[builtins.str] = None,
    existing_lambda_obj: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Function] = None,
    existing_vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    lambda_function_props: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.FunctionProps, typing.Dict[builtins.str, typing.Any]]] = None,
    open_search_domain_props: typing.Optional[typing.Union[_aws_cdk_aws_opensearchservice_ceddda9d.CfnDomainProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_props: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpcProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c1e6c42a48f3546216e3a2b9be25f3621705c14d127c8ce6fcef0af38ca1318(
    *,
    open_search_domain_name: builtins.str,
    cognito_domain_name: typing.Optional[builtins.str] = None,
    create_cloud_watch_alarms: typing.Optional[builtins.bool] = None,
    deploy_vpc: typing.Optional[builtins.bool] = None,
    domain_endpoint_environment_variable_name: typing.Optional[builtins.str] = None,
    existing_lambda_obj: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Function] = None,
    existing_vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    lambda_function_props: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.FunctionProps, typing.Dict[builtins.str, typing.Any]]] = None,
    open_search_domain_props: typing.Optional[typing.Union[_aws_cdk_aws_opensearchservice_ceddda9d.CfnDomainProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_props: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpcProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
