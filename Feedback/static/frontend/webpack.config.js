const path = require('path');
const merge = require('webpack-merge');
const validate = require('webpack-validator');
const parts = require('./lib/parts');

// Define the input and output paths. Since django collects all static files
// from the static/js and static/css, webpack has to build into the parent
// folders.
const PATHS = {
  app: path.join(__dirname, 'app'),
  build: path.join(__dirname, '../'),
  js: 'js',
  css: 'css'
};

// Common config for all build types.
const common = {
  entry: {
    feedback: PATHS.app
  },
  output: {
    path: PATHS.build,
    filename: path.join(PATHS.js, '[name].js')
  },
  resolve: {
    extensions: ['', '.js', '.jsx'],
    alias: {
      // We're using react-lite since we don't need server side rendering. This
      // library is a lot smaller.
      // 'react': 'react-lite',
      // 'react-dom': 'react-lite'
    }
  },
  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        // Enable caching for improved performance during development // It uses default OS directory by default. If you need
        // something more custom, pass a path to it.
        // I.e., babel?cacheDirectory=<path>
        loaders: ['babel?cacheDirectory'],
        // Parse only app files! Without this it will go through
        // the entire project. In addition to being slow,
        // that will most likely result in an error.
        include: PATHS.app
      },
      {
        // Required by react-markdown
        test: /\.json$/,
        loader: 'json'
      }
    ]
  },
  plugins: []
};

var config;

// Build differently based on the npm command.
switch (process.env.npm_lifecycle_event) {
  case 'build':
    config = merge(
      common,
      {
        devtool: 'source-map'
      },
      parts.injectVariable(
        'process.env.NODE_ENV',
        'production'
      ),
      parts.extractBundle({
        name: 'feedback_vendor',
        entries: ['react']
      }),
      parts.minify(),
      parts.extractCSS(PATHS.app, PATHS.css)
    );
    break;
  default:
    config = merge(
      common,
      {
        devtool: 'source-map'
      },
      parts.extractCSS(PATHS.app, PATHS.css)
    );
}

module.exports = validate(config);