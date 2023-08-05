[![ CI DBaaS Mongo Python](https://github.com/ionos-cloud/sdk-resources/actions/workflows/ci-dbaas-mongo-python.yml/badge.svg)](https://github.com/ionos-cloud/sdk-resources/actions/workflows/ci-dbaas-mongo-python.yml)
[![Gitter](https://img.shields.io/gitter/room/ionos-cloud/sdk-general)](https://gitter.im/ionos-cloud/sdk-general)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-dbaas-mongo&metric=alert_status)](https://sonarcloud.io/summary?id=sdk-python-dbaas-mongo)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-dbaas-mongo&metric=bugs)](https://sonarcloud.io/summary/new_code?id=sdk-python-dbaas-mongo)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-dbaas-mongo&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=sdk-python-dbaas-mongo)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-dbaas-mongo&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=sdk-python-dbaas-mongo)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-dbaas-mongo&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=sdk-python-dbaas-mongo)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-dbaas-mongo&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=sdk-python-dbaas-mongo)
[![Release](https://img.shields.io/github/v/release/ionos-cloud/sdk-python-dbaas-mongo.svg)](https://github.com/ionos-cloud/sdk-python-dbaas-mongo/releases/latest)
[![Release Date](https://img.shields.io/github/release-date/ionos-cloud/sdk-python-dbaas-mongo.svg)](https://github.com/ionos-cloud/sdk-python-dbaas-mongo/releases/latest)
[![PyPI version](https://img.shields.io/pypi/v/ionoscloud-dbaas-mongo)](https://pypi.org/project/ionoscloud-dbaas-mongo/)

![Alt text](.github/IONOS.CLOUD.BLU.svg?raw=true "Title")


# Python API client for ionoscloud_dbaas_mongo

With IONOS Cloud Database as a Service, you have the ability to quickly set up and manage a MongoDB database. You can also delete clusters, manage backups and users via the API.

MongoDB is an open source, cross-platform, document-oriented database program. Classified as a NoSQL database program, it uses JSON-like documents with optional schemas.

The MongoDB API allows you to create additional database clusters or modify existing ones. Both tools, the Data Center Designer (DCD) and the API use the same concepts consistently and are well suited for smooth and intuitive use.


## Overview
The IONOS Cloud SDK for Python provides you with access to the IONOS Cloud Dbaas Postgres API. The client library supports both simple and complex requests. It is designed for developers who are building applications in Python. All API operations are performed over SSL and authenticated using your IONOS Cloud portal credentials. The API can be accessed within an instance running in IONOS Cloud or directly over the Internet from any application that can send an HTTPS request and receive an HTTPS response.


### Installation & Usage

**Requirements:**
- Python >= 3.5

### pip install

Since this package is hosted on [Pypi](https://pypi.org/) you can install it by using:

```bash
pip install ionoscloud-dbaas-mongo
```

If the python package is hosted on a repository, you can install directly using:

```bash
pip install git+https://github.com/ionos-cloud/sdk-python-dbaas-mongo.git
```

Note: you may need to run `pip` with root permission: `sudo pip install git+https://github.com/ionos-cloud/sdk-python-dbaas-mongo.git`

Then import the package:

```python
import ionoscloud_dbaas_mongo
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```bash
python setup.py install --user
```

or `sudo python setup.py install` to install the package for all users

Then import the package:

```python
import ionoscloud_dbaas_mongo
```

> **_NOTE:_**  The Python SDK does not support Python 2. It only supports Python >= 3.5.

### Authentication

The username and password **or** the authentication token can be manually specified when initializing the SDK client:

```python
configuration = ionoscloud_dbaas_mongo.Configuration(
                username='YOUR_USERNAME',
                password='YOUR_PASSWORD',
                token='YOUR_TOKEN'
                )
client = ionoscloud_dbaas_mongo.ApiClient(configuration)
```

Environment variables can also be used. This is an example of how one would do that:

```python
import os

configuration = ionoscloud_dbaas_mongo.Configuration(
                username=os.environ.get('IONOS_USERNAME'),
                password=os.environ.get('IONOS_PASSWORD'),
                token=os.environ.get('IONOS_TOKEN')
                )
client = ionoscloud_dbaas_mongo.ApiClient(configuration)
```

**Warning**: Make sure to follow the Information Security Best Practices when using credentials within your code or storing them in a file.


### HTTP proxies

You can use http proxies by setting the following environment variables:
- `IONOS_HTTP_PROXY` - proxy URL
- `IONOS_HTTP_PROXY_HEADERS` - proxy headers

### Changing the base URL

Base URL for the HTTP operation can be changed in the following way:

```python
import os

configuration = ionoscloud_dbaas_mongo.Configuration(
                username=os.environ.get('IONOS_USERNAME'),
                password=os.environ.get('IONOS_PASSWORD'),
                host=os.environ.get('IONOS_API_URL'),
                server_index=None,
                )
client = ionoscloud_dbaas_mongo.ApiClient(configuration)
```

## Certificate pinning:

You can enable certificate pinning if you want to bypass the normal certificate checking procedure,
by doing the following:

Set env variable IONOS_PINNED_CERT=<insert_sha256_public_fingerprint_here>

You can get the sha256 fingerprint most easily from the browser by inspecting the certificate.


## Documentation for API Endpoints

All URIs are relative to *https://api.ionos.com/databases/mongodb*
<details >
    <summary title="Click to toggle">API Endpoints table</summary>


| Class | Method | HTTP request | Description |
| ------------- | ------------- | ------------- | ------------- |
| ClustersApi | [**clusters_delete**](docs/api/ClustersApi.md#clusters_delete) | **DELETE** /clusters/{clusterId} | Delete a Cluster |
| ClustersApi | [**clusters_find_by_id**](docs/api/ClustersApi.md#clusters_find_by_id) | **GET** /clusters/{clusterId} | Get a cluster by id |
| ClustersApi | [**clusters_get**](docs/api/ClustersApi.md#clusters_get) | **GET** /clusters | Get Clusters |
| ClustersApi | [**clusters_patch**](docs/api/ClustersApi.md#clusters_patch) | **PATCH** /clusters/{clusterId} | Patch a cluster |
| ClustersApi | [**clusters_post**](docs/api/ClustersApi.md#clusters_post) | **POST** /clusters | Create a Cluster |
| LogsApi | [**clusters_logs_get**](docs/api/LogsApi.md#clusters_logs_get) | **GET** /clusters/{clusterId}/logs | Get logs of your cluster |
| MetadataApi | [**infos_version_get**](docs/api/MetadataApi.md#infos_version_get) | **GET** /infos/version | Get API Version |
| MetadataApi | [**infos_versions_get**](docs/api/MetadataApi.md#infos_versions_get) | **GET** /infos/versions | Get All API Versions |
| RestoresApi | [**clusters_restore_post**](docs/api/RestoresApi.md#clusters_restore_post) | **POST** /clusters/{clusterId}/restore | In-place restore of a cluster |
| SnapshotsApi | [**clusters_snapshots_get**](docs/api/SnapshotsApi.md#clusters_snapshots_get) | **GET** /clusters/{clusterId}/snapshots | Get the snapshots of your cluster |
| TemplatesApi | [**templates_get**](docs/api/TemplatesApi.md#templates_get) | **GET** /templates | Get Templates |
| UsersApi | [**clusters_users_delete**](docs/api/UsersApi.md#clusters_users_delete) | **DELETE** /clusters/{clusterId}/users/{username} | Delete a MongoDB User by ID |
| UsersApi | [**clusters_users_find_by_id**](docs/api/UsersApi.md#clusters_users_find_by_id) | **GET** /clusters/{clusterId}/users/{username} | Get a MongoDB User by ID |
| UsersApi | [**clusters_users_get**](docs/api/UsersApi.md#clusters_users_get) | **GET** /clusters/{clusterId}/users | Get all Cluster Users |
| UsersApi | [**clusters_users_patch**](docs/api/UsersApi.md#clusters_users_patch) | **PATCH** /clusters/{clusterId}/users/{username} | Patch a MongoDB User by ID |
| UsersApi | [**clusters_users_post**](docs/api/UsersApi.md#clusters_users_post) | **POST** /clusters/{clusterId}/users | Create MongoDB User |

</details>

## Documentation For Models

All URIs are relative to *https://api.ionos.com/databases/mongodb*
<details >
<summary title="Click to toggle">API models list</summary>

 - [APIVersion](docs/models/APIVersion)
 - [ClusterList](docs/models/ClusterList)
 - [ClusterListAllOf](docs/models/ClusterListAllOf)
 - [ClusterLogs](docs/models/ClusterLogs)
 - [ClusterLogsInstances](docs/models/ClusterLogsInstances)
 - [ClusterLogsMessages](docs/models/ClusterLogsMessages)
 - [ClusterProperties](docs/models/ClusterProperties)
 - [ClusterResponse](docs/models/ClusterResponse)
 - [Connection](docs/models/Connection)
 - [CreateClusterProperties](docs/models/CreateClusterProperties)
 - [CreateClusterRequest](docs/models/CreateClusterRequest)
 - [CreateRestoreRequest](docs/models/CreateRestoreRequest)
 - [DayOfTheWeek](docs/models/DayOfTheWeek)
 - [ErrorMessage](docs/models/ErrorMessage)
 - [ErrorResponse](docs/models/ErrorResponse)
 - [Health](docs/models/Health)
 - [MaintenanceWindow](docs/models/MaintenanceWindow)
 - [Metadata](docs/models/Metadata)
 - [Pagination](docs/models/Pagination)
 - [PaginationLinks](docs/models/PaginationLinks)
 - [PatchClusterProperties](docs/models/PatchClusterProperties)
 - [PatchClusterRequest](docs/models/PatchClusterRequest)
 - [PatchUserProperties](docs/models/PatchUserProperties)
 - [PatchUserRequest](docs/models/PatchUserRequest)
 - [ResourceType](docs/models/ResourceType)
 - [SnapshotList](docs/models/SnapshotList)
 - [SnapshotListAllOf](docs/models/SnapshotListAllOf)
 - [SnapshotProperties](docs/models/SnapshotProperties)
 - [SnapshotResponse](docs/models/SnapshotResponse)
 - [State](docs/models/State)
 - [TemplateList](docs/models/TemplateList)
 - [TemplateListAllOf](docs/models/TemplateListAllOf)
 - [TemplateProperties](docs/models/TemplateProperties)
 - [TemplateResponse](docs/models/TemplateResponse)
 - [User](docs/models/User)
 - [UserMetadata](docs/models/UserMetadata)
 - [UserProperties](docs/models/UserProperties)
 - [UserRoles](docs/models/UserRoles)
 - [UsersList](docs/models/UsersList)


[[Back to API list]](#documentation-for-api-endpoints) [[Back to Model list]](#documentation-for-models)

</details>