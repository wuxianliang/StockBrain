<template lang="pug">
  Col
    Card
      p(title='K线') {{code}}
      div#k-data
</template>

<script>
import echarts from 'echarts'

function splitData(rawData) {
    var categoryData = [];
    var values = [];
    var volumes = [];
    for (var i = 0; i < rawData.length; i++) {
        categoryData.push(rawData[i].date);
        values.push(rawData[i].value);
        volumes.push([i, rawData[i].volume, rawData[i].value[0]>rawData[i].value[1]?-1:1]);
    }
    return {
        categoryData: categoryData,
        values: values,
        volumes: volumes
    };
}

function calculateMA(dayCount, data) {
    var result = [];
    for (var i = 0, len = data.values.length; i < len; i++) {
        if (i < dayCount) {
            result.push('-');
            continue;
        }
        var sum = 0;
        for (var j = 0; j < dayCount; j++) {
            sum += data.values[i - j][1];
        }
        result.push(+(sum / dayCount).toFixed(3));
    }
    return result;
}
export default {
  name: 'kLineChart',
  props: ['kdata', 'name', 'code'],
  mounted () {
    // this.drawKLine(this.kdata, this.name)
  },
  watch: {
    kdata() {
      this.drawKLine(this.kdata, this.name)
    }
  },
  methods: {
    drawKLine(kdata, name) {
      let kLineChart = echarts.init(document.getElementById('k-data'))
      var data = splitData(kdata);

      const option = {
        title: {
  		        text: name,
  		        left: 0
  		    },
        animation: false,
        legend: {
          bottom: 10,
          left: 'center',
          data: ['日线', 'MA5', 'MA10', 'MA20', 'MA30']
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          },
          backgroundColor: 'rgba(245, 245, 245, 0.8)',
          borderWidth: 1,
          borderColor: '#ccc',
          padding: 10,
          textStyle: {
            color: '#000'
          },
          position: function (pos, params, el, elRect, size) {
            var obj = {top: 10};
            obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
            return obj;
          },
          extraCssText: 'width: 170px'
        },
        axisPointer: {
          link: {xAxisIndex: 'all'},
          label: {
            backgroundColor: '#777'
          }
        },
        toolbox: {
          feature: {
            dataZoom: {
              yAxisIndex: false
            },
            brush: {
              type: ['lineX', 'clear']
            }
          }
        },
        brush: {
          xAxisIndex: 'all',
          brushLink: 'all',
          outOfBrush: {
            colorAlpha: 0.1
          }
        },
        visualMap: {
          seriesIndex: 5,
          dimension: 2,
          pieces: [{
            value: 1,
            color: '#c23531'
          }, {
            value: -1,
            color: '#2f4554'
          }]
        },
        grid: [
          {
            left: '10%',
            right: '8%',
            height: '50%'
          },
          {
            left: '10%',
            right: '8%',
            top: '63%',
            height: '16%'
          }
        ],
        xAxis: [
          {
            type: 'category',
            data: data.dates,
            scale: true,
            boundaryGap : false,
            axisLine: {onZero: false},
            splitLine: {show: false},
            splitNumber: 20,
            min: 'dataMin',
            max: 'dataMax',
            axisPointer: {
              z: 100
            }
          },
          {
            type: 'category',
            gridIndex: 1,
            data: data.categoryData,
            scale: true,
            boundaryGap : false,
            axisLine: {onZero: false},
            axisTick: {show: false},
            splitLine: {show: false},
            axisLabel: {show: false},
            splitNumber: 20,
            min: 'dataMin',
            max: 'dataMax',
            axisPointer: {
              label: {
                formatter: function (params) {
                  var seriesValue = (params.seriesData[0] || {}).value;
                  return params.value
                    + (seriesValue != null
                      ? '\n' + echarts.format.addCommas(seriesValue)
                      : ''
                    );
                }
              }
            }
          }],
          yAxis: [
            {
              scale: true,
              splitArea: {
                show: true
              }
            },
            {
              scale: true,
              gridIndex: 1,
              splitNumber: 2,
              axisLabel: {show: false},
              axisLine: {show: false},
              axisTick: {show: false},
              splitLine: {show: false}
            }
          ],
          dataZoom: [
            {
              type: 'inside',
              xAxisIndex: [0, 1],
              start: 70,
              end: 100
            },
            {
              show: true,
              xAxisIndex: [0, 1],
              type: 'slider',
              top: '85%',
              start: 98,
              end: 100
            }
          ],
          series: [
            {
              name: '日线',
              type: 'candlestick',
              data: data.values,
              itemStyle: {
                normal: {
                  borderColor: null,
                  borderColor0: null
                }
              },
              tooltip: {
                formatter: function (param) {
                  param = param[0];
                  return [
                    'Date: ' + param.name + '<hr size=1 style="margin: 3px 0">',
                    'Open: ' + param.data[0] + '<br/>',
                    'Close: ' + param.data[1] + '<br/>',
                    'Lowest: ' + param.data[2] + '<br/>',
                    'Highest: ' + param.data[3] + '<br/>'
                  ].join('');
                }
              }
            },
            {
              name: 'MA5',
              type: 'line',
              data: calculateMA(5, data),
              smooth: true,
              lineStyle: {
                normal: {opacity: 0.5}
              }
            },
            {
              name: 'MA10',
              type: 'line',
              data: calculateMA(10, data),
              smooth: true,
              lineStyle: {
                normal: {opacity: 0.5}
              }
            },
            {
              name: 'MA20',
              type: 'line',
              data: calculateMA(20, data),
              smooth: true,
              lineStyle: {
                normal: {opacity: 0.5}
              }
            },
            {
              name: 'MA30',
              type: 'line',
              data: calculateMA(30, data),
              smooth: true,
              lineStyle: {
                normal: {opacity: 0.5}
              }
            },
            {
              name: 'Volume',
              type: 'bar',
              xAxisIndex: 1,
              yAxisIndex: 1,
              data: data.volumes
            }
          ]
        };
      kLineChart.setOption(option);
      kLineChart.on('brushSelected', (params) => {
        //this.$store.state.kLine.brush = params.batch[0].selected[0].dataIndex
        console.log(params);
        this.$store.dispatch('brushSelect', params.batch[0].selected[0].dataIndex);
      });
      kLineChart.on('click', (params)=>{
        this.$store.dispatch('pickDate', params.name);
      })
    }
  }
}



</script>

<style lang="stylus">
#k-data
  width 500px
  height 700px
</style>
