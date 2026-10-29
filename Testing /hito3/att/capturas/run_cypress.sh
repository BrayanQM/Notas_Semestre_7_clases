#!/usr/bin/env bash
cd "/home/eynor/Documents/semestr7/Testing /hito3/att/appTesting" || exit 1
clear
echo '$ npx cypress run --spec 8_pruebaUICypress.cy.js'
echo
npx cypress run --spec 8_pruebaUICypress.cy.js
