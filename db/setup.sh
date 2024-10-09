#!/bin/bash
set -e
service mysql start
mysql < data.sql
service mysql stop