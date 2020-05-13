# Orchestron Community

![Orchestron Logo](https://www.orchestron.io/hubfs/Orchestron%20November%202017/Image/logo.png?t=1528974210460)

Orchestron is an Application Vulnerability Management and Correlation Tool. One of the key challenges for organizations large and small is to manage vulnerabilities from applications in their environment. This has become a more serious issue with application security being integrated into the CI/CD Environment. In this kind of implementation, security results from SAST, DAST, and Source Composition Analysis (SCA) tools come in, often continuously from automated CI/CD processes. Without a way to manage these vulnerability results, things tend to get overwhelming, very quickly for Application Security teams. This is where Orchestron comes in. 

> Orchestron helps you solve one key problem "Find and fix vulnerabilities early in the lifecycle"

Orchestron allows you to do the following quite effectively: 

* Manage results from various application security tools directly from the CI/CD pipeline with convenient features like webhooks. See Webhooks for more details. For a list of supported tools and formats, please see here.
* Speak the Developer's Language with integrations with Jira => Results from security tools can pushed to Jira from Orchestron. See Settings for more details
* Manage False Positives from across different security tools. See Vulnerabilities for more details.
* Automatically correlate and merge vulnerabilities from across various security tools
* Easily manage releases and "in-time" security assessments with Engagements. See "Engagements" for more details
* Unlike many other tools, Orchestron also attempts to correlate/merge results from across SAST, DAST and SCA tools

## Setup

### Prerequisites
* Install [Docker](https://docs.docker.com/install/)
* Install [Docker Compose](https://docs.docker.com/compose/install/)

### Getting started


To Get Started with Orchestron , run the following steps

```commandline
git clone https://github.com/we45/orchestron-community.git

cd orchestron-community

docker-compose up -d

```

* Browser to [http://localhost](http://localhost)

* Default `username` and `password`

```commandline
username: admin@organization.com
password: Str0ngP@ssw0rd

```

### Update the existing orchestron
```commandline
cd orchestron-community

docker-compose pull

docker-compose up -d

```

### Documentation
Click here for [Orchestron documentation](https://we45devteam.atlassian.net/wiki/spaces/OR/overview) it includes a detailed guides.
