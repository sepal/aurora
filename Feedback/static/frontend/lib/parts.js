const path = require('path');
const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const autoprefixer = require('autoprefixer');

// Adds CSS and SASS loaders with autoprefixer using postcss and extracts them into a seperate file.
exports.extractCSS = function (paths, output_dir) {
  console.log(paths);
  return {
    module: {
      loaders: [
        {
          test: /\.css$/,
          loader: ExtractTextPlugin.extract('style', 'css!postcss'),
          include: paths
        },
        {
          test: /\.scss$/,
          loader: ExtractTextPlugin.extract('style', 'css!sass!postcss'),
          include: paths
        }
      ]
    },
    plugins: [
      // Output extracted CSS to a file.
      // todo: make the output folder configurable.
      new ExtractTextPlugin(path.join(output_dir, 'feedback.css'))
    ],
    postcss: function () {
      return [autoprefixer];
    }
  };
};

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