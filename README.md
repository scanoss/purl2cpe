# Introduction

The purl2cpe project is a dataset that contains relations between CPEs (Common Product Enumerator) and PURLs (Package URL). 

[Mitre Corporation’s CVE Program](https://www.cve.org/) Mission  is to Identify, define, and catalog publicly disclosed cybersecurity vulnerabilities.
This program issues CVE IDs to identify new vulnerabilities.

The [NIST’s National Vulnerability Database](https://nvd.nist.gov/) analyzes each CVE and, among other things, issues CPE (Common Product Enumerator) IDs to identify specific component versions, and publishes the list of CPE to CVE relationship.

[PURL (Package URL)](https://github.com/package-url/purl-spec) is an open specification that standardizes identification and location of software packages/versions in their respective repositories.

While CPEs provide a precise identification for components and versions, they do not provide an easy way to connect these vulnerable component versions with their respective Open Source repositories. These connections must be made available by human curation.

SCANOSS specializes in Software Composition Analysis and Open Source Intelligence and maintains a dataset that connects PURLs to CPEs. This dataset has now been released as Open Source. 

With purl2cpe, it is now easy for anyone to monitor the Open Source packages they use for known vulnerabilities.

# Folder Structure
There are two main folders in this repo:
* [data](data)
* [utilities](utilities)

## Relationship Data
All purl2cpe relationship information is stored in the [data](data) folder.
The information inside this is structured based on the CPE `vendor` and `product` fields. 
Inside the [data](data) folder there is one sub-folder for each `vendor`, and subsequently one sub-folder for each `product` of that `vendor`.

Inside the `product` folder there are two files:
* `cpes.yml` stores all CPEs of that product
* `purls.yml` stores all related purls for that product.

For example, the path for the `aerospike_server` product from `aerospike` vendor would be:
```commandline
data/
    aerospike/
        aerospike_server/
            cpes.yml
            purls.yml
```

[cpes.yml](data/aerospike/aerospike_server/cpes.yml):
```yaml
cpes:
  - cpe:2.3:a:aerospike:aerospike_server:4.0.0.1:*:*:*:community:*:*:*
  - cpe:2.3:a:aerospike:aerospike_server:4.0.0.6:*:*:*:community:*:*:*
  - cpe:2.3:a:aerospike:aerospike_server:4.1.0.1:*:*:*:community:*:*:*
...
```
--------------------------------------------------------- 

[purls.yml](data/aerospike/aerospike_server/purls.yml):
```yaml
purls:
  - pkg:docker/aerospike/aerospike-server
  - pkg:github/aerospike/aerospike-server
```

### Contributing New Relationship Data
Our automation loads the latest `cpes.yml` files daily (directly from the NVD). That leaves the `purls.yml` relationship data.

If you find a missing/invalid relationship, please do the following:
- Fork the [repo](https://github.com/scanoss/purl2cpe)
- Update the affected `purls.yml` files
- Create a Pull Request with the details of the update

The PURL2CPE team will review these requests and accept them into list for everyone to benefit from.

## Utilities
Utilities to help consume this data are located in the [utilities](utilities) folder. More details can be found [here](utilities/README.md).

