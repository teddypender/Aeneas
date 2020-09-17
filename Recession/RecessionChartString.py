#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 19:23:05 2020

@author: theodorepender
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
              duration: 1000
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
            valueSuffix: "%",
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
            min: Date.UTC(2000, 7, 1),
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

      <!-- <script>
        function loadData() {
          var url = "https://docs.google.com/spreadsheets/d/1Kgn_QkPE58ZetRG_1g0MDpuKdxfpf-WI-8UDxuP4BYw/edit#gid=818089148";
          xmlhttp = new XMLHttpRequest();
          xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
              document.getElementById("Date").innerHTML = xmlhttp.responseText;
            }
          };
          xmlhttp.open("GET", url, true);
          xmlhttp.send(null);
        }

      </script>
      -->
    </head>

    <!-- <body class="body" onload="loadData()"> -->

    <body class="body">
      <div class="section-3">
        <div id="w-node-44a08bb7354c-415dff4a" class="neumorphic compact">
          <div class="html-embed2 chart w-embed w-script">
            

"""

lineChartBottom = """
            <div id="{0}"></div>
            <script type="text/javascript">
              var {0} = new Highcharts.Chart({{
                colors: ['{1}'],
                "chart": {{
                  renderTo: '{0}',
                  "type": "line",
                  height: 600
                  //marginBottom: 120
                }},
                data: {{
                  googleSpreadsheetKey: '{2}',
                  googleSpreadsheetWorksheet: {3}
                }},
                credits: {{
                  text: 'Aeneas',
                  href: ''
                }},
                title: {{
                  text: '{4}',
                }},
                tooltip: {{
                  valueDecimals: 1,
                }},
                "series": [{{
                  type: 'line',
                }}],
                yAxis: [{{
                  max: {5},
                  gridLineColor: 'rgba(150,150,150,.2)',
                  labels: {{
                    formatter: function() {{
                      return this.value + "%";
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
  
lineChartBottom_ = """
            <div id="{0}"></div>
            <script type="text/javascript">
              var {0} = new Highcharts.Chart({{
                colors: ['{1}'],
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
                  text: '{4}',
                }},
                tooltip: {{
                  valueDecimals: 1,
                }},
                "series": [{{
                  type: 'line',
                }}],
                series: [{{
                    name: '{2}',
                    data: {3}
                }}],
                xAxis: {{
                type: 'datetime',
                ordinal: true
                }},
                yAxis: [{{
                  max: {5},
                  gridLineColor: 'rgba(150,150,150,.2)',
                  labels: {{
                    formatter: function() {{
                      return this.value + "%";
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