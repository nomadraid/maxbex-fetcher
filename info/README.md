## The Problem.

The trading team has requested an external data source, you can view the website page [https://publicationtool.jao.eu/core/maxExchanges](https://publicationtool.jao.eu/core/maxExchanges). The team has requested historical data for the past month and for the data from the external source to be available. The data will need to be scraped and stored in a timeseries for each separate key on the page. The engineering team has been tasked with building a scraper that can scrape the data source on a continuous basis (also historical dates) to retrieve the data when it is released.

## Assumptions

* The trading team are able to connect and consume the data from a db when it is stored.
* The data doesn't remain static after it is published.

## Solution Requirements

* Code that will scrape the data source for historical dates.
* Code that will scrape the data source on a continuous basis.
* Code that will insert timeseries data into a database (your choice).
* DB schema that supports a timeseries model.

## Hints

* The data from the website can be retrieved from an api endpoint and example call is https://publicationtool.jao.eu/core/api/data/maxExchanges?FromUtc=2022-10-22T22%3A00%3A00.000000Z&ToUtc=2022-10-23T22%3A00%3A00.000000Z
* You may use a framework to fulfill the solution requirements.
* You may use a database of your choice.

## Additional questions
----------------------------------------------------------------------------------------------------------------
* What db did to use and why?
----------------------------------------------------------------------------------------------------------------

TimescaleDB is an open-source, time-series SQL database that is built on top of PostgreSQL. It is fully ACID compliant, meaning that it supports Atomicity, Consistency, Isolation, and Durability, which are the four properties of a relational database management system that guarantee data integrity and consistency.

In terms of insert and query performance, TimescaleDB is designed specifically for time-series data, and provides significantly faster insert and query performance than a standard PostgreSQL setup. This is due to the way TimescaleDB is designed to handle time-series data, which involves creating separate tables for each time interval (e.g. daily, hourly, etc.) and using a hypertable to query across all of the interval tables. This allows TimescaleDB to take advantage of PostgreSQL's built-in indexes and perform queries much more efficiently than if the data were stored in a single table.

TimescaleDB is also designed to be highly scalable, allowing it to handle large amounts of time-series data. TimescaleDB supports sharding, which allows data to be distributed across multiple machines to improve performance and scalability. It also allows to partition data by time, which helps to avoid the "hot-spot" problem that can occur with time-series data when all of the data is stored in a single table.
Compared to PostgreSQL, TimescaleDB has some key differences:

- TimescaleDB is built specifically for time-series data and provides better performance and scalability when working with time-series data than PostgreSQL.
- TimescaleDB provides built-in support for time-series data operations such as time-based aggregation and downsampling, which are not available in PostgreSQL.
- TimescaleDB provides a plugin architecture for data retention policies and data management, which is not available

----------------------------------------------------------------------------------------------------------------
* How to build redundant scraping code?
----------------------------------------------------------------------------------------------------------------

Building redundant scraping code involves creating multiple instances of your scraping code that can run simultaneously and independently of each other. This can be achieved by using a distributed scraping framework, such as Scrapy Cluster or Portia, or by running multiple instances of your scraping code on different machines or in different containers.

Additionally, you can also implement redundancy at the database level by using a replicated database system, such as MySQL or MongoDB, that allows for multiple copies of the data to be stored and automatically synced across different machines.

Another way to achieve redundancy is to use a load balancer in front of your scraping instances, this way if one instance goes down, the load balancer can route traffic to the other working instances.
Finally, it's also important to build in error handling and monitoring to your scraping code so that you can detect and address any issues that may arise.

----------------------------------------------------------------------------------------------------------------
* How to test a data scraper?
----------------------------------------------------------------------------------------------------------------

There are several ways to test a data scraper, including:

- Unit testing: This involves writing individual test cases for each function or method in the scraper to ensure they are working correctly.

- Functional testing: This involves testing the entire scraper end-to-end, by running it against a sample of the website and checking if the output is as expected.

- Integration testing: This involves testing the scraper in conjunction with other components in your system, such as the database or the visualization layer, to ensure that the data is being stored and displayed correctly.

- Performance testing: This involves testing the scraper's performance under different loads and conditions, such as high traffic or slow internet speeds, to ensure it can handle real-world scenarios.

- Stress testing: This involves testing the scraper's performance under high loads or with large amounts of data, to ensure it can handle extreme conditions.

- Monitoring: This involves continuously monitoring the scrape process and data for any errors or anomalies.
It's important to have a good test coverage, and test your scraping process in different scenarios to ensure it will work as expected.

----------------------------------------------------------------------------------------------------------------
* Data catalogue design?
----------------------------------------------------------------------------------------------------------------

A data catalog is a critical component of a data pipeline when working with time-series energy trading data for a fast growing analytics company. Here are some best practices for designing a data catalog:

- Data discovery: The data catalog should make it easy for users to discover and understand the data that is available. This may include providing metadata, data dictionaries, and data lineage information to help users understand the data and how it has been processed.

- Data access: The data catalog should provide a simple and user-friendly interface for accessing data. This may include providing data visualization tools, data access APIs, and self-service data preparation tools to help users access and work with data.
Data security: The data catalog should provide a secure environment for data access. This may include providing role-based access control, data encryption, and data masking features to help protect sensitive data.

- Data governance: The data catalog should support data governance processes to ensure that data is being used ethically, legally, and in compliance with company policy. This may include providing data lineage information, data quality metrics, and data governance workflows to help users understand the data and its usage.

- Data integration: The data catalog should be integrated with the data pipeline to provide a single source of truth for data. This may include providing data integration capabilities such as data mapping, data transformation, and data quality checks to help users integrate data from different sources.

- Data management: The data catalog should provide tools for data management such as data archival, data retention, and data deletion. This will help the company to adhere to legal and regulatory requirements for data retention and deletion.
- Searchability: The data catalog should be searchable and able to be queried to help the users find the data they need quickly.

- Metrics and monitoring: The data catalog should provide monitoring and metrics on data usage, data quality, and data lineage to help identify and resolve any issues that may arise.

- Scalability: The data catalog should be designed to scale horizontally and vertically.

----------------------------------------------------------------------------------------------------------------
* Data pipeline design?
----------------------------------------------------------------------------------------------------------------

When working with time-series energy trading data for a fast growing analytics company, there are a number of best practices to keep in mind when designing your data pipeline:

- Data integration: Energy trading data is often sourced from multiple systems, such as SCADA systems, trading platforms, and weather forecasts. It's important to have a robust data integration strategy in place to handle data from multiple sources and ensure that it is cleaned, transformed, and loaded into the data warehouse in a consistent format.

- Data quality: Data quality is critical when working with time-series energy trading data. It's important to have a data quality process in place to ensure that data is accurate, complete, and consistent. This may involve validating data against business rules, removing duplicate or inconsistent data, and providing feedback to data providers to improve data quality.

- Data modeling: Time-series energy trading data is often complex and requires sophisticated data modeling techniques to make it usable for analysis. It's important to have a data modeling process in place to ensure that the data is organized and structured in a way that makes it easy to analyze and understand.

- Data storage: Time-series data requires a storage solution that can handle large amounts of data and support high-performance queries. Time-series databases such as InfluxDB, TimescaleDB, and OpenTSDB are designed to handle this type of data, and are a good choice for energy trading data.

- Data governance: As the data pipeline and the company grow, it's important to have a data governance process in place to ensure that data is being used ethically, legally, and in compliance with company policy.
Scalability and performance: The energy trading market is fast-paced and high-volume, and the pipeline should be able to handle it, it should be designed to scale horizontally and vertically as the data volume and complexity increases.

- Monitoring and alerting: It's important to have a monitoring and alerting system in place to ensure that the data pipeline is running smoothly and to quickly identify and resolve any issues that may arise.

- Automation: Automation can help to reduce the manual effort and errors involved in data pipeline management. Automating data pipeline management tasks, such as data ingestion, data quality checks, data modeling and data processing can help to reduce the time and effort required to maintain a data pipeline.

- Flexibility: The data pipeline should be flexible and adaptable to changing requirements and technologies. As the company grows and evolves, the data pipeline should be able to evolve with it.

----------------------------------------------------------------------------------------------------------------
* Thoughts on [https://martinfowler.com/articles/data-monolith-to-mesh.html](https://martinfowler.com/articles/data-monolith-to-mesh.html)
----------------------------------------------------------------------------------------------------------------

Failures of today's data platforms:
1. It is centralized, monolithic and domain agnostic a.k.a. data lake
2. Coupled pipeline decomposition
3. Siloed and hyper-specialized ownership

The next enterprise data platform architecture embraces the ubiquitous data with a distributed Data Mesh. The paradigm shift is in the convergence of:
1. Data
2. Distributed Domain Driven Architecture
3. Product Thinking with Data
4. Self-serve Platform Design


##### Data and distributed domain driven architecture convergence
! The architectural quantum in a domain oriented data platform, is a domain and not the pipeline stage.
- Domain oriented data decomposition and ownership
- Source oriented domain data
- Consumer oriented and shared domain data
- Distributed pipelines as domain internal implementation

##### Data and product thinking convergence
- Domain data as a product
- Discoverable
- Addressable
- Trustworthy and truthful
- Self-describing semantics and syntax
- Inter-operable and governed by global standards
- Secure and governed by a global access control
- Domain data cross-functional teams

##### Data and self-serve platform design convergence
The key to building the data infrastructure as a platform is:
- to not include any domain specific concepts or business logic, keeping it domain agnostic,
- make sure the platform hides all the underlying complexity and provides the data infrastructure components in a self-service manner.