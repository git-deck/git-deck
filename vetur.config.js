/** @type {import('vls').VeturConfig} */
module.exports = {
  settings: {
    "vetur.useWorkspaceDependencies": true,
    "vetur.experimental.templateInterpolationService": true
  },
  projects: [
    {
      root: './webapp', // ←ここをvueプロジェクトのフォルダに合わせる
      package: './package.json',
      tsconfig: './tsconfig.json',
    }
  ]
}