# SWIFT code REST API

This project is a RESTful API built with **Django REST Framework** to parse, store, and serve SWIFT code data for banks in various countries. The API allows querying by individual SWIFT code or by country (using ISO-2 country codes). The application is containerized using Docker, and the data is stored in PostgreSQL database for fast, low-latency querying.

## Table of Contents

* [Main Technologies](#main-technologies)
* [Setup Instructions](#setup-instructions)

## Main Technologies

* **Python**
* **Django**
* **Django Rest Framework**
* **PostgreSQL**
* **Docker**

## Setup Instructions

### Prerequisites

Before setting up ensure you have the following installed:
* Docker - for containerization
* Docker Compose - for running multi-container application
* Git - for cloning the repository

### Installation and Preparation

1. Clone the github repository
```bash
git clone https://github.com/jcyran/swift_code_api.git
cd swift_code_api
```
2. 

