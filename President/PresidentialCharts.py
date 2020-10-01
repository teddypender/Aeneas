wordChart ="""
<!DOCTYPE html>
<meta charset="utf-8">
<html>
<body>
  <script src="https://d3js.org/d3.v3.min.js"></script>
  <script src="https://rawgit.com/jasondavies/d3-cloud/master/build/d3.layout.cloud.js"></script>
  <link href='https://fonts.googleapis.com/css?family=Barlow' rel='stylesheet'>
  <script>

//Simple animated example of d3-cloud - https://github.com/jasondavies/d3-cloud
//Based on https://github.com/jasondavies/d3-cloud/blob/master/examples/simple.html

// Encapsulate the word cloud functionality
function wordCloud(selector) {

    var fill = d3.scale.category20();

    //Construct the word cloud's SVG element
    var svg = d3.select(selector).append("svg")
        .attr("width", 800)
        .attr("height", 500)
        .append("g")
        .attr("transform", "translate(400,250)");


    //Draw the word cloud
    function draw(words) {
        var cloud = svg.selectAll("g text")
                        .data(words, function(d) { return d.text; })

        //Entering words
        cloud.enter()
            .append("text")
            .style("font-family", "Barlow")
            .style("background-color", "transparent") //color: rgb(222, 57, 71)
            .style("color", "rgb(222, 57, 71)") //rep = color: rgb(222, 57, 71), dem = rgb(63, 82, 185)
            .style("fill", function(d, i) { return fill(i); })
            .attr("text-anchor", "middle")
            .attr('font-size', 1)
            .text(function(d) { return d.text; });

        //Entering and existing words
        cloud
            .transition()
                .duration(800)
                .style("font-size", function(d) { return d.size + "px"; })
                .attr("transform", function(d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .style("fill-opacity", 1);

        //Exiting words - 
        cloud.exit()
            .transition()
                .duration(800)
                .style('fill-opacity', 1e-6)
                .attr('font-size', 1)
                .remove();
    }


    //Use the module pattern to encapsulate the visualisation code. We'll
    // expose only the parts that need to be public.
    return {

        //Recompute the word cloud for a new set of words. This method will
        // asycnhronously call draw when the layout has been computed.
        //The outside world will need to call this function, so make it part
        // of the wordCloud return value.
        update: function(words) {
            d3.layout.cloud().size([800, 500])
                .words(words)
                .padding(5)
                .rotate(function() { return ~~(Math.random() * 2) * 0; })
                .font("Barlow")
                .fontSize(function(d) { return d.size; })
                .on("end", draw)
                .start();
        }
    }

}
"""
wordChartData = """
//Some sample data - http://en.wikiquote.org/wiki/Opening_lines
var words = ['{0}'];
var wordMap = {1};
var maxSize = {2};
"""

wordChartBottom = """
//Prepare one of the sample sentences by removing punctuation,
// creating an array of words and computing a random size attribute.
function getWords(i) {
    var w = words[i];
    var s = 10 + wordMap[w];
    return w
            .replace(/[!\.,:;\?]/g, '')
            .split('-')
            .map(function(d, s) {
                return {text: d, size: 10 + ( s / Math.random())};
                //return {text: d, size: s};
            })
}

//This method tells the word cloud to redraw with a new set of words.
//In reality the new words would probably come from a server request,
// user input or some other source.
function showNewWords(vis, i) {
    i = i || 0;

    vis.update(getWords(i ++ % words.length))
    setTimeout(function() { showNewWords(vis, i + 1)}, 2000)
}

//Create a new instance of the word cloud visualisation.
var myWordCloud = wordCloud('body');

//Start cycling through the demo data
showNewWords(myWordCloud);


</script>
</body>
</html>
"""
