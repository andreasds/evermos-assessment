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

## Setup

```bash
./scripts/setup-dev.sh
```
