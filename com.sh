#!/bin/sh

git add .
git commit -m "readme"
echo 'nimrobotics' | sudo -S git push -u origin master

