#!/bin/bash
dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone_test.psql
python3 test_app.py