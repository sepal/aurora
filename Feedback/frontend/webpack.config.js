const path = require('path');
const merge = require('webpack-merge');
const parts = require('./lib/parts');

// Define the input and output paths. Since django collects all static files
// from the static/js.
const PATHS = {
  app: path.join(__dirname, 'app'),
  build: path.join(__dirname, '../static'),
  js: 'js',
};

// Common config for all build types.
const common = {
  context: path.resolve(__dirname, PATHS.app),
  entry: {
    feedback: './index.js'
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /(node_modules|bower_components)/,
        use: [{
          loader: "babel-loader",
        }]
      }
    ]
  },
  plugins: [],
  output: {
    path: PATHS.build,
    filename: path.join(PATHS.js, '[name].js')
  },
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
      parts.minify()
    );
    break;
  default:
    config = merge(
      common,
      {
        devtool: 'source-map'
      }
    );
}
module.exports = config;