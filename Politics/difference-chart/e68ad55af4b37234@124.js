// https://observablehq.com/@d3/difference-chart@124
export default function define(runtime, observer) {
  const main = runtime.module();
  const fileAttachments = new Map([["weather.tsv",new URL("./files/4adc98b10d124a9baedf976477b8848feecba26cc94672f2b1dc4fbc94c71c67635eb65915c37ad2e4c3d606ddd00b9dc62fde6f4515e399574907f9c0bf6431",import.meta.url)]]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));

  main.variable(observer("chart")).define("chart", ["DOM","d3","width","height","data","xAxis","yAxis","curve","x","y","colors"], function(DOM,d3,width,height,data,xAxis,yAxis,curve,x,y,colors)
{
  const aboveUid = DOM.uid("above");
  const belowUid = DOM.uid("below");

  const svg = d3.create("svg")
      .attr("viewBox", [0, 0, width, height])
      .datum(data);

  svg.append("g")
      .call(xAxis);

  svg.append("g")
      .call(yAxis);

  svg.append("clipPath")
      .attr("id", aboveUid.id)
    .append("path")
      .attr("d", d3.area()
          .curve(curve)
          .x(d => x(d.date))
          .y0(0)
          .y1(d => y(d.value1)));

  svg.append("clipPath")
      .attr("id", belowUid.id)
    .append("path")
      .attr("d", d3.area()
          .curve(curve)
          .x(d => x(d.date))
          .y0(height)
          .y1(d => y(d.value1)));

  svg.append("path")
      .attr("clip-path", aboveUid)
      .attr("fill", colors[1])
      .attr("d", d3.area()
          .curve(curve)
          .x(d => x(d.date))
          .y0(height)
          .y1(d => y(d.value0)));

  svg.append("path")
      .attr("clip-path", belowUid)
      .attr("fill", colors[0])
      .attr("d", d3.area()
          .curve(curve)
          .x(d => x(d.date))
          .y0(0)
          .y1(d => y(d.value0)));

  svg.append("path")
      .attr("fill", "none")
      .attr("stroke", "black")
      .attr("stroke-width", 1.5)
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round")
      .attr("d", d3.line()
          .curve(curve)
          .x(d => x(d.date))
          .y(d => y(d.value0)));
  
  return svg.node();
}
);
  main.variable(observer("height")).define("height", function(){return(
600
)});
  main.variable(observer("margin")).define("margin", function(){return(
{top: 20, right: 20, bottom: 30, left: 30}
)});
  main.variable(observer("x")).define("x", ["d3","data","margin","width"], function(d3,data,margin,width){return(
d3.scaleTime()
    .domain(d3.extent(data, d => d.date))
    .range([margin.left, width - margin.right])
)});
  main.variable(observer("y")).define("y", ["d3","data","height","margin"], function(d3,data,height,margin){return(
d3.scaleLinear()
    .domain([
      d3.min(data, d => Math.min(d.value0, d.value1)),
      d3.max(data, d => Math.max(d.value0, d.value1))
    ]).nice(5)
    .range([height - margin.bottom, margin.top])
)});
  main.variable(observer("xAxis")).define("xAxis", ["height","margin","d3","x","width"], function(height,margin,d3,x,width){return(
g => g
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x)
        .ticks(width / 80)
        .tickSizeOuter(0))
    .call(g => g.select(".domain").remove())
)});
  main.variable(observer("yAxis")).define("yAxis", ["margin","d3","y","data"], function(margin,d3,y,data){return(
g => g.append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y))
    .call(g => g.select(".domain").remove())
    .call(g => g.select(".tick:last-of-type text").clone()
        .attr("x", 3)
        .attr("text-anchor", "start")
        .attr("font-weight", "bold")
        .text(data.y))
)});
  main.variable(observer("colors")).define("colors", ["d3"], function(d3){return(
[d3.schemeRdYlBu[3][2], d3.schemeRdYlBu[3][0]]
)});
  main.variable(observer("curve")).define("curve", ["d3"], function(d3){return(
d3.curveStep
)});
  main.variable(observer("data")).define("data", ["d3","FileAttachment"], async function(d3,FileAttachment)
{
  const parseDate = d3.timeParse("%Y%m%d");
  const data = d3.tsvParse(await FileAttachment("weather.tsv").text(), d => ({
    date: parseDate(d.date),
    value0: +d["New York"], // The primary value.
    value1: +d["San Francisco"] // The secondary comparison value.
  }));
  data.y = "°F";
  return data;
}
);
  main.variable(observer("d3")).define("d3", ["require"], function(require){return(
require("d3@6")
)});
  return main;
}
