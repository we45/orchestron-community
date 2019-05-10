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


### Prerequisites
* Install [Docker](https://docs.docker.com/install/)
* Install [Docker Compose](https://docs.docker.com/compose/install/)

### Getting started


To Get Started with Orchestron , run the following steps

```commandline
git cline https://github.com/we45/orchestron-community.git

cd orchestron-community
```

##### Make the necessary changes in the compose file(docker-compose.yml)
* **MYSQL_ROOT_PASSWORD**   MySQL Database Password for Root User. If necessary, changes can be made to the docker-compose.yml file and a non-root User can be used instead.
* **MINIO_ACCESS_KEY**   Minio Access Key should be a minimum of 3 characters in length.
* **MINIO_SECRET_KEY** Minio Secret Key should be a minimum of 8 characters in length.
* **ENC_KEY** Encryption Key is used to Encrypt Jira and Email Configuration Parameters.
* **JWT_SECRET_KEY** JWT Secret Key to Generate JWT tokens.
* **ADMIN_USER_EMAIL** Administrator Email ID.
* **ADMIN_USER_PASS** Administrator Password.

**Note:** Once you made the necessary changes in the compose file run the below command.

```commandline
docker-compose up -d
```

* Browser to [http://localhost](http://localhost)


### Documentation
Click here [Orchestron Documentation](https://we45devteam.atlassian.net/wiki/spaces/OR/overview)

