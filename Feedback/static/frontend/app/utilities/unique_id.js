let seen_ids = {};

/**
 * Returns a string to use as an html id and guaranties its uniqueness.
 *
 * @param string name The string which should be converted to an html id.
 */
export default function (name) {
  let str = name.toLowerCase();
  // Some characters are replaced by hyphens.
  str = str.replace(/[\s_\[]]+/g, '-');
  // http://www.w3.org/TR/html4/types.html#type-name defines that ids can only
  // contain digits, hyphens, underscore, colons and periods, so we'll strip
  // all other characters.
  str = str.replace(/[^A-Za-z0-9\-_]/g, '');

  let id = '';
  // If the id was already used, then lets change the id and increase the
  // counter, otherwise create a new entry.
  if (str in seen_ids) {
    id = `${str}--${seen_ids[str]}`;
    seen_ids[str]++;
  } else {
    seen_ids[str] = 1;
  }

  return id;
}