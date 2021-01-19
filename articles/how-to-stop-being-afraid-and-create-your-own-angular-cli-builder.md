# How to stop being afraid and create your own Angular CLI Builder

> _You can find the original article_ [_here_](https://indepth.dev/posts/1371/how-to-create-your-own-angular-builder)\_\_

![](../.gitbook/assets/image%20%281%29.png)

Angular CLI v8.0.0 brought us a stable CLI Builders API, which allows you to customize, replace, or even create new CLI commands

Now the most popular builder for customizing the `webpack` configuration is[ @angular-builders/custom-webpack](https://www.npmjs.com/package/@angular-builders/custom-webpack). If you look at the source code of all the builders supplied with the package, you will see very compact solutions that do not exceed 30 lines of code.

Maybe make your own?

Challenge Accepted!

_This material assumes that you are already familiar with the Angular and Angular CLI, you know what rxjs is and how to live with it, and you are also ready to read 50 lines of code._

### So what exactly are these builders? <a id="so-what-exactly-are-these-builders"></a>

**B**u**ilder** is just a function that can be called using the Angular CLI. It is called with two parameters:

1. JSON-like configuration object
2. `BuilderContext` — an object that provides access, for example, to the logger.

A function can be either synchronous or asynchronous. As a bonus, you can return `Observable`. But in any case, both `Promise` and `Observable` should emit `BuilderOutput`.

This function, packaged in a certain way in the npm package, can be used to configure such CLI commands as `build`, `test`, `lint`, `deploy`, and any other from the `architect` section of the `angular.json` configuration file.

### OK. Will there be just an example from the documentation? <a id="ok-will-there-be-just-an-example-from-the-documentation"></a>

Not. Of course, at first, I made an [example](https://github.com/ng-builders/ng-builders/blob/master/libs/build/src/command/index.ts), most similar to [the example from the documentation](https://angular.io/guide/cli-builder#creating-a-builder). I used such a builder when working with [NX](https://nx.dev/angular) and deploying only modified applications. But I suddenly needed a builder who can run commands from `angular.json` in a certain order and depending on each other.

A more real-world example: you suddenly needed your application running dev-server in tests. There are various console utilities and npm packages for starting and waiting for the server to start, but why not create a builder that can run dev-server in watch mode before running the tests and kill dev-server as soon as the tests are complete?

### Where to begin? <a id="where-to-begin"></a>

You need to start by creating a blank for the package in which we will pack the builders. I generated the workspace using[ NX](https://nx.dev/angular), as well as the library blank for the builder.

npx create-nx-workspace ng-builders  
cd ./ng-builders  
npx ng g @nrwl/node:library build

### Build Configuration <a id="build-configuration"></a>

This is how I saw the configuration that solved my problem:

```javascript
// angular.json
{
   "version": 1,
   "projects": {
     "app": {
       "architect": {
         "stepper": {
           "builder": "@ ng-builders / build: stepper",
           "options": {
             "targets": { // description of targets
               "jest": { // target name and configuration
                 "target": "app: jest", // existing task in angular.json
                 "deps": ["server"] // dependent targets that need to be run before the main
               },
               "server": {
                 "target": "app: serve",
                 "watch": true // watch mode
               }
             },
             "steps": ["jest"] // list of goals to complete
           }
         }
       }
     }
   }
 }
```

In theory, such a task in `angular.json` can be done using the command:

```bash
ng run app:stepper
```

Having worked a little on the specification, I came to the following interfaces:

```typescript
export interface Target {
   / **
    * A list of target ids that must be completed before starting the task
    *
    * Differs from Schema#steps in that the task does not wait for the full
    * performing dependent tasks
    * /
   deps?: string[];
   / **
    * Purpose to fulfill
    * /
   target: string;
   / **
    * Turn on watch mode
    * /
   watch?: boolean;
   / **
    * Overriding target configuration parameters
    * /
   overrides?: {[key: string]: any};
 }

 export interface Targets {
   // targetId - task name
   [targetId: string]: Target;
 }

 export interface Schema {
   / **
    * Strict sequence of tasks in the array
    * indicate targetId of Targets
    *
    * The next task is launched only after the previous
    * /
   steps: string[];
   targets: Targets;
 }
```

The specification is completed. Of course, the scheme can be further expanded and, for example, add a configuration choice \(production, dev, etc.\), but for `v1.0` this will be enough.

[JSON schema](https://github.com/ng-builders/ng-builders/blob/master/libs/build/src/stepper/schema.json) was also written on these interfaces, which will be used when validating configuration data.

### Let’s code <a id="let-s-code"></a>

So, we have a configuration interface. When starting a task through the Angular CLI, everything should work wonderfully.

To begin with, write the `runStepper` function and create the `StepperBuilder`.

```typescript
// index.ts
 export function runStepper(
   input: Schema,
   context: BuilderContext
 ): BuilderOutputLike {
   return buildSteps(input, context).pipe (
     map(() => ({
       success: true
     })),
     catchError(error => {
       return of({error: error.toString(), success: false});
     })
   );
 }

 export const StepperBuilder = createBuilder(runStepper);

 export default StepperBuilder;
```

Note that the type of the first argument of the `runStepper` function is the same `Schema` from the configuration specification above. The function returns `Observable<BuilderOutput>`.

Next, we will implement the `buildSteps` function, which will be responsible for the steps

{% code title="index.ts" %}
```typescript
 function buildSteps(config: Schema, context: BuilderContext): Observable<any> {
   return concat(
      config.steps.map(step => buildStep(step, config.targets, context))
   );
 }
```
{% endcode %}

It seems nothing complicated. Each next step is performed after the previous one is completed.

In fact, we have one thing that remains unknown — the `buildStep` function, which will run each individual step with its dependencies:

{% code title="index.ts" %}
```typescript
 function buildStep(
   stepName: string,
   targets: Targets,
   context: BuilderContext
 ): Observable<any> {
   const {deps = [], overrides, target, watch}: Target = targets[stepName];

   const deps$ = deps.length
     ?  combineLatest(deps.map(depName => buildStep(depName, targets, context)))
     : of(null);

   return deps$.pipe (
     concatMap(() => {
       return scheduleTargetAndForget(context, targetFromTargetString(target), {
         watch
         ...overrides
       });
     }),
     watch ? tap(noop) : take(1)
   );
 }
```
{% endcode %}

There are several interesting points in this function:

1. Step dependencies run in parallel, and the main task of the step is only after each of the dependencies emits at least one event. For example, this gives us a guarantee that the dev-server \(if the task to start it in the list of dependencies of the current step\) is launched before running the tests \(if this is the main task of the step\)
2. The function `scheduleTargetAndForget`, imported from `@angular-devkit/architect`. This function allows you to run targets from `angular.json` and override their settings. This function returns `Observable`, unsubscribing from which stops the task in progress.
3. If the `watch` parameter has a positive value, then the main task of the step will not end after the first emitted event, therefore the current task will live forever until it completes itself, or until the unsubscribe from the returned `Observable`, or the process is completed.

Actually, this is all about the builder itself. The full version can be viewed [here](https://github.com/ng-builders/ng-builders/blob/6fae264c2d068d74b7c85300d13b9c09e42fd60b/libs/build/src/stepper/index.ts). Stayed in 56 lines of code. Not bad, right?

The last point that is interesting and important for us is the `builders.json` file

{% code title="builders.json" %}
```javascript
{
   "$ schema": "../../@angular-devkit/architect/src/builders-schema.json",
   "builders": {
     "stepper": {
       "implementation": "./stepper",
       "schema": "./schema.json",
       "description": "Stepper"
     }
   }
 }
```
{% endcode %}

As you can see, this file lists the builders with the parameters “implementation” \(entry point for importing the builder\), “schema” \(validation scheme\) and “description”

Then we search for [package.json](https://github.com/ng-builders/ng-builders/blob/6fae264c2d068d74b7c85300d13b9c09e42fd60b/libs/build/package.json) and add the `builders` property with a relative path to the `builders.json` file

{% code title="package.json" %}
```javascript
{
  "name": "@ng-builders/build",
  "builders": "./builders.json",
  …
}
```
{% endcode %}

It remains only to collect the package:

```bash
npm run build
```

Add everything into a commit and push all this beauty to Github.

### And that’s all? <a id="and-that-s-all"></a>

Yes, that’s all. Three simple functions, a little imagination, and the fulfillment of mandatory configuration contracts are all that is needed to quickly create custom builders for the Angular CLI. But an attentive reader, of course, will point out the lack of tests for a new builder. And I hope that this very reader unexpectedly ignites himself with the desire to close this gap, [forks the project](https://github.com/ng-builders/ng-builders), and will try to write tests himself.

The builder can NOT be used \(as soon as tests appear, I will definitely remove NOT\) in your projects

```bash
npm i @ng-builders/build -D
```

### Summary <a id="summary"></a>

The CLI Builders API is a powerful tool for extending and customizing the Angular CLI. The builder created by us does not solve the most popular problems, but it took only 1 hour to create the whole package. This means that creating a custom builder to solve particular problems is not such a difficult task.

What other builders can you create? It can be a builder for deploying, testing, and codebase checking for your application using special tools. It all depends on your needs and imagination.

#### P.S.: <a id="p-s-"></a>

Angular CLI Builders are perfectly used and work in NX Workspace even without Angular. An example of this miracle I will definitely show you in the future. In the meantime, you can read me on [Twitter](https://twitter.com/katsuba_igor), write to me on [Telegram](https://t.me/katsuba), and speak only good words.

