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
  plugins: [
  ]
};

var config;

// Build differently based on the npm command.
switch(process.env.npm_lifecycle_event) {
  case 'build':
    config = merge(
      common,
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
      parts.clean(PATHS.build),
      parts.extractCSS(PATHS.app, PATHS.css)
    );
}

module.exports = validate(config);