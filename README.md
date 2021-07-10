# Repo-Schlep
The details of the project(s) i.e. the code, documentation etc. will be listed here.

# Contributing Guidelines

Thank you for your interest in contributing to our project! 💛


This is our website link of our Sign in/up Page 


https://dependabot-npm-and-yarn-dns-packet-1-3-4.d30dl8xk9x6qzt.amplifyapp.com/

We have made it using Html,CSS and react web development language.

AWS Amplify aims to enhance the development experience using JavaScript with AWS. Amplify codifies best practices through programmatic interfaces to help you effortlessly interact with cloud resources.

First and foremost Amplify exposes to you WHAT things do and then HOW best to do them. The WHAT is at a functional use case with HOW being an opinionated implementation that you can override with “escape hatches.” This will allow you to have higher velocity and build better applications by focusing less on implementation choices. Secondly, Amplify should be a manifestation of The Rule of Least Power when developing against AWS. This means it encourages architectural and programmatic best practices and the ability to start quickly. This shows by encouraging certain services (API Gateway usage vs. direct DynamoDB interaction) or certain connection patterns (Circuit breaker, retry counts and throttle up/down).

Opinionated implementations: There are many ways to interface with AWS Services. Certain service interactions are favored over others. For instance, if sending and receiving JSON, we would prefer an API Gateway endpoint to other mechanisms. Amplify will programmatically help optimize for cost and performance through library decisions.

Declarative actions: Amplify will provide you a reference to a generic client object and the ability to perform common actions. “RegisterUser”, “Login”, “SendObject”, “UpdateObject”, “StreamData”. By default you should not need to worry about AWS Service specific API operations like putItem() with a unique hash or even HTTP verbs.

Cascading service interactions: Certain actions in a declarative style can have overlapping or ambiguous AWS Service implementations. With an opinionated implementation, we can decide which Services are "primary" and which are "secondary" depending on what is configured. For instance, sending an image will prefer S3 over API Gateway.

Simple, standard data objects: Sending & receiving data to AWS Services can have many parameters, which tend to show up in the SDKs. These are abstracted and inferred, where possible, with simple JSON that the implementation can reason about. Standard parameters (bucket names, stream names, partition keys, etc.) that are part of the implementation are extracted from a simplified configuration file and dynamically generated/updated in order to further allow focus on state and data types only.

# Our Design

As more and more modules were introduced to AWS Amplify, it became necessary to modularize the library into smaller pieces so that users could avoid importing unnecessary parts into their app. The goal of this design is to make AWS Amplify modularized and also keep it backward-compatible to avoid breaking changes.

Modular import prevents unnecessary code dependencies from being included with the app, and thus decreases the bundle size while enabling added new functionality without the risk of introducing errors related to unused code.

Amplify has established the concepts of categories and plugins. A category is a collection of api calls that are exposed to the client to do things inside that category. For example, in the storage category, generally one wants to upload and download objects from storage so the apis exposed to the client will represent that functionality. Because Amplify is pluggable, a plugin of your choosing will provide the actual implementation behind that api interface. Using the same example of Storage, the plugin we choose might be AWSStoragePlugin which would then implement each api call from the category with a service call or set of service calls to S3, the underlying storage provider of the AWS plugin.

# Development Process

Our work is done directly on aws Amplify and PR's are sent to the GitHub repo by core team members and contributors. Everyone undergoes the same review process to get their changes into the repo.

## Setting up for local development

This section should get you running with **Amplify JS** and get you familiar with the basics of the codebase. You will need the latest version of [Node.js](https://nodejs.org/en/) on your system and developing locally also requires `yarn` workspaces. You can install it [here](https://classic.yarnpkg.com/en/docs/install#mac-stable).

Start by [forking](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) the main branch of [amplify-js](https://github.com/aws-amplify/amplify-js).

```
git clone git@github.com:[username]/amplify-js.git
cd amplify-js

yarn
yarn bootstrap
yarn build
```

> Note: Make sure to always [sync your fork](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork) with main branch of `amplify-js`

## Architecture of the codebase

Amplify JS is a monorepo built with `Yarn` and `Lerna`. All the categories of Amplify live within the `packages` directory in the root. Each category inside packages has its own `src/` and `package.json`.

[**Packages inside Amplify JS Monorepo**](https://github.com/aws-amplify/amplify-js/tree/main/packages)

## Steps towards contributions

- To make changes with respect to a specific category, go into `packages/[category]`.
- Make changes to required file.
- Write unit tests
- Yarn build
- Run test suite
- Test in sample app using yarn linking
- Submit a PR

