# Tools used in the project
The following lists the tools and frameworks, that are used in the project. 
- [Docker](https://docs.docker.com/get-started/overview/)    
   Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications. By taking advantage of Docker's methodologies for shipping, testing, and deploying code, you can significantly reduce the delay between writing code and running it in production.
- [Kubernetes](https://kubernetes.io/docs/concepts/overview/)   
   Kubernetes is a portable, extensible, open source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation. It has a large, rapidly growing ecosystem. Kubernetes services, support, and tools are widely available. Kubernetes provides you with a framework to run distributed systems resiliently. It takes care of scaling and failover for your application, provides deployment patterns, and more. 
- [FastAPI](https://fastapi.tiangolo.com/tutorial/)   
   FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints.
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)   
   SQLAlchemy is basically referred to as the toolkit of Python SQL that provides developers with the flexibility of using the SQL database. The benefit of using this particular library is to allow Python developers to work with the language’s own objects, and not write separate SQL queries. They can basically use Python to access and work with databases. SQLAlchemy is also an Object Relational Mapper which is a technique used to convert data between databases or OOP languages such as Python.
- [FastAPI with SQLAlchemy](https://fastapi.tiangolo.com/tutorial/sql-databases/)   
   FastAPI with SQLAlchemy combines the benefits of FastAPI for building APIs with SQLAlchemy for database interaction. It allows developers to rapidly create RESTful APIs with automatic interactive documentation (Swagger UI) while leveraging SQLAlchemy's powerful ORM capabilities for database operations.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)   
   Alembic provides for the creation, management, and invocation of change management scripts for a relational database, using SQLAlchemy as the underlying engine.
- [Swagger UI](https://swagger.io/tools/swagger-ui/)   
   Swagger UI allows anyone — be it your development team or your end consumers — to visualize and interact with the API’s resources without having any of the implementation logic in place. It’s automatically generated from your OpenAPI (formerly known as Swagger) Specification, with the visual documentation making it easy for back end implementation and client side consumption.

# GitLab CI/CD

The following is a collection of short hints on how to do the most essential things in a GitLab CI/CD pipeline:

- How to delay a job until another job is done: 
  
By using 'needs' you can specify dependencies between different jobs.

- How to change the image used in a task:
 
By using the 'image' key, you can specify the name of the Docker image. 
You can further customize it by using two sub-keywords: 'name' to define the image name and 'entrypoint' to define the entrypoint.
    
- How do you start a task manually:

A job can be specified to run manually using the 'when: manual' syntax. Once defined, the job can be started in the GitLab Pipeline UI by clicking the "Play" button.

- The Script part of the config file - what is it good for?

The script part defines the commands or script to be executed as part of a job. It is good for automating repetitive tasks associated with the development lifecycle, error handling, logging, and output.


- If I want a task to run for every branch I put it into the stage ??

 + If I want a task to run for every branch I put it into the stage commit

- If I want a task to run for every merge request I put it into the stage ??
 
 +If I want a task to run for every merge request I put it into the stage acceptance

- If I want a task to run for every commit to the main branch I put it into the stage ??

 + If I want a task to run for every commit to the main branch I put it into the stage Release

# flake8 / flakeheaven

- What is the purpose of flake8?

- What types of problems does it detect

- Why should you use a tool like flake8 in a serious project?

## Run flake8 on your local Computer

  It is very annoying (and takes a lot of time) to wait for the pipeline to check the syntax 
  of your code. To speed it up, you may run it locally like this:

### Configure PyCharm (only once)
- select _Settings->Tools->External Tools_ 
- select the +-sign (new Tool)
- enter Name: *Dockerflake8*
- enter Program: *docker*
- enter Arguments: 
    *exec -i 1337_pizza_web_dev flakeheaven lint /opt/project/app/api/ /opt/project/tests/*
- enter Working Directory: *$ProjectFileDir$*

If you like it convenient: Add a button for flake8 to your toolbar!
- right click into the taskbar (e.g. on one of the git icons) and select *Customize ToolBar*
- select the +-sign and Add Action
- select External Tools->Dockerflake8

### Run flake8 on your project
  - Remember! You will always need to run the docker container called *1337_pizza_web_dev* of your project, to do this! 
    So start the docker container(s) locally by running your project
  - Now you may run flake8 
      - by clicking on the new icon in your toolbar or 
      - by selecting from the menu: Tools->External Tools->Dockerflake8 

# GrayLog

- What is the purpose of GrayLog?
   GrayLog is a powerful open-source log management tool that helps in collecting, indexing, and analyzing log data from various sources. It is used to monitor systems, troubleshoot issues, and gain insights from log data. 


- What logging levels are available?
   Logging levels determine the severity or importance of the messages being logged. Common logging levels include:

     DEBUG: Detailed information, typically of interest only when diagnosing problems.
     INFO: Confirm that things are working as expected.
     WARN: An indication that something unexpected happened, or indicative of some problem in the near future (e.g., ‘disk space low’). The software is still working as expected.
     ERROR: Due to a more serious problem, the software has not been able to perform some function.
     FATAL: Severe errors that cause premature termination. Expect these to be immediately visible on a status console.

- What is the default logging level?
      For many systems and programming environments, the default logging level is often INFO or WARNING.

- Give 3-4 examples for logging commands in Python:
  ```python
Basic Logging Setup:

import logging
logging.basicConfig(level=logging.INFO)

Logging a Debug Message:
logging.debug("This is a debug message")

Logging an Info Message:
logging.info("This is an info message")

Logging a Warning Message:
logging.warning("This is a warning message")

Logging an Error Message:
logging.error("This is an error message")
  ```

# SonarQube

- What is the purpose of SonarQube?
+ SonarQube is used for writing clean code. It helps in managing Code Quality, it can perform static Code Analysis and Security Vulnerability Detection.

- What is the purpose of the quality rules of SonarQube?
+ The quality rules are guidelines and criteria for evaluating the quality of code. There are four types of rules:
   - Code Smell (maintainability domain)
   - Bug (reliability domain)
   - Vulnerability (security domain)
   - Security hotspot (security domain)

- What is the purpose of the quality gates of SonarQube?
  The quality gates in SonarQube play a crucial role in maintaining and improving code quality by providing a structured and automated way to enforce quality standards. They help prevent poor-quality code from progressing through the development lifecycle, thus ensuring that the final product is robust, maintainable, and secure.
  Quality gates in SonarQube are composed of various conditions that a project must meet:
    -Code Coverage: The percentage of code covered by automated tests.
    -New Bugs: The number of bugs introduced in the new code.
    -New Vulnerabilities: The number of security vulnerabilities in the new code.
    -New Code Smells: The number of maintainability issues in the new code.
    -Duplicated Lines: The percentage of code duplication.
    -Technical Debt: The estimated effort to fix all maintainability issues.


## Run SonarLint on your local Computer

It is very annoying (and takes a lot of time) to wait for the pipeline to run SonarQube. 
To speed it up, you may first run the linting part of SonarQube (SonarLint) locally like this:

### Configure PyCharm for SonarLint (only once)

- Open *Settings->Plugins*
- Choose *MarketPlace*
- Search for *SonarLint* and install the PlugIn

### Run SonarLint

- In the project view (usually to the left) you can run the SonarLint analysis by a right click on a file or a folder. 
  You will find the entry at the very bottom of the menu.
- To run it on all source code of your project select the folder called *app*

# VPN

The servers providing Graylog, SonarQube and your APIs are hidden behind the firewall of Hochschule Darmstadt.
From outside the university it can only be accessed when using a VPN.
https://its.h-da.io/stvpn-docs/de/ 