#!/bin/bash
thd --triggers /etc/triggerhappy/triggers.d/ /dev/input/event* &
