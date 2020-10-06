// https://observablehq.com/@hshoff/a-rather-lazy-recreation-of-a-fivethirtyeight-chart-using-v@428
export default function define(runtime, observer) {
  const main = runtime.module();
  main.variable(observer()).define(["md"], function(md){return(
md`
  # Recreating a FiveThirtyEight chart using vx

  
`
)});
  main.variable(observer()).define(["html"], function(html){return(
html`
  <div id="chart"></div>
`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`
Reference Chart: [https://projects.fivethirtyeight.com/trump-approval-ratings/](https://projects.fivethirtyeight.com/trump-approval-ratings/)<br/>
Data Sources: [polls](https://projects.fivethirtyeight.com/trump-approval-data/approval_polllist.csv), [trend lines](https://projects.fivethirtyeight.com/trump-approval-data/approval_topline.csv)<br/>
react + d3 = vx: [github.com/hshoff/vx](https://github.com/hshoff/vx)

I stumbled on this chart in the [FiveThirtyEight](http://fivethirtyeight.com/) sidebar. And at the bottom of the article it says "Download the data", and thought "I should try to remake that". But not a pixel perfect remake...like a "this is an interview and you have 30 minutes to recreate this" kind of remake. The tooltip is left as an excersize for the reader and can be done with [\`@vx/tooltip\`](https://github.com/hshoff/vx/tree/master/packages/vx-tooltip).

**[Note]** Observable doesn't support the JSX transform [yet](https://twitter.com/tmcw/status/996439254266888192), so you have to use the \`React.createElement(type, [props], [...children])\` api. Which happens to be a lot to type so I aliased the function to \`$()\` as a nod to my jQuery days.
`
)});
  main.variable(observer()).define(["Scale","Shape","Axis","Curve","React","d3","width","polls","trends","Group","Grid","ReactDOM"], function(Scale,Shape,Axis,Curve,React,d3,width,polls,trends,Group,Grid,ReactDOM)
{
  const { scaleLinear, scaleTime } = Scale;
  const { Area, Line, LinePath } = Shape;
  const { AxisLeft, AxisBottom } = Axis;
  const { curveLinear } = Curve;
  
  const $ = React.createElement;

  const parseTime = d3.timeParse("%m/%e/%Y");
  const formatTime = d3.timeFormat("%B");
  const formatNumber = d3.format(".1f");
  
  const margin = {
    top: 20,
    left: 40,
    right: 160,
    bottom: 40
  };

  const height = 500;
  const h = height - margin.top - margin.bottom;
  const w = width - margin.left - margin.right;

  
  const TrumpPolls = polls.filter((d, i) => d.president === 'Donald Trump' && i % 2 === 0)
  const TrumpTrends = trends.filter((d, i) => d.president === 'Donald Trump' && i % 7 === 0)
  
  const x = d => parseTime(d.modeldate);
  const xValues = TrumpTrends.map(d => x(d));
  
  const approve = d => parseFloat(d.approve_estimate);
  const disapprove = d => parseFloat(d.disapprove_estimate);
  
  const xScale = scaleTime({
    range: [0, w],
    domain: [Math.min(...xValues), Math.max(...xValues)]
  });
  const yScale = scaleLinear({
    range: [h, 0],
    domain: [20, 80]
  });

  const Chart = function() {
    return (
      $('svg', { width, height }, [
        $(Line, {
          from: { x: w + margin.left, y: 10 },
          to: { x: w + margin.left, y: height - margin.top },
          fill: "#5b5e5f",
          strokeDasharray: "2,2"
        }),
        $(AxisBottom, {
          left: margin.left,
          top: height - margin.bottom,
          scale: xScale,
          stroke: '#f0f0f0',
          numTicks: 7,
          tickStroke: '#f0f0f0',
          tickFormat: value => formatTime(value).toUpperCase(),
          tickLabelProps: value => {
            return {
              fontSize: 8,
              fill: '#999',
              fontFamily: 'helvetica',
              textAnchor: 'middle',
            }
          }
        }),
        $(AxisLeft, {
          left: margin.left,
          top: margin.top,
          scale: yScale,
          stroke: '#f0f0f0',
          tickStroke: '#f0f0f0',
          tickValues: [20, 30, 40, 50, 60, 70, 80],
          tickFormat: (value) => value === 80 ? `80%` : value,
          tickLabelProps: (value) => {
            return {
              fontSize: 13,
              fill: value === 50 ? '#111' : '#999',
              fontFamily: 'monospace',
              fontWeight: 600,
              dy: '0.32em',
              dx: '-.1em',
              textAnchor: 'end'
            }
          }
        }),
        $(Group.Group, { left: margin.left, top: margin.top }, [
          $(Grid.Grid, {
            xScale,
            yScale,
            width: w,
            height: h,
            stroke: '#f0f0f0',
            numTicks: 7
          }),
          $(Area, {
            data: TrumpTrends,
            x,
            xScale,
            yScale,
            y0: d => parseFloat(d.disapprove_lo),
            y1: d => parseFloat(d.disapprove_hi),
            stroke: 'none',
            fill: '#ff7400',
            fillOpacity: 0.15
          }),
          $(Area, {
            data: TrumpTrends,
            x,
            xScale,
            yScale,
            y0: d => parseFloat(d.approve_lo),
            y1: d => parseFloat(d.approve_hi),
            stroke: 'none',
            fill: '#009e29',
            fillOpacity: 0.15
          }),
          ...TrumpPolls.map((poll,i) => {
            return (
              $(React.Fragment, { key: `poll-${i}` }, [
                $('circle', {
                  cx: xScale(parseTime(poll.enddate)),
                  cy: yScale(poll.approve),
                  r: 3,
                  fill: '#009f29',
                  fillOpacity: 0.1
                }),
                $('circle', {
                  cx: xScale(parseTime(poll.enddate)),
                  cy: yScale(poll.disapprove),
                  r: 3,
                  fill: '#ff7400',
                  fillOpacity: 0.1
                })
              ])
            );
          }),
          $(Line, {
            from: { x: -8, y: yScale(50) },
            to: { x: w, y: yScale(50) }
          }),
          $(LinePath, {
            data: TrumpTrends,
            y: disapprove,
            x,
            xScale,
            yScale,
            strokeWidth: 3,
            stroke: '#ff7400'
          }),
          $(LinePath, {
            curve: curveLinear,
            data: TrumpTrends,
            y: approve,
            x,
            xScale,
            yScale,
            strokeWidth: 3,
            stroke: '#009e29'
          }),
          $('text', {
            fontFamily: 'helvetica',
            fontSize: 32,
            fontWeight: 700,
            fill: '#ff7400',
            dx: '.2em',
            x: xScale(x(TrumpTrends[0])),
            y: yScale(disapprove(TrumpTrends[0])),
          }, [
            $('tspan', null, formatNumber(disapprove(TrumpTrends[0]))),
            $('tspan', { fontSize: 14, dy: '-.8em' }, '%'),
            $('tspan', { fontSize: 14, dx: '.2em', fill: '#222', fontWeight: 400 }, 'Disapprove')
           ]
          ),
          $('text', {
            fontFamily: 'helvetica',
            fontSize: 32,
            fontWeight: 700,
            fill: '#009e29',
            dx: '.2em',
            x: xScale(x(TrumpTrends[0])),
            y: yScale(approve(TrumpTrends[0])),
          }, [
            $('tspan', null, formatNumber(approve(TrumpTrends[0]))),
            $('tspan', { fontSize: 14, dy: '-.8em' }, '%'),
            $('tspan', { fontSize: 14, dx: '.25em', fill: '#222', fontWeight: 400 }, 'Approve')
           ]
          )
        ]),
      ])
    );
  }
  
  ReactDOM.render(
    $(Chart),
    document.getElementById("chart")
  );
  
  // name the cell section
  return "the code";
}
);
  main.variable(observer()).define(["md"], function(md){return(
md`## Data`
)});
  main.variable(observer("polls")).define("polls", ["d3"], function(d3){return(
d3.csv("https://projects.fivethirtyeight.com/trump-approval-data/approval_polllist.csv")
)});
  main.variable(observer("trends")).define("trends", ["d3"], function(d3){return(
d3.csv("https://projects.fivethirtyeight.com/trump-approval-data/approval_topline.csv")
)});
  main.variable(observer()).define(["md"], function(md){return(
md`## Dependencies`
)});
  main.variable(observer("d3")).define("d3", ["require"], function(require){return(
require('d3')
)});
  main.variable(observer("React")).define("React", ["require"], function(require){return(
require("https://bundle.run/react")
)});
  main.variable(observer("ReactDOM")).define("ReactDOM", ["require"], function(require){return(
require("https://bundle.run/react-dom")
)});
  main.variable(observer("Scale")).define("Scale", ["require"], function(require){return(
require("https://bundle.run/@vx/scale@0.0.161")
)});
  main.variable(observer("Axis")).define("Axis", ["require"], function(require){return(
require("https://bundle.run/@vx/axis@0.0.162 ")
)});
  main.variable(observer("Group")).define("Group", ["require"], function(require){return(
require("https://bundle.run/@vx/group@0.0.161")
)});
  main.variable(observer("Curve")).define("Curve", ["require"], function(require){return(
require("https://bundle.run/@vx/curve@0.0.161")
)});
  main.variable(observer("Shape")).define("Shape", ["require"], function(require){return(
require("https://bundle.run/@vx/shape@0.0.162")
)});
  main.variable(observer("Grid")).define("Grid", ["require"], function(require){return(
require("https://bundle.run/@vx/grid@0.0.162")
)});
  return main;
}
