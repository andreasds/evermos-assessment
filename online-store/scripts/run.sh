#!/bin/bash

docker exec \
    -it \
    online-store-be \
    python -m online_store \
        --conf configs/online-store.conf
