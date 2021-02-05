# Online Store 12.12 Event

## Problem happened

* Lost handling when the order is bigger than the current stock
* Unhandled usage of shared resources (current stock value at this case)
  when used at the same time (race condition)

## Solution offered

* Put a lock around the shared data to ensure only one thread can access
  the data at a time

## Requirements

* [Docker](https://docs.docker.com/get-docker/) Docker Engine
* [MySQL](https://www.mysql.com) MySQL Database
* [Python](https://www.python.org/downloads) Python programming language
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) Micro web framework

## Setup

```bash
./scripts/setup-dev.sh
```

From that script, we have:

* Database run at port 17306 with root password `mysql-admin`
* Backend run with API access port 18001

## How to Run

```bash
./scripts/run.sh
```

* API Endpoint will run at http://localhost:18001/

## How to Run manually

```bash
python -m online_store --conf configs/online-store.conf
```
