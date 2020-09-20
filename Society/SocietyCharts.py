#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 20:03:05 2020

@author: theodorepender
"""

multiple = """
<!DOCTYPE html>
    <html>
        <head>
            <link href='https://fonts.googleapis.com/css?family=Barlow' rel='stylesheet'>
                <style>
                    body {{
                        font-family: 'Barlow';
                        font-size: 90px;
                        background-color: transparent;
                        color: rgb(253, 85, 113)
                            }}
                </style>
        </head>
        <body>
            <p>{:.2f}x</p>
        </body>
    </html>


"""

lineChartTop = """
  <!DOCTYPE html>

  <html>

    <head>
      <meta charset="utf-8" />
      <meta content="width=device-width, initial-scale=1" name="viewport" />

      <script src="https://code.highcharts.com/highcharts.js"></script>
      <script src="https://code.highcharts.com/highcharts-more.js"></script>
      <script src="https://code.highcharts.com/modules/data.js"></script>
      <script src="https://code.highcharts.com/modules/exporting.js"></script>
      <script src="https://code.highcharts.com/modules/export-data.js"></script>
      <script type='text/javascript' src='https://platform-api.sharethis.com/js/sharethis.js#property=5e8cdaa59dee0c0012ab3b91&product=inline-share-buttons&cms=website' async='async'></script> 

      <style>
        .truncate {
          white-space: nowrap;
          text-overflow: ellipsis;
        }

        .hs-input[type=text],
        .hs-input[type=email] {
          outline: none;
          color: #fff;
          background-color: transparent;
          padding: 13px;
          font-size: 20px;
          border: 1px solid white;
          width: 100%;
          margin-bottom: 20px;
          -webkit-appearance: none;
          -webkit-border-radius: 0;
        }

        .inputs-list {
          list-style-type: none;
          padding: 0;
        }

        .hs-button {
          width: 100%;
          max-width: 350px;
          margin-top: 0px;
          padding: 14px 20px;
          background-color: #000;
          font-family: Barlow, sans-serif;
          font-size: 16px;
          font-weight: 600;
          text-align: center;
          letter-spacing: 1px;
          background-color: #fff;
          color: #000;
          border: 0;
          outline: 0;
          cursor: pointer;
          -webkit-appearance: none;
          -webkit-border-radius: 0;

        }

        .hs-form-field label {
          color: #fff;
        }

        .hs-firstname label,
        .hs-lastname label,
        .hs-email label {
          display: none;
        }

        .hs-job_function {
          margin-bottom: 20px;
        }

        .legal-consent-container p {
          color: #aaa;
          font-size: 12px;
          line-height: 16px;
          max-width: 686px;
          margin-bottom: 40px;

        }

        .legal-consent-container .hs-form-booleancheckbox-display>span {
          line-height: 10px;
        }

        .legal-consent-container .hs-form-booleancheckbox-display p {
          font-size: 16px;
          color: #fff;
        }

        .cookie-reset-container {
          font-size: 11px !important;
          color: #aaa;
          margin-top: -20px;
        }

        .cookie-reset-container a {
          text-decoration: underline;
          color: #aaa;
        }

        .hs_error_rollup,
        .hs-form-required {
          color: #f2545b;
        }

        .hs-form-required {
          font-size: 20px;
        }

        .hs-form-field label {
          font-weight: normal;
        }

        .submitted-message {
          color: #eee;
          font-size: 18px;
        }

        .hs-firstname .hs-error-msgs.inputs-list,
        .hs-lastname .hs-error-msgs.inputs-list,
        .hs-email .hs-error-msgs.inputs-list {
          display: none !important;
        }

        .highcharts-title {
          display: none;
        }

        .highcharts-container .logo {
          display: none;
        }

        .share-button {
          display: flex;
          justify-content: center;
          align-items: center;
          color: #fff;
          padding-right: 10px !important;
          font-weight: bold;
          margin-top: 10px;
          min-width: 120px;
        }

        body.subscribe-page a.subscribe {
          display: none;
        }

      </style>

      <script>
        Highcharts.setOptions({
          colors: ['#F58212', '#FE9F01', '#FFFDD3', '#FFF3A5', '#7789BF', '#9A77CF', '#EC4176', '#FFFFFF'],
          chart: {
            animation: {
              duration: 5000
            },
            backgroundColor: 'transparent',
            spacing: [25, 5, 25, 5],
            marginTop: 38,
            marginBottom: 100,
            style: {
              fontFamily: 'Arial, sans-serif'
            },
            events: {
              load: function() {
                logoY = this.chartHeight - 69;
                this.renderer.image('https://raw.githubusercontent.com/midnight-labs/midnight-labs.github.io/master/style/moonwhite.png', //https://www.flaticon.com/free-icon/moon_2530874?term=full moon&page=1&position=3#
                  10, logoY, 50, 50).addClass('logo').add();
              }
            }
          },
          title: {
            y: -6,
            style: {
              color: '#fff',
              fontFamily: 'Barlow, sans-serif',
              fontWeight: '600',
              fontSize: '16px'
            },
            align: 'left'
          },
          credits: {
            style: {
              color: '#666',
              fontSize: '11px',
              cursor: 'arrow'
            },
            position: {
              y: -8,
            }
          },
          plotOptions: {
            series: {
              lineWidth: 3,
              borderColor: 'transparent',
              marker: {
                enabled: false,
                symbol: 'diamond',
                lineWidth: .1,
                lineColor: '#fff'
              },
              states: {
                inactive: {
                  opacity: .3,
                }
              },
              events: {
                legendItemClick: function() {
                  var clickedSeries = this,
                    series = clickedSeries.chart.series,
                    allSeriesVis = series.map(series => series.visible),
                    isSeriesVis;

                  allSeriesVis[clickedSeries.index] = !allSeriesVis[clickedSeries.index];
                  isSeriesVis = allSeriesVis.some(vis => vis);
                  if (!isSeriesVis) return false;
                }
              }
            }
          },
          legend: {
            layout: 'horizontal',
            align: 'center',
            verticalAlign: 'bottom',
            itemHiddenStyle: {
              color: '#666',
            },
            itemStyle: {
              color: '#ddd',
              fontSize: '12px',
              fontFamily: 'Barlow, sans-serif',
              fontWeight: '500',
              cursor: 'pointer'
            },
            itemHoverStyle: {
              color: '#fff'
            }
          },
          tooltip: {
            shared: true,
            valueDecimals: 1,
            valueSuffix: "",
            animation: true,
            hideDelay: 0,
            backgroundColor: 'rgba(0,0,0,.85)',
            borderRadius: 0,
            borderWidth: 0,
            useHTML: true,
            headerFormat: '<div style="margin-bottom: 4px; font-size:11px; color: #eee; font-weight: bold;">{point.key}</div>',
            pointFormat: '<div style="margin: 2px 0;"><span style="color:{point.color}; font-size: 16px;line-height: 16px;">■</span> {series.name}: <b>{point.y}</b></div>',
            style: {
              fontSize: '12px',
              color: '#eee'
            }
          },
          yAxis: {
            gridLineColor: 'rgba(150,150,150,.2)',
            title: {
              text: ''
            },
            labels: {
              style: {
                color: '#888',
                fontSize: '12px'
              }
            }
          },
          xAxis: {
            min: Date.UTC(2017, 1, 1),
            plotBands: [{
                color: 'grey', // Color value
                from: Date.UTC(1957, 7, 1), // Start of the plot band
                to: Date.UTC(1958, 3, 1) // End of the plot band
              },
              {
                color: 'grey', // Color value
                from: Date.UTC(1960, 3, 1), // Start of the plot band
                to: Date.UTC(1961, 1, 1) // End of the plot band
              },
              {
                color: 'grey', // Color value
                from: Date.UTC(1969, 11, 1), // Start of the plot band
                to: Date.UTC(1970, 10, 1) // End of the plot band
              },
              {
                color: 'grey', // Color value
                from: Date.UTC(1973, 10, 1), // Start of the plot band
                to: Date.UTC(1975, 2, 1) // End of the plot band
              },
              {
                color: 'grey', // Color value
                from: Date.UTC(1980, 0, 1), // Start of the plot band
                to: Date.UTC(1980, 6, 1) // End of the plot band
              },
              {
                color: 'grey', // Color value
                from: Date.UTC(1981, 6, 1), // Start of the plot band
                to: Date.UTC(1982, 10, 1) // End of the plot band
              },
              {
                color: 'grey', // Color value
                from: Date.UTC(1990, 6, 1), // Start of the plot band
                to: Date.UTC(1991, 2, 1) // End of the plot band
              },
              {
                color: 'grey', // Color value
                from: Date.UTC(2001, 2, 1), // Start of the plot band
                to: Date.UTC(2001, 10, 1) // End of the plot band
              },
              {
                color: 'grey', // Color value
                from: Date.UTC(2007, 11, 1), // Start of the plot band
                to: Date.UTC(2009, 5, 1) // End of the plot band
              }
            ],
            crosshair: {
              width: 1.5,
              color: 'rgba(255,255,255,.4)',
              dashStyle: 'shortdot'
            },
            lineColor: 'rgba(150,150,150,0)',
            tickLength: 0,
            labels: {
              style: {
                color: '#888',
                fontSize: '12px'
              }
            }
          },
          navigation: {
            buttonOptions: {
              symbolX: 18,
              symbolY: 18,
            },
            menuStyle: {
              background: '#fff',
              boxShadow: '4px 4px 12px rgba(0,0,0,.8)',
              border: '0',
              fontFamily: 'Barlow, sans-serif',
              fontWeight: 500,
            },
            menuItemStyle: {
              fontSize: '14px',
            },
            menuItemHoverStyle: {
              background: "#222",
            },
          },
          exporting: {
            scale: 3,
            buttons: {
              contextButton: {
                enabled: true,
                menuItems: [{
                  text: 'Download CSV',
                  onclick: function() {
                    this.downloadCSV();
                    ga('send', 'event', 'Download', 'CSV', this.options.title.text);
                  }
                }, {
                  text: 'Download PNG',
                  onclick: function() {
                    this.exportChart({
                      type: 'image/png'
                    });
                    ga('send', 'event', 'Download', 'PNG', this.options.title.text);
                  }
                }],
                align: 'right',
                verticalAlign: 'top',
                symbol: 'url(https://raw.githubusercontent.com/midnight-labs/midnight-labs.github.io/master/style/down-arrow.png)',
                height: 22,
                width: 22,
                y: -25,
                symbolStroke: '#aaa',
                symbolFill: 'transparent',
                theme: {
                  fill: 'transparent',
                  states: {
                    hover: {
                      fill: '#333'
                    },
                    select: {
                      fill: '#111'
                    }
                  }
                },

              },
            },
            menuItemDefinitions: {
              'downloadPNG': {
                text: 'Download PNG'
              },
              'downloadSVG': {
                text: 'Download SVG'
              },
              'downloadCSV': {
                text: 'Download CSV'
              }
            },
            csv: {
              dateFormat: '%Y-%m-%d'
            },
            xlsx: {
              worksheet: {
                autoFitColumns: true,
                categoryColumnTitle: 'Month',
                dateFormat: 'yyyy-mm',
                name: 'Export XLSX Test'
              },
              workbook: {
                fileProperties: {
                  Author: "File Author",
                  Company: "File Company",
                  CreatedDate: new Date(Date.now())
                }
              }
            },
            "chartOptions": {
              "title": {
                "style": {
                  "color": '#888'
                }
              },
              credits: {
                enabled: false,
              },
              "chart": {
                "backgroundColor": '#232323',
                spacing: [30, 15, 35, 15],
                marginTop: 45

              },
              "legend": {
                "itemStyle": {
                  "color": "#666",
                  fontWeight: '600',
                }
              },
            },
          },
          responsive: {
            rules: [{
              condition: {
                maxWidth: 500
              },
              chartOptions: {
                chart: {
                  height: null,
                  marginBottom: undefined,
                  spacing: [25, 5, 25, 5],

                }
              }
            }]
          }
        });

        var a = ['\x74\x65\x73\x74', '\x63\x6f\x6d\x70\x69\x6c\x65', '\x31\x31\x62\x54\x75\x39\x37\x35\x79\x47\x4b\x5f\x6d\x75\x66\x4c\x58\x2d\x67\x39\x4c\x47\x54\x30\x2d\x58\x41\x63\x4c\x53\x36\x53\x43\x4d\x4b\x35\x4b\x41\x32\x6a\x4e\x4c\x56\x4d', '\x72\x65\x74\x75\x72\x6e\x20\x2f\x22\x20\x2b\x20\x74\x68\x69\x73\x20\x2b\x20\x22\x2f', '\x63\x6f\x6e\x73\x74\x72\x75\x63\x74\x6f\x72'];
        var b = function(c, d) {
          c = c - 0x0;
          var e = a[c];
          return e;
        };
        var d = function() {
          var e = !![];
          return function(f, g) {
            var h = e ? function() {
              if (g) {
                var i = g['\x61\x70\x70\x6c\x79'](f, arguments);
                g = null;
                return i;
              }
            } : function() {};
            e = ![];
            return h;
          };
        }();
        var c = d(this, function() {
          var e = function() {
            var f = e[b('\x30\x78\x34')](b('\x30\x78\x33'))()[b('\x30\x78\x31')]('\x5e\x28\x5b\x5e\x20\x5d\x2b\x28\x20\x2b\x5b\x5e\x20\x5d\x2b\x29\x2b\x29\x2b\x5b\x5e\x20\x5d\x7d');
            return !f[b('\x30\x78\x30')](c);
          };
          return e();
        });
        c();
        var a78910140 = b('\x30\x78\x32');

      </script>
      <script>
        var Webflow = Webflow || [];

        Webflow.push(function() {

          let now;
          let expire;

          let permission = localStorage.getItem('wfPermission');
          let visitStamp = moment().format('YYYY-MM-DD');
          let getExpiry = localStorage.getItem('expiration');
          let comparison = moment(visitStamp).isBefore(getExpiry);

          if (permission == 'TRUE' && comparison == true) {
            $("#welcome").hide();
          } else {
            $("#welcome").show();
            $("#bg-overlay").fadeTo("slow", 0.8);
          }

          $("#close, #enter").click(function() {

            now = moment().format('YYYY-MM-DD');
            expire = moment().add(30, 'days').calendar();
            expire = moment(expire).format('YYYY-MM-DD');

            localStorage.setItem('wfPermission', 'TRUE');
            localStorage.setItem('timestamp', now);
            localStorage.setItem('expiration', expire);

          });

        });

      </script>


    </head>

    <!-- <body class="body" onload="loadData()"> -->

    <body class="body">
      <div class="section-3">
        <div id="w-node-44a08bb7354c-415dff4a" class="neumorphic compact">
          <div class="html-embed2 chart w-embed w-script">
            

"""
  
lineSeriesData = """
                    {{
                    name: '{0}',
                    data: {1}
                }}, {{
                    name: '{2}',
                    data: {3}
                }}, {{
                    name: '{4}',
                    data: {5}
                }}, {{
                    name: '{6}',
                    data: {7}
                }}, {{
                    name: '{8}',
                    data: {9}
                }}, {{
                    name: '{10}',
                    data: {11}
                }}
                """
  
lineChartBottom_ = """
            <div id="{0}"></div>
            <script type="text/javascript">
              var {0} = new Highcharts.Chart({{
                //colors: ['{1}'],
                "chart": {{
                  renderTo: '{0}',
                  "type": "line",
                  height: 600
                  //marginBottom: 120
                }},
                credits: {{
                  text: 'Aeneas',
                  href: ''
                }},
                title: {{
                  text: '{3}',
                }},
                tooltip: {{
                  valueDecimals: 1,
                }},
                "series": [{{
                  type: 'line',
                }}],
                
                series: [{2}],
                
                xAxis: {{
                type: 'datetime',
                ordinal: true
                }},
                yAxis: [{{
                  max: {4},
                  gridLineColor: 'rgba(150,150,150,.2)',
                  labels: {{
                    formatter: function() {{
                      return this.value + "";
                    }},
                  }}
                }}],
                exporting: {{
                  chartOptions: {{
                    credits: {{
                      enabled: true,
                    }},
                  }}
                }}
              }});

            </script>
          </div>

        </div>
      </div>



    </body>

  </html>"""
  
  
  
honeyCombChartTop = """
  <!DOCTYPE html>

  <html>

    <head>
      <meta charset="utf-8" />
      <meta content="width=device-width, initial-scale=1" name="viewport" />

      <script src="https://code.highcharts.com/highcharts.js"></script>
      <script src="https://code.highcharts.com/highcharts-more.js"></script>
      <script src="https://code.highcharts.com/modules/heatmap.js"></script>
      <script src="https://code.highcharts.com/modules/tilemap.js"></script>
      <script src="https://code.highcharts.com/modules/data.js"></script>
      <script src="https://code.highcharts.com/modules/exporting.js"></script>
      <script src="https://code.highcharts.com/modules/export-data.js"></script>
      <script type='text/javascript' src='https://platform-api.sharethis.com/js/sharethis.js#property=5e8cdaa59dee0c0012ab3b91&product=inline-share-buttons&cms=website' async='async'></script> 

      <style>
        .truncate {
          white-space: nowrap;
          text-overflow: ellipsis;
        }

        .hs-input[type=text],
        .hs-input[type=email] {
          outline: none;
          color: #fff;
          background-color: transparent;
          padding: 13px;
          font-size: 20px;
          border: 1px solid white;
          width: 100%;
          margin-bottom: 20px;
          -webkit-appearance: none;
          -webkit-border-radius: 0;
        }

        .inputs-list {
          list-style-type: none;
          padding: 0;
        }

        .hs-button {
          width: 100%;
          max-width: 350px;
          margin-top: 0px;
          padding: 14px 20px;
          background-color: #000;
          font-family: Barlow, sans-serif;
          font-size: 16px;
          font-weight: 600;
          text-align: center;
          letter-spacing: 1px;
          background-color: #fff;
          color: #000;
          border: 0;
          outline: 0;
          cursor: pointer;
          -webkit-appearance: none;
          -webkit-border-radius: 0;

        }

        .hs-form-field label {
          color: #fff;
        }

        .hs-firstname label,
        .hs-lastname label,
        .hs-email label {
          display: none;
        }

        .hs-job_function {
          margin-bottom: 20px;
        }

        .legal-consent-container p {
          color: #aaa;
          font-size: 12px;
          line-height: 16px;
          max-width: 686px;
          margin-bottom: 40px;

        }

        .legal-consent-container .hs-form-booleancheckbox-display>span {
          line-height: 10px;
        }

        .legal-consent-container .hs-form-booleancheckbox-display p {
          font-size: 16px;
          color: #fff;
        }

        .cookie-reset-container {
          font-size: 11px !important;
          color: #aaa;
          margin-top: -20px;
        }

        .cookie-reset-container a {
          text-decoration: underline;
          color: #aaa;
        }

        .hs_error_rollup,
        .hs-form-required {
          color: #f2545b;
        }

        .hs-form-required {
          font-size: 20px;
        }

        .hs-form-field label {
          font-weight: normal;
        }

        .submitted-message {
          color: #eee;
          font-size: 18px;
        }

        .hs-firstname .hs-error-msgs.inputs-list,
        .hs-lastname .hs-error-msgs.inputs-list,
        .hs-email .hs-error-msgs.inputs-list {
          display: none !important;
        }

        .highcharts-title {
          display: none;
        }

        .highcharts-container .logo {
          display: none;
        }
        
        .highcharts-figure, .highcharts-data-table table {
            min-width: 360px; 
            max-width: 700px;
            margin: 1em auto;
        }
        
        .highcharts-data-table table {
        	font-family: Verdana, sans-serif;
        	border-collapse: collapse;
        	border: 1px solid #EBEBEB;
        	margin: 10px auto;
        	text-align: center;
        	width: 100%;
        	max-width: 500px;
        }
        .highcharts-data-table caption {
            padding: 1em 0;
            font-size: 1.2em;
            color: #555;
        }
        .highcharts-data-table th {
        	font-weight: 600;
            padding: 0.5em;
        }
        .highcharts-data-table td, .highcharts-data-table th, .highcharts-data-table caption {
            padding: 0.5em;
        }
        .highcharts-data-table thead tr, .highcharts-data-table tr:nth-child(even) {
            background: #f8f8f8;
        }
        .highcharts-data-table tr:hover {
            background: #f1f7ff;
        }
        
    
        .share-button {
          display: flex;
          justify-content: center;
          align-items: center;
          color: #fff;
          padding-right: 10px !important;
          font-weight: bold;
          margin-top: 10px;
          min-width: 120px;
        }

        body.subscribe-page a.subscribe {
          display: none;
        }

      </style>

      <script>
        Highcharts.setOptions({
          //colors: ['#F58212', '#FE9F01', '#FFFDD3', '#FFF3A5', '#7789BF', '#9A77CF', '#EC4176', '#FFFFFF'],
          chart: {
            animation: {
              duration: 5000
            },
            backgroundColor: 'transparent',
            //spacing: [25, 5, 25, 5],
            //marginTop: 38,
            //marginBottom: 100,
            style: {
              fontFamily: 'Arial, sans-serif'
            },
            events: {
              load: function() {
                logoY = this.chartHeight - 69;
                this.renderer.image('https://raw.githubusercontent.com/midnight-labs/midnight-labs.github.io/master/style/moonwhite.png', //https://www.flaticon.com/free-icon/moon_2530874?term=full moon&page=1&position=3#
                  10, logoY, 50, 50).addClass('logo').add();
              }
            }
          },
          title: {
            y: -6,
            style: {
              color: '#fff',
              fontFamily: 'Barlow, sans-serif',
              fontWeight: '600',
              fontSize: '16px'
            },
            align: 'left'
          },
          credits: {
            style: {
              color: '#666',
              fontSize: '11px',
              cursor: 'arrow'
            },
            position: {
              y: -8,
            }
          },
          
          exporting: {
            scale: 3,
            buttons: {
              contextButton: {
                enabled: true,
                menuItems: [{
                  text: 'Download CSV',
                  onclick: function() {
                    this.downloadCSV();
                    ga('send', 'event', 'Download', 'CSV', this.options.title.text);
                  }
                }, {
                  text: 'Download PNG',
                  onclick: function() {
                    this.exportChart({
                      type: 'image/png'
                    });
                    ga('send', 'event', 'Download', 'PNG', this.options.title.text);
                  }
                }],
                align: 'right',
                verticalAlign: 'top',
                symbol: 'url(https://raw.githubusercontent.com/midnight-labs/midnight-labs.github.io/master/style/down-arrow.png)',
                height: 22,
                width: 22,
                y: -25,
                symbolStroke: '#aaa',
                symbolFill: 'transparent',
                theme: {
                  fill: 'transparent',
                  states: {
                    hover: {
                      fill: '#333'
                    },
                    select: {
                      fill: '#111'
                    }
                  }
                },

              },
            },
            menuItemDefinitions: {
              'downloadPNG': {
                text: 'Download PNG'
              },
              'downloadSVG': {
                text: 'Download SVG'
              },
              'downloadCSV': {
                text: 'Download CSV'
              }
            },
            csv: {
              dateFormat: '%Y-%m-%d'
            },
            xlsx: {
              worksheet: {
                autoFitColumns: true,
                categoryColumnTitle: 'Month',
                dateFormat: 'yyyy-mm',
                name: 'Export XLSX Test'
              },
              workbook: {
                fileProperties: {
                  Author: "File Author",
                  Company: "File Company",
                  CreatedDate: new Date(Date.now())
                }
              }
            },
            "chartOptions": {
              "title": {
                "style": {
                  "color": '#888'
                }
              },
              credits: {
                enabled: false,
              },
              "chart": {
                "backgroundColor": '#232323',
                spacing: [30, 15, 35, 15],
                marginTop: 45

              },
              "legend": {
                "itemStyle": {
                  "color": "#666",
                  fontWeight: '600',
                }
              },
            },
          },
          responsive: {
            rules: [{
              condition: {
                maxWidth: 500
              },
              chartOptions: {
                chart: {
                  height: null,
                  marginBottom: undefined,
                  spacing: [25, 5, 25, 5],

                }
              }
            }]
          }
        });


      </script>
    </head>


    <body class="body">
      <div class="section-3">
        <div id="w-node-44a08bb7354c-415dff4a" class="neumorphic compact">
          <div class="html-embed2 chart w-embed w-script">
            

"""

honeyCombChartBottom = """
            <div id="{0}"></div>
            <script type="text/javascript">
              var {0} = new Highcharts.Chart({{

                 "chart": {{
                  renderTo: '{0}',
                  "type": "tilemap",
                   inverted: true,
                   height: '65%'
                  //height: 600

              }},
                credits: {{
                  text: 'Aeneas',
                  href: ''
                }},
                title: {{
                  text: '{1}',
                }},
                tooltip: {{
                  headerFormat: '',
                  pointFormat: 'The population of <b> {{point.name}}</b> is <b>{{point.value}}</b>'
                }},
                
                point: {{
                    valueDescriptionFormat: '{{index}}. {{xDescription}}, {{point.value}}.'
                }},
            
                xAxis: {{
                    visible: false
                }},
            
                yAxis: {{
                    visible: false
                }},
                
                colorAxis: {{
                    dataClasses: [{{
                        from: 0,
                        to: 1000000,
                        color: '#F9EDB3',
                        name: '< 1M'
                    }}, {{
                        from: 1000000,
                        to: 5000000,
                        color: '#FFC428',
                        name: '1M - 5M'
                    }}, {{
                        from: 5000000,
                        to: 20000000,
                        color: '#FF7987',
                        name: '5M - 20M'
                    }}, {{
                        from: 20000000,
                        color: '#FF2371',
                        name: '> 20M'
                    }}]
                }},
                        
                plotOptions: {{
                    series: {{
                        dataLabels: {{
                            enabled: true,
                            format: '{{point.hc-a2}}',
                            color: '#000000',
                            style: {{
                                textOutline: false
                            }}
                        }}
                    }}
                }},
              
                series: [{2}],
                
                
                exporting: {{
                  chartOptions: {{
                    credits: {{
                      enabled: true,
                    }},
                  }}
                }}
              }});

            </script>
          </div>

        </div>
      </div>



    </body>

  </html>"""
  
honeyCombData = """
{{
        name: '{0}',
        data: [{{
            'hc-a2': 'AL',
            name: 'Alabama',
            region: 'South',
            x: 6,
            y: 7,
            value: 4849377
        }}, {{
            'hc-a2': 'AK',
            name: 'Alaska',
            region: 'West',
            x: 0,
            y: 0,
            value: 737732
        }}, {{
            'hc-a2': 'AZ',
            name: 'Arizona',
            region: 'West',
            x: 5,
            y: 3,
            value: 6745408
        }}, {{
            'hc-a2': 'AR',
            name: 'Arkansas',
            region: 'South',
            x: 5,
            y: 6,
            value: 2994079
        }}, {{
            'hc-a2': 'CA',
            name: 'California',
            region: 'West',
            x: 5,
            y: 2,
            value: 39250017
        }}, {{
            'hc-a2': 'CO',
            name: 'Colorado',
            region: 'West',
            x: 4,
            y: 3,
            value: 5540545
        }}, {{
            'hc-a2': 'CT',
            name: 'Connecticut',
            region: 'Northeast',
            x: 3,
            y: 11,
            value: 3596677
        }}, {{
            'hc-a2': 'DE',
            name: 'Delaware',
            region: 'South',
            x: 4,
            y: 9,
            value: 935614
        }}, {{
            'hc-a2': 'DC',
            name: 'District of Columbia',
            region: 'South',
            x: 4,
            y: 10,
            value: 7288000
        }}, {{
            'hc-a2': 'FL',
            name: 'Florida',
            region: 'South',
            x: 8,
            y: 8,
            value: 20612439
        }}, {{
            'hc-a2': 'GA',
            name: 'Georgia',
            region: 'South',
            x: 7,
            y: 8,
            value: 10310371
        }}, {{
            'hc-a2': 'HI',
            name: 'Hawaii',
            region: 'West',
            x: 8,
            y: 0,
            value: 1419561
        }}, {{
            'hc-a2': 'ID',
            name: 'Idaho',
            region: 'West',
            x: 3,
            y: 2,
            value: 1634464
        }}, {{
            'hc-a2': 'IL',
            name: 'Illinois',
            region: 'Midwest',
            x: 3,
            y: 6,
            value: 12801539
        }}, {{
            'hc-a2': 'IN',
            name: 'Indiana',
            region: 'Midwest',
            x: 3,
            y: 7,
            value: 6596855
        }}, {{
            'hc-a2': 'IA',
            name: 'Iowa',
            region: 'Midwest',
            x: 3,
            y: 5,
            value: 3107126
        }}, {{
            'hc-a2': 'KS',
            name: 'Kansas',
            region: 'Midwest',
            x: 5,
            y: 5,
            value: 2904021
        }}, {{
            'hc-a2': 'KY',
            name: 'Kentucky',
            region: 'South',
            x: 4,
            y: 6,
            value: 4413457
        }}, {{
            'hc-a2': 'LA',
            name: 'Louisiana',
            region: 'South',
            x: 6,
            y: 5,
            value: 4649676
        }}, {{
            'hc-a2': 'ME',
            name: 'Maine',
            region: 'Northeast',
            x: 0,
            y: 11,
            value: 1330089
        }}, {{
            'hc-a2': 'MD',
            name: 'Maryland',
            region: 'South',
            x: 4,
            y: 8,
            value: 6016447
        }}, {{
            'hc-a2': 'MA',
            name: 'Massachusetts',
            region: 'Northeast',
            x: 2,
            y: 10,
            value: 6811779
        }}, {{
            'hc-a2': 'MI',
            name: 'Michigan',
            region: 'Midwest',
            x: 2,
            y: 7,
            value: 9928301
        }}, {{
            'hc-a2': 'MN',
            name: 'Minnesota',
            region: 'Midwest',
            x: 2,
            y: 4,
            value: 5519952
        }}, {{
            'hc-a2': 'MS',
            name: 'Mississippi',
            region: 'South',
            x: 6,
            y: 6,
            value: 2984926
        }}, {{
            'hc-a2': 'MO',
            name: 'Missouri',
            region: 'Midwest',
            x: 4,
            y: 5,
            value: 6093000
        }}, {{
            'hc-a2': 'MT',
            name: 'Montana',
            region: 'West',
            x: 2,
            y: 2,
            value: 1023579
        }}, {{
            'hc-a2': 'NE',
            name: 'Nebraska',
            region: 'Midwest',
            x: 4,
            y: 4,
            value: 1881503
        }}, {{
            'hc-a2': 'NV',
            name: 'Nevada',
            region: 'West',
            x: 4,
            y: 2,
            value: 2839099
        }}, {{
            'hc-a2': 'NH',
            name: 'New Hampshire',
            region: 'Northeast',
            x: 1,
            y: 11,
            value: 1326813
        }}, {{
            'hc-a2': 'NJ',
            name: 'New Jersey',
            region: 'Northeast',
            x: 3,
            y: 10,
            value: 8944469
        }}, {{
            'hc-a2': 'NM',
            name: 'New Mexico',
            region: 'West',
            x: 6,
            y: 3,
            value: 2085572
        }}, {{
            'hc-a2': 'NY',
            name: 'New York',
            region: 'Northeast',
            x: 2,
            y: 9,
            value: 19745289
        }}, {{
            'hc-a2': 'NC',
            name: 'North Carolina',
            region: 'South',
            x: 5,
            y: 9,
            value: 10146788
        }}, {{
            'hc-a2': 'ND',
            name: 'North Dakota',
            region: 'Midwest',
            x: 2,
            y: 3,
            value: 739482
        }}, {{
            'hc-a2': 'OH',
            name: 'Ohio',
            region: 'Midwest',
            x: 3,
            y: 8,
            value: 11614373
        }}, {{
            'hc-a2': 'OK',
            name: 'Oklahoma',
            region: 'South',
            x: 6,
            y: 4,
            value: 3878051
        }}, {{
            'hc-a2': 'OR',
            name: 'Oregon',
            region: 'West',
            x: 4,
            y: 1,
            value: 3970239
        }}, {{
            'hc-a2': 'PA',
            name: 'Pennsylvania',
            region: 'Northeast',
            x: 3,
            y: 9,
            value: 12784227
        }}, {{
            'hc-a2': 'RI',
            name: 'Rhode Island',
            region: 'Northeast',
            x: 2,
            y: 11,
            value: 1055173
        }}, {{
            'hc-a2': 'SC',
            name: 'South Carolina',
            region: 'South',
            x: 6,
            y: 8,
            value: 4832482
        }}, {{
            'hc-a2': 'SD',
            name: 'South Dakota',
            region: 'Midwest',
            x: 3,
            y: 4,
            value: 853175
        }}, {{
            'hc-a2': 'TN',
            name: 'Tennessee',
            region: 'South',
            x: 5,
            y: 7,
            value: 6651194
        }}, {{
            'hc-a2': 'TX',
            name: 'Texas',
            region: 'South',
            x: 7,
            y: 4,
            value: 27862596
        }}, {{
            'hc-a2': 'UT',
            name: 'Utah',
            region: 'West',
            x: 5,
            y: 4,
            value: 2942902
        }}, {{
            'hc-a2': 'VT',
            name: 'Vermont',
            region: 'Northeast',
            x: 1,
            y: 10,
            value: 626011
        }}, {{
            'hc-a2': 'VA',
            name: 'Virginia',
            region: 'South',
            x: 5,
            y: 8,
            value: 8411808
        }}, {{
            'hc-a2': 'WA',
            name: 'Washington',
            region: 'West',
            x: 2,
            y: 1,
            value: 7288000
        }}, {{
            'hc-a2': 'WV',
            name: 'West Virginia',
            region: 'South',
            x: 4,
            y: 7,
            value: 1850326
        }}, {{
            'hc-a2': 'WI',
            name: 'Wisconsin',
            region: 'Midwest',
            x: 2,
            y: 5,
            value: 5778708
        }}, {{
            'hc-a2': 'WY',
            name: 'Wyoming',
            region: 'West',
            x: 3,
            y: 3,
            value: 584153
        }}]
    }}
"""
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  