/** @type {import("@typescript-eslint/experimental-utils").TSESLint.Linter.Config} */
module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
  },
  ignorePatterns: ["static/**/*", "dist/**/*", "**/node_modules/**/*", "asset/**/*"],
  extends: [
    '@nuxtjs/eslint-config-typescript',
    'plugin:nuxt/recommended',
    'prettier',
  ],
  plugins: [],
  rules: {},
}
