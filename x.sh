#!/bin/bash
NOW=$(date +"%d-%m-%Y")
git add .
git commit -m "latest $NOW"
git push -u origin master
