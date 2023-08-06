#!/bin/bash

green="$(tput setaf 2)"
bold="$(tput bold)"
reset="$(tput sgr0)"

for file in *.py; do
    echo "${green}${bold}Running test: ${file%.py}...${reset}"
    coverage run $file > /dev/null
    echo "Done."
    echo "==================="
    echo
    coverage report
    echo
    echo
done

mkdir pdf
mv ./*.pdf pdf

mkdir tex
mv ./*.tex tex
