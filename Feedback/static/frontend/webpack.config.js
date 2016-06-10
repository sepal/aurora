const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const PATHS = {
  app: path.join(__dirname, 'app'),
  build: path.join(__dirname, '../js')
};

module.exports = {
  entry: {
    app: PATHS.app
  },
  output: {
    path: PATHS.build,
    filename: 'feedback.js'
  },
  plugin: [
    new HtmlWebpackPlugin({
      title: 'Webpack demo',
    })
  ]
};