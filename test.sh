#!/usr/bin/env bash

bazel test //... --test_output=all
bazel run //example:example
