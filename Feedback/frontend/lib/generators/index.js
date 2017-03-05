/**
 * Config file for plop, a generator app
 * This allows us to quickly generate components and other stuff.
 */

const componentGenerator = require('./component');

module.exports = (plop) => {
  plop.setGenerator('component', componentGenerator);
};