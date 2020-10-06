# Recreating a FiveThirtyEight chart using vx

https://observablehq.com/@hshoff/a-rather-lazy-recreation-of-a-fivethirtyeight-chart-using-v@428

View this notebook in your browser by running a web server in this folder. For
example:

~~~sh
python -m SimpleHTTPServer
~~~

Or, use the [Observable Runtime](https://github.com/observablehq/runtime) to
import this module directly into your application. To npm install:

~~~sh
npm install @observablehq/runtime@4
npm install https://api.observablehq.com/@hshoff/a-rather-lazy-recreation-of-a-fivethirtyeight-chart-using-v.tgz?v=3
~~~

Then, import your notebook and the runtime as:

~~~js
import {Runtime, Inspector} from "@observablehq/runtime";
import define from "@hshoff/a-rather-lazy-recreation-of-a-fivethirtyeight-chart-using-v";
~~~

To log the value of the cell named “foo”:

~~~js
const runtime = new Runtime();
const main = runtime.module(define);
main.value("foo").then(value => console.log(value));
~~~
