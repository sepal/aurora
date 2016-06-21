# Aurora feedback system

This app provides a page, where students can give feedback for 
aurora system and the staff can manage those issues on a kanban like 
system.

The app is build on top of [react](https://facebook.github.io/react/) 
and some additional frontend tools, to simulate trello as best as 
possible, while keeping a maintainable code base.

The code is split into a generic backend code in django and a client 
side code in `static/frontend`.

## Requirements

You will [nodejs](http://nodejs.org/) > 4 and I also suggest upgrading
npm:
```
npm update -g npm
```

The provided vagrant box comes with nodejs, so you also should be able
to compile the frontend code with the provided tools there.

## Developing

The frontend code is bundled into components, which means each module is 
bundled into a GUI component. A component contains at least one 
(React Component)[] and can be a stateless single function or a class.
It can optionally have a styling which is scoped to that component only.

### New components
You can generate new components using the command
```
npm run generate component
```
which ask you a couple of questions like the name and type of component
and then places it into `./app/components`.

### Styling components

The stylesheet is generated using [PostCSS](https://github.com/postcss/postcss), 
[React-CSS-Modules](https://github.com/gajus/react-css-modules) and [SASS](http://sass-lang.com/).

This allows classes to be bound to the the single UI component. This 
means that for example a the css class `.lane` in `app/components/Lane`
is only applied main div of the lane component.

Additionally there are also some global style settings in the folder
`app/styles/config` like a colors and global spacing variables.
There is also `app/style/abstract` dir, which contains some mixins to
apply generic stylings.

### Compiling

While developing you can use the command:
```
npm run start
```
which will watch for changes in the frontend code and recompile the 
code.

With 
```
npm run build
```
can be used for the compile the code for production, which means that 
the js and css code will be minified and unglified.

You should **not** edit the feedback.css or *.js files directly, since 
they will be overridden with the the next compile!