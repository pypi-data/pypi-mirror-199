# CircleCI OIDC

This repository contains constructs to communicate between CircleCI and AWS via an Open ID Connect (OIDC) provider.
The process is described in [this CircleCI blog post](https://circleci.com/blog/openid-connect-identity-tokens/).

## Security Benefits

By using the OpenID Connect provider, you can communicate with AWS from CircleCI without saving static credentials
(e.g., `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) in your CircleCI project settings or a context. Removing
static credentials, especially in light of the early 2023 [breach](https://circleci.com/blog/jan-4-2023-incident-report/),
is a best practice for security.

## Quick Start

Install the package:

```bash
npm install @blimmer/cdk-circleci-oidc

or

yarn add @blimmer/cdk-circleci-oidc
```

Then, create the provider and role(s).

```python
import { Stack, StackProps } from 'aws-cdk-lib';
import { CircleCiOidcProvider, CircleCiOidcRole } from '@blimmer/cdk-circleci-oidc';
import { Construct } from 'constructs';
import { ManagedPolicy, PolicyStatement } from 'aws-cdk-lib/aws-iam';
import { Bucket } from 'aws-cdk-lib/aws-s3';

export class CircleCiStack extends Stack {
  readonly provider: CircleCiOidcProvider; // export for use in other stacks

  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    this.provider = new CircleCiOidcProvider(this, 'OidcProvider', {
      // Find your organization ID in the CircleCI dashboard under "Organization Settings"
      organizationId: '11111111-2222-3333-4444-555555555555',
    });

    const myCircleCiRole = new CircleCiOidcRole(this, 'MyCircleCiRole', {
      circleCiOidcProvider: this.provider,
      roleName: "MyCircleCiRole",

      // Pass some managed policies to the role
      managedPolicies: [
        ManagedPolicy.fromAwsManagedPolicyName('AmazonS3ReadOnlyAccess'),
      ],
    })

    // You can also access the role from the construct. This allows adding roles and using `grant` methods after the
    // construct has been created.
    myCircleCiRole.role.addToPolicy(new PolicyStatement({
      actions: ['s3:ListAllMyBuckets'],
      resources: ['*'],
    }));

    const bucket = new Bucket(this, 'MyBucket');
    bucket.grantRead(myCircleCiRole.role);
  }
}
```

Now, in your `.circleci/config.yml` file, you can use the [AWS CLI Orb](https://circleci.com/developer/orbs/orb/circleci/aws-cli)
to assume your new role.

```yaml
version: 2.1

orbs:
  aws-cli: circleci/aws-cli@3.1.4 # https://circleci.com/developer/orbs/orb/circleci/aws-cli

workflows:
  version: 2
  build:
    jobs:
      - oidc-job:
          context: oidc-assumption # You _must_ use a context, even if it doesn't contain any secrets (see https://circleci.com/docs/openid-connect-tokens/#openid-connect-id-token-availability)

jobs:
  oidc-job:
    docker:
      - image: cimg/base:stable
    steps:
      - checkout
      # https://circleci.com/developer/orbs/orb/circleci/aws-cli#commands-setup
      - aws-cli/setup:
          role-arn: 'arn:aws:iam::123456789101:role/MyCircleCiRole'
      - run:
          name: List S3 Buckets
          command: aws s3 ls
```

## Usage

For detailed API docs, see [API.md](/API.md).

## Python

This package is available for Python as `cdk-circleci-oidc`.

```bash
pip install cdk-circleci-oidc
```

## Contributing

Contributions, issues, and feedback are welcome!
