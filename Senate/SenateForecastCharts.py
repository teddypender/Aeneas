#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 18:45:21 2020

@author: theodorepender
"""
lastUpdated = """
<!DOCTYPE html>
    <html>
        <head>
            <link href='https://fonts.googleapis.com/css?family=Barlow' rel='stylesheet'>
                <style>
                    body {{
                        font-family: 'Barlow';
                        font-size: 40px;
                        background-color: transparent;
                        color: rgb(255, 255, 255);
                        transform: translate(0%, -100%);
                            }}
                </style>
        </head>
        <body>
            <p>Last Updated at: {0}</p>
        </body>
    </html>


"""
demWinPct = """
<!DOCTYPE html>
    <html>
        <head>
            <link href='https://fonts.googleapis.com/css?family=Barlow' rel='stylesheet'>
                <style>
                    body {{
                        font-family: 'Barlow';
                        font-size: 135px;
                        background-color: transparent;
                        color: rgb(63, 82, 185);
                        transform: translate(0%, -100%);
                            }}
                </style>
        </head>
        <body>
            <p>{:.1f}%</p>
        </body>
    </html>


"""

repWinPct = """
<!DOCTYPE html>
    <html>
        <head>
            <link href='https://fonts.googleapis.com/css?family=Barlow' rel='stylesheet'>
                <style>
                    body {{
                        font-family: 'Barlow';
                        font-size: 135px;
                        background-color: transparent;
                        color: rgb(222, 57, 71);
                        transform: translate(0%, -100%);
                            }}
                </style>
        </head>
        <body>
            <p>{:.1f}%</p>
        </body>
    </html>


"""

demMeanSeats = """
<!DOCTYPE html>
    <html>
        <head>
            <link href='https://fonts.googleapis.com/css?family=Barlow' rel='stylesheet'>
                <style>
                    body {{
                        font-family: 'Barlow';
                        font-size: 270px;
                        background-color: transparent;
                        color: rgb(63, 82, 185);
                        transform: translate(0%, -100%);
                            }}
                </style>
        </head>
        <body>
            <p>{:.1f}</p>
        </body>
    </html>


"""

repMeanSeats = """
<!DOCTYPE html>
    <html>
        <head>
            <link href='https://fonts.googleapis.com/css?family=Barlow' rel='stylesheet'>
                <style>
                    body {{
                        font-family: 'Barlow';
                        font-size: 270px;
                        background-color: transparent;
                        color: rgb(222, 57, 71);
                        transform: translate(0%, -100%);
                            }}
                </style>
        </head>
        <body>
            <p>{:.1f}</p>
        </body>
    </html>


"""


demNthSeats = """
<!DOCTYPE html>
    <html>
        <head>
            <link href='https://fonts.googleapis.com/css?family=Barlow' rel='stylesheet'>
                <style>
                    body {{
                        font-family: 'Barlow';
                        font-size: 90px;
                        background-color: transparent;
                        color: rgb(63, 82, 185);
                        transform: translate(0%, -100%);
                            }}
                </style>
        </head>
        <body>
            <p>{:.1f}</p>
        </body>
    </html>


"""

repNthSeats = """
<!DOCTYPE html>
    <html>
        <head>
            <link href='https://fonts.googleapis.com/css?family=Barlow' rel='stylesheet'>
                <style>
                    body {{
                        font-family: 'Barlow';
                        font-size: 90px;
                        background-color: transparent;
                        color: rgb(222, 57, 71);
                        transform: translate(0%, -100%);
                            }}
                </style>
        </head>
        <body>
            <p>{:.1f}</p>
        </body>
    </html>


"""

histogramChartTop = """
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
            min: 0,
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
histogramChartBottom_ = """
            <div id="{0}"></div>
            <script type="text/javascript">
              var {0} = new Highcharts.Chart({{
                colors: ['{3}'],
                
                "chart": {{
                  renderTo: '{0}',
                  "type": "column",
                  height: 600
                  //marginBottom: 120
                }},
                
                credits: {{
                  text: 'Aeneas',
                  href: ''
                }},
                
                title: {{
                      text: 'Histogram using a column chart'
                    }},
                    subtitle: {{
                      text: ''
                    }},
                    xAxis: {{
                      categories: {1},
                      crosshair: true,
                      title: {{
                        text: 'Number of Seats'
                      }}
                    }},
                    yAxis: {{
                      gridLineWidth: 0,
                      min: 0,
                      title: {{
                        text: 'Probability (%)'
                      }}
                    }},
                    tooltip: {{
                      headerFormat: '<span style="font-size:18px">{{point.key}} Seats</span><table>',
                      pointFormat: '<tr><td style="color:{{series.color}};padding:0">{{series.name}}: </td>' +
                        '<td style="padding:0"><b>{{point.y:.1f}}%</b></td></tr>',
                      footerFormat: '</table>',
                      shared: true,
                      useHTML: true
                    }},
                    plotOptions: {{
                      column: {{
                        pointPadding: 0,
                        borderWidth: 0,
                        groupPadding: 0,
                        shadow: false
                      }}
                    }},
                    series: [{{
                      name: 'Probability',
                      data: {2} 
                  
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
          colors: ['#3F52B9', '#DE3947', '#FFFDD3', '#FFF3A5', '#7789BF', '#9A77CF', '#EC4176', '#FFFFFF'],
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
            min: Date.UTC(2020, 7, 24),
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
                min: {5},
                type: 'datetime',
                ordinal: true
                }},
                yAxis: [{{
                  max: {4},
                  min: 0,
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
  
  
heatMapTableTop = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="robots" content="all" />
    <!-- <title>jQuery Tutorial Demo - Creating a data heat map</title> -->
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>


    <script type="text/JavaScript">
      $(document).ready(function(){
	// Function to get the Max value in Array
    Array.max = function( array ){
        return Math.max.apply( Math, array );
    };

    // get all values
    var counts= $('#heat-map-3 tbody td').not('.stats-title').map(function() {
        return parseInt($(this).text());
    }).get();
	
	// return max value
	var max = Array.max(counts);
	
	xr = 87;
    xg = 104;
    xb = 172;
    
    zr = 255;
    zg = 255;
    zb = 255;
   
    yr = 250;
    yg = 90;
    yb = 80;
    
    wr = 242;
    wg = 188;
    wb = 22;

    n = 50;
	
	// add classes to cells based on nearest 10 value
	/*
	$('#heat-map-3 tbody td').not('.stats-title').each(function(){
		var val = parseInt($(this).text());
		var pos = parseInt((Math.round((val/max)*100)).toFixed(0));
		if (val < 50) {
    		red = parseInt((xr + (( pos * (zr - xr)) / (n-1))).toFixed(0));
    		green = parseInt((xg + (( pos * (zg - xg)) / (n-1))).toFixed(0));
    		blue = parseInt((xb + (( pos * (zb - xb)) / (n-1))).toFixed(0));
    		clr = 'rgb('+red+','+green+','+blue+')'
    		}
    	else {
        	red = parseInt((zr + (( (pos - 50) * (yr - zr)) / (n-1))).toFixed(0));
    		green = parseInt((zg + (( (pos - 50) * (yg - zg)) / (n-1))).toFixed(0));
    		blue = parseInt((zb + (( (pos - 50) * (yb - zb)) / (n-1))).toFixed(0));
    		clr = 'rgb('+red+','+green+','+blue+')'
    	};
		$(this).css({backgroundColor:clr});
	});
	*/
	$('#heat-map-3 tbody td').not('.stats-title').each(function(){
		var val = parseInt($(this).text());
		var pos = parseInt((Math.round((val/max)*100)).toFixed(0));
    		red = parseInt((zr + (( pos * (wr - zr)) / (n-1))).toFixed(0));
    		green = parseInt((zg + (( pos * (wg - zg)) / (n-1))).toFixed(0));
    		blue = parseInt((zb + (( pos * (wb - zb)) / (n-1))).toFixed(0));
    		clr = 'rgb('+red+','+green+','+blue+')'
		$(this).css({backgroundColor:clr});
	});
});
</script>
    
    <link href='https://fonts.googleapis.com/css?family=Barlow' rel='stylesheet'>

    <style type="text/css">
      blockquote,
      img,
      label,
      h1,
      h2,
      h3,
      h4,
      h5,
      h6,
      pre,
      ul,
      ol,
      li,
      dl,
      dt,
      dd,
      form,
      fieldset,
      input,
      th,
      td {
        border:  none; //1px solid rgba(150,150,150,.2); //0;
        outline: none;
        margin: 0;
        padding: 0;
      }

      body {
        height: 100%;
        //background: #1B1A1C;
        background-color: transparent;
        color: #1f1f1f;
        font-family: 'Barlow';
        font-size: 16px;
        padding: 7px 0;
      }
      
      table {
      background-color: rgba(150,150,150,0.2);
      }

      ul,
      ol {
        list-style: none;
      }

      a {
        text-decoration: none;
      }

      .text-center {
        text-align: center;
        padding: 10px 0;
      }

      h2 {
        margin-bottom: 30px;
      }

      .wrap {
        width: 800px;
        margin: 0 auto;
      }

      .clear {
        clear: both;
      }

      /* Tutorial CSS */
      .heat-map {
        border: none; //1px solid rgba(150,150,150,.2);
        margin: 0 auto 20px auto;
        width: 800px;
      }

      .heat-map tr th {
        font-weight: 900;
        padding: 5px 7px;
        border-right: none; //1px solid rgba(150,150,150,.2);
        border-bottom: none; //1px solid rgba(150,150,150,.2);
        border-top: none; //1px solid rgba(150,150,150,.2);
        border-left: none; //1px solid rgba(150,150,150,.2);
        text-shadow: none; //0 1px 0 rgba(150,150,150,.2);
        font: bold 13px 'Barlow';
        text-transform: capitalize;
        color: #fff;
        background-color: rgba(150,150,150,.2); //#757477;
        background-image: -moz-linear-gradient(center top, #F9F9F9, #ECECEC);
      }

      .heat-map tr th.last {
        border-right: none;
      }

      .heat-map tr th.first,
      .heat-map tr td.stats-title {
        border-left: none;
        text-align: center;
        font-size: 16px;
      }

      .heat-map tr td {
        padding: 5px 7px;
        /*border-top: 1px solid #fff; border-right: 1px solid #fff; */
        border-right: none; //1px solid rgba(150,150,150,.2);
        border-bottom: none; //1px solid rgba(150,150,150,.2);
        text-align : center;
        color: #000;
        font-size: 13px;
      }

      tr.stats-row {
        text-align: right;
      }

      .heat-map tr.stats-row td.stats-title {
        //text-align: center;
        color: #000;
        font-size: 28px;
        text-shadow: none; //0 1px 0 #fff;
        background: rgba(150,150,150,.2); //#757477;
        border-top: none; //1px solid rgba(150,150,150,.2);
        border-bottom: none; //1px solid rgba(150,150,150,.2);
        border-right: none; //1px solid rgba(150,150,150,.2);
      }

      .heat-map tr.stats-row td.stats-title.last {
        border-bottom: 1px solid rgba(150,150,150,.2);
      }

    </style>
  </head>

  <body>
    <div style="width:100%; height:100%; align-self: center; margin:0 auto;">
      <!--<h2 class="text-center">jQuery Demo: Create A Data Heat Map</h2>-->
     """
heatMapTableBottom = """
      {0}

      <p class="clear text-center"><a></a></p>
    </div>
  </body>

</html>
"""
  
