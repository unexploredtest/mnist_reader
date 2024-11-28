#!/bin/bash

for filename in data/*.gz; do gzip -kd "${filename}"; done
