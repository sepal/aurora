const path = require('path');
const webpack = require('webpack');

// Minifyies the build for production using the the webpack UglifyJsPlugin.
exports.minify = function () {
  return {
    plugins: [
      new webpack.optimize.UglifyJsPlugin({
        compress: {
          warnings: false
        }
      })
    ]
  };
};

// Inject variables during build time.
exports.injectVariable = function (key, value) {
  const env = {};
  env[key] = JSON.stringify(value);
  return {
    plugins: [
      new webpack.DefinePlugin(env)
    ]
  };
};

// Extract JS bundles as seperate files.
exports.extractBundle = function (options) {
  const entry = {};
  entry[options.name] = options.entries;
  return {
    // Define an entry point needed for splitting.
    entry: entry,
    plugins: [
      // Extract bundle and manifest files. Manifest is
      // needed for reliable caching.
      new webpack.optimize.CommonsChunkPlugin({
        names: [options.name, 'feedback_manifest'],
        // options.name modules only
        minChunks: Infinity
      })
    ]
  };
};