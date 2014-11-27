#!/bin/bash

python send-test.py -i localhost -p 8080 -s 42.23.42.42 -P 42
python send-test.py -i localhost -p 8080 -s 42.23.42.23 -P 23
python send-test.py -i localhost -p 8080 -s 42.23.42.133 -P 1337

