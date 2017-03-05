/**
 * Component generator config.
 */

module.exports = {
  description: 'Create a new component',
  prompts: [
    {
      type: 'list',
      name: 'type',
      message: 'Select the component type',
      default: 'Stateless function',
      choices: () => ['Class', 'Stateless function']
    },
    {
      type: 'input',
      name: 'name',
      message: 'What should be the name of new component?',
      validate: value => {
        if ((/.+/).test(value)) {
          return true;
        }

        return 'A new is required';
      }
    },
    {
      type: 'confirm',
      name: 'addStylesheet',
      default: true,
      message: 'Generate a stylesheet?'
    }
  ],
  actions: data => {
    var actions = [
      {
        type: 'add',
        path: '../../app/components/{{properCase name}}/index.js',
        templateFile: data.type == 'Class' ?  './component/class.js.hbs' : './component/stateless.js.hbs',
        abortOnFail: true
      }
    ];

    if (data.addStylesheet) {
      actions.push({
        type: 'add',
        path: '../../app/components/{{properCase name}}/style.scss',
        templateFile: './component/styles.scss.hbs'
      })
    }
    return actions;
  }
};