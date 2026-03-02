# Fast DDS Suite

This repository defines the versions of the eProsima products that are contained in the Fast DDS Suite, as well as their build options.

The **Fast DDS Suite** is a comprehensive suite of products related with Fast DDS, distributed by eProsima in the form of Docker images which can be downloaded [here](https://eprosima.com/index.php/downloads-all).

## Repository's branching model

The repository tracks the version progression of the products contained in the Fast DDS Suite through two types of branches:

* **`fastdds-suite`**: The principal branch that points all repositories to their `main` or `master` branches, representing the latest development versions of all products.

* **`fastdds-suite-<major>.<minor>.x`**: Version tracking branches that pin all repositories to their latest corresponding release for that specific Fast DDS version. For example, branch `fastdds-suite-3.4.x` will point to Fast DDS 3.4.x latest release and the compatible versions of all other products in the suite.

## Versioning and tagging

### Fast DDS Suite

1. The version of Fast DDS Suite corresponds to that of the contained Fast DDS.
1. If any of the contained products other than Fast DDS releases a patch version, a new build of Fast DDS Suite could be issued.
1. All tags corresponding to this suite follow the pattern `fastdds-suite-v<major>.<minor>.<patch>-<build>`, where `-<build>` is optional and may not be present.
