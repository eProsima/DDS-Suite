# eProsima Suites

This repository defines the versions of the eProsima products that are contained in each of the eProsima suites, as well as their build options.
The eProsima suites are:

* **eProsima DDS Suite**: Suite of all DDS related products
* **Fast DDS Suite**: Suite of products related with Fast DDS
* **Micro XRCE-DDS Suite**: Suite of products related with Micro XRCE-DDS

Each of these suites is distributed by eProsima in the form of Docker images which can be downloaded [here](https://eprosima.com/index.php/downloads-all).

* [Repository's branching model](#repositorys-branching-model)
* [Versioning and tagging](#versioning-and-tagging)

## Repository's branching model

The repository tracks the version progression of the products contained in each of the suites through three principal branches, one for each suite.
Furthermore, since each suite is versioned following a SEMVER pattern, there exist tracking branches for each minor version of each suite (for more information of the suites' versioning schemas, please refer to [Versioning and tagging](#versioning-and-tagging)).
All these branches are captures in the following table:

| Suite | Principal branch | Version branches |
|-|-|-|
| eProsima DDS Suite | `eprosima-dds-suite` | `eprosima-dds-suite-<major>.<minor>.x` |
| Fast DDS Suite | `fastdds-suite` | `fastdds-suite-<major>.<minor>.x` |
| Micro XRCE-DDS Suite | `xrcedds-suite` | `xrcedds-suite-<major>.<minor>.x` |

## Versioning and tagging

Since this repository tracks the evolution of 3 different suites, each of them follows its own versioning and tagging model.

### eProsima DDS Suite

1. Starting at v1.0.0, each major version of eProsima DDS Suite is tied with a corresponding major version of Fast DDS, with eProsima DDS Suite v1 being tied with Fast DDS v2.
1. Similarly, each minor version of eProsima DDS Suite is tied with a minor version of Fast DDS, with eProsima DDS Suite v1.0 being tied with Fast DDS v2.5.
1. For any given version of eProsima DDS Suite, all its contained products minor versions are fixed.
1. The patch versions of eProsima DDS Suite are increased every time one of its contained products has a patch release on the minor version of the product tied to the corresponding minor version of eProsima DDS Suite.
1. All tags corresponding to this suite follow the pattern `eprosima-dds-suite-v<major>.<minor>.<patch>`

### Fast DDS Suite

1. The version of Fast DDS Suite corresponds to that of the contained Fast DDS.
1. If any of the contained products other than Fast DDS releases a patch version, a new build of Fast DDS Suite may be issued.
1. All tags corresponding to this suite follow the pattern `fastdds-suite-v<major>.<minor>.<patch>-<build>`, where `-<build>` is optional and may not be present.

### Micro XRCE-DDS Suite

1. The version of Micro XRCE-DDS Suite corresponds to that of the contained Micro XRCE-DDS Agent and Client.
1. If any of the contained products other than Micro XRCE-DDS Agent and Client releases a patch version, a new build of Micro XRCE-DDS Suite may be issued.
1. All tags corresponding to this suite follow the pattern `xrcedds-suite-v<major>.<minor>.<patch>-<build>`, where `-<build>` is optional and may not be present.
