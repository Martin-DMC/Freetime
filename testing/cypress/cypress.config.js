const { defineConfig } = require("cypress");
const viteConfig = require('./vite.config');

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },

  component: {
    devServer: {
      framework: "svelte",
      bundler: "vite",
      viteConfig,
    },
  },
});
