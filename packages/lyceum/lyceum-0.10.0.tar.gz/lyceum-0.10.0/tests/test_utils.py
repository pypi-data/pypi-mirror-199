#!/usr/bin/env python

"""Tests for `lyceum.utils` package."""
import math

import pytest

from lyceum.utils import rep2dot


def test_rep2dot():
    assert rep2dot("/home/ben/Documents/Boulot/1NSI/TPs/TP13-SE-Linux-Hachette/TP13-PROF/activite",
                   include_files_patterns=["tresor.txt", "mystere.txt"]) == """digraph tree {"""
