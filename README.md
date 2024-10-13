# Frontend for ATOM Project

This repository contains the frontend of the ATOM project, which is responsible for the user interface and communication with the backend API.

To start the project, you need:

- Download the repository.
- Install dependencies via (list is in the file `package.json`)
- Launch Api (master branch)
- Run the project using `npm run serve`

## Short description of the project files:

├── `public`

│ ├── Frame.svg <- Main SVG image used in the UI

│ ├── favicon.ico <- Website icon

│ ├── `index.html` <- Main HTML file

├── `src`

│ ├── assets <- Static assets folder (images, styles, etc.)

│ ├── fonts <- Custom fonts

│ ├── router <- Vue Router configuration

│ ├── store <- Vuex store for state management

│ ├── `App.vue` <- Root Vue component

│ ├── `main.js` <- Entry point for the Vue app

├── .gitignore <- Ignored files for Git

├── babel.config.js <- Babel configuration for transpiling JavaScript

├── jsconfig.json <- Configuration for JavaScript development

├── package-lock.json <- Lock file for dependencies

├── `package.json` <- List of project dependencies

└── vue.config.js <- Vue CLI configuration
