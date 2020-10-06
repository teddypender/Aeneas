// https://observablehq.com/@autopaideia/covid-19-curves-u-s@2127
import define1 from "./7764a40fe6b83ca1@412.js";
import define2 from "./e93997d5089d7165@2286.js";

export default function define(runtime, observer) {
  const main = runtime.module();
  main.variable(observer()).define(["md","type","d3","us_data"], function(md,type,d3,us_data){return(
md`# COVID-19 Curves (U.S.)

Interactive U.S.-based versions of [the charts in this article](https://www.nytimes.com/interactive/2020/03/19/world/coronavirus-flatten-the-curve-countries.html). The bars represent the actual number of new ${type} reported per day, while the line is a seven-day moving average to help smooth out the day-to-day anomolies and reveal the overall trend.

Data [from The New York Times](https://github.com/nytimes/covid-19-data).

*Last updated ${d3.utcFormat('%B %e, %Y')(new Date(d3.max(us_data, d => d.date)))}*.`
)});
  main.variable(observer("viewof type")).define("viewof type", ["radio"], function(radio){return(
radio({
  title: 'Type',
  options: [
    { label: 'Cases', value: 'cases' },
    { label: 'Deaths', value: 'deaths' },
  ],
  value: 'cases',
})
)});
  main.variable(observer("type")).define("type", ["Generators", "viewof type"], (G, _) => G.input(_));
  main.variable(observer()).define(["md"], function(md){return(
md`## Total`
)});
  main.variable(observer()).define(["make_figure","us_data","width"], function(make_figure,us_data,width){return(
make_figure('United States', us_data, width)
)});
  main.variable(observer()).define(["md"], function(md){return(
md`## State/Territory`
)});
  main.variable(observer("viewof state")).define("viewof state", ["select","raw_state_data"], function(select,raw_state_data){return(
select({
  title: 'Select State/Territory',
  options: Array.from(new Set(raw_state_data.map(d => d.state))).sort(),
  value: 'New York',
})
)});
  main.variable(observer("state")).define("state", ["Generators", "viewof state"], (G, _) => G.input(_));
  main.variable(observer()).define(["make_figure","active_state_data","width"], function(make_figure,active_state_data,width){return(
make_figure(active_state_data.state, active_state_data, width)
)});
  main.variable(observer()).define(["md","active_state_counties_data","type","state"], function(md,active_state_counties_data,type,state){return(
md`### Counties

${active_state_counties_data.length && `The highest ${Math.min(active_state_counties_data.length, 6)} counties in terms of **${type}** this past week in **${state}**.` || 'No counties to display.'}`
)});
  main.variable(observer("viewof county_scale_type")).define("viewof county_scale_type", ["radio"], function(radio){return(
radio({
  title: 'Scale',
  options: [
    { label: 'Shared', value: 'shared' },
    { label: 'Independent', value: 'independent' },
  ],
  value: 'shared',
})
)});
  main.variable(observer("county_scale_type")).define("county_scale_type", ["Generators", "viewof county_scale_type"], (G, _) => G.input(_));
  main.variable(observer()).define(["active_state_counties_data","html","width","county_scale_type","d3","type","make_figure"], async function(active_state_counties_data,html,width,county_scale_type,d3,type,make_figure)
{
  if (!active_state_counties_data.length) return html``;

  const counties = active_state_counties_data.slice(0, 6);
  const figureWidth = width > 500 ? width / 2 : width;

  const domain = county_scale_type === 'shared'
    ? [0, d3.max(counties, d => d3.max(d, v => v[type]))]
    : undefined;

  return html`<div style="display: flex; flex-wrap: wrap;">${
    await Promise.all(counties.map(data => make_figure(data.county, data, figureWidth, domain)))
  }</div>`;
}
);
  main.variable(observer()).define(["md"], function(md){return(
md`## All States and Territories`
)});
  main.variable(observer("viewof state_scale_type")).define("viewof state_scale_type", ["radio"], function(radio){return(
radio({
  title: 'Scale',
  options: [
    { label: 'Shared', value: 'shared' },
    { label: 'Independent', value: 'independent' },
  ],
  value: 'independent',
})
)});
  main.variable(observer("state_scale_type")).define("state_scale_type", ["Generators", "viewof state_scale_type"], (G, _) => G.input(_));
  main.variable(observer()).define(["vl","type","state_scale_type","state_data"], function(vl,type,state_scale_type,state_data)
{
  const line = vl.markLine({ interpolate: 'monotone' })
    .encode(
      vl.x()
        .fieldT('date')
        .timeUnit('utcyearmonthdate')
        .axis({ tickCount: 'month', format: '%b.', grid: false, tickSize: 6, labelColor: '#929292' })
        .title(null),

      vl.y()
        .fieldQ('mean')
        .axis(null)
        .scale({ nice: false })
        .title(null),

      vl.color({ value: 'red' }),
    );
  
  const text = vl.markText({ align: 'right', dx: -13, dy: -4, baseline: 'top', fontSize: 9 })
    .encode(
      vl.text()
        .fieldQ('argmax.mean_ceil')
        .format(',d'),

      vl.x()
        .fieldT('argmax.date')
        .timeUnit('utcyearmonthdate')
        .title(null),

      vl.y()
        .fieldQ('argmax.mean')
        .axis(null)
        .title(null),
    )
    .transform(
      vl.calculate('ceil(datum.mean)').as('mean_ceil'),
      vl.aggregate({ op: 'argmax', field: 'mean', as: 'argmax' }),
    );
  
  const tick = text.markTick({ size: 10, xOffset: -4, align: 'right', fill: '#000' });

  return vl.layer(line.markArea({ opacity: 0.2 }), line, text, tick)
    .width(165)
    .height(100)
    .facet(vl.facet().fieldN('state').title(null))
    .columns(5)
    .transform(
      vl.window({ op: 'mean', field: type, as: 'mean' })
        .groupby('state')
        .frame([-3, 3]),
    )
    .resolve({
      axis: { x: 'independent' },
      scale: { y: state_scale_type }
    })
    .config({
      style: { cell: { stroke: 'transparent' } },
      header: { labelFontSize: 14, labelPadding: 0 },
      padding: { top: 5, right: 0, bottom: 5, left: 0 },
    })
    .data(state_data
      .filter(d => d.total)
      .map(d => d.map(v => Object.assign({ state: d.state }, v)))
      .flat())
    .render();
}
);
  main.variable(observer()).define(["md"], function(md){return(
md`## Appendix`
)});
  main.variable(observer("raw_state_data")).define("raw_state_data", ["d3"], function(d3){return(
d3.csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
)});
  main.variable(observer("raw_county_data")).define("raw_county_data", ["d3"], function(d3){return(
d3.csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
)});
  main.variable(observer("process_data")).define("process_data", ["d3","type"], function(d3,type){return(
data => {
  const output = data.map((d, i) => ({
    date: d.date,
    cases: Math.max(d.cases - (data[i - 1] ? data[i - 1].cases : 0), 0),
    deaths: Math.max(d.deaths - (data[i - 1] ? data[i - 1].deaths : 0), 0),
    total_cases: +d.cases,
    total_deaths: +d.deaths,
  }));

  // The line/area will be shifted to the right by one band, so prepend
  // a placeholder value with 0 to the left to make up for it
  const dayBefore = new Date(output[0].date);
  dayBefore.setDate(dayBefore.getDate() - 1);

  output.unshift({
    date: d3.utcFormat('%Y-%m-%d')(dayBefore),
    cases: 0,
    deaths: 0,
    total_cases: 0,
    total_deaths: 0,
  });

  Object.assign(output, data[0], {
    past_week: d3.sum(output.slice(-7), d => d[type]),
    total: output[output.length - 1][`total_${type}`],
  });

  ['date', 'cases', 'deaths'].forEach(key => delete output[key]);

  return output;
}
)});
  main.variable(observer("us_data")).define("us_data", ["process_data","d3","raw_state_data"], function(process_data,d3,raw_state_data){return(
process_data(d3.groups(raw_state_data, d => d.date)
  .map(([date, data]) => ({
    date,
    cases: d3.sum(data, d => d.cases),
    deaths: d3.sum(data, d => d.deaths),
  })))
)});
  main.variable(observer("state_data")).define("state_data", ["d3","raw_state_data","process_data"], function(d3,raw_state_data,process_data){return(
d3.groups(raw_state_data, d => d.state)
  .map(([, rows]) => process_data(rows))
)});
  main.variable(observer("active_state_data")).define("active_state_data", ["state_data","state"], function(state_data,state){return(
state_data.find(d => d.state === state)
)});
  main.variable(observer("county_data")).define("county_data", ["d3","raw_county_data","process_data"], function(d3,raw_county_data,process_data){return(
d3.groups(raw_county_data, d => d.county + d.state)
  .map(([, rows]) => process_data(rows))
)});
  main.variable(observer("active_state_counties_data")).define("active_state_counties_data", ["county_data","state","d3"], function(county_data,state,d3){return(
county_data
  .filter(d => d.state === state)
  .filter(d => d.total)
  .filter(d => d.county !== 'Unknown')
  .filter(d => d.county !== 'District of Columbia')
  // .filter(d => d.past_week > 100)
  .sort((a, b) => d3.descending(a.past_week, b.past_week))
)});
  main.variable(observer("date_extent")).define("date_extent", ["d3","raw_state_data"], function(d3,raw_state_data)
{
  const extent = d3.extent(raw_state_data, d => d.date)
    .map(d => new Date(d));
  extent[0].setDate(extent[0].getDate() - 1);
  extent[1].setDate(extent[1].getDate() + 1);

  return extent;
}
);
  main.variable(observer("make_chart")).define("make_chart", ["vl","date_extent","d3","type"], function(vl,date_extent,d3,type){return(
(data, width, domain) => {
  const bars = vl.markBar({ opacity: 0.1 })
    .encode(
      vl.x()
        .fieldT('date')
        .timeUnit('utcyearmonthdate')
        .scale({ domain: date_extent.map(d3.utcFormat('%Y-%m-%d')) })
        .axis({ tickCount: 'month', format: '%B', grid: false, tickSize: 6 })
        .title(null),

      vl.y()
        .fieldQ(type)
        .scale({ domain, nice: false })
        .axis({ tickCount: 4, domain: false, ticks: false, labelAlign: 'left', labelBaseline: 'bottom' })
        .title(null),

      vl.color({ value: 'red' }),
    );

  // Push the line/area layers to the right edge of the bars (1 bandwidth)
  const xOffset = width / d3.timeDay.count(...date_extent);

  const line = bars.markLine({ interpolate: 'monotone', xOffset })
    .encode(vl.y().fieldQ('mean'));

  const area = line.markArea({ opacity: 0.2, xOffset });

  return vl.layer(bars, area, line)
    .data(data)
    .transform(
      vl.window({ op: 'mean', field: type, as: 'mean' }).frame([-3, 3]),
    )
    .width(width)
    .height(width / 5)
    .autosize({ type: 'fit-x', contains: 'padding' })
    .config({
      style: { cell: { stroke: 'transparent' } },
      axis: { labelColor: '#929292', gridColor: '#ececec' },
      padding: { top: 5, right: 0, bottom: 5, left: 0 },
    })
    .render();
}
)});
  main.variable(observer("make_figure")).define("make_figure", ["html","type","make_chart"], function(html,type,make_chart){return(
async (title, data, width, domain) => html`<figure style="max-width: none;">
  <figcaption style="margin-bottom: 10px;">
    <h3>${title}</h3>
    <small style="color: #333;">${data.past_week.toLocaleString('en')} NEW ${type.toUpperCase()} IN PAST WEEK</small><br />
    <small>${data.total.toLocaleString('en')} TOTAL ${type.toUpperCase()}</small>
  </figcaption>
  ${await make_chart(data, width, domain)}
</figure>`
)});
  main.variable(observer("d3")).define("d3", ["require"], function(require){return(
require("d3@5", "d3-array@2")
)});
  const child1 = runtime.module(define1);
  main.import("vl", child1);
  const child2 = runtime.module(define2);
  main.import("radio", child2);
  main.import("select", child2);
  return main;
}
