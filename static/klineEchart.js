//input trades is an array, the return array has structure of [[[trade1.enter_date,trade1.enter_price],[trade1.exit_date,trade1.exit_price]],[[trade2...],[]],etc...]
function calculateMA(dayCount,closes) {
    var result = [];
    for (var i = 0, len = closes.length; i < len; i++) {
        if (i < dayCount-1) {
            result.push('-');
            continue;
        }
		
		var sum = 0;
		for (var j = 0; j < dayCount; j++) {
			sum += closes[i - j];
			}
		result.push((sum/dayCount).toFixed(2));
	}		
    return result;
}


function klineChart(kdata,divId,enterTrades,exitTrades){
	// 基于准备好的dom，初始化echarts实例
	var myChart = echarts.init(document.getElementById(divId));
	var dates=[]
	var values=[]
	var volumes=[]
	var closes=[]
	for (var i = 0, len = kdata.length; i < len; i++){
		var date=kdata[i][0];
		var vol=kdata[i][5];
		var val=[kdata[i][1],kdata[i][2],kdata[i][4],kdata[i][3]];
		var cls=kdata[i][2];
		dates.push(date);
		values.push(val);
		volumes.push(vol);
		closes.push(cls);
	}
	
	option = {
		title: {
			text: 'K线图',
			left: 0
		},
		tooltip: {
			trigger: 'axis',
			axisPointer: {
				type: 'line'
			}
		},
		legend: {
			data: ['K-Line','MA5','MA20','MA60','买入点','卖出点']
		},
		grid: [
		{
			left: '10%',
			right: '10%',
			top: '5%',
			height: '60%'
		},
		{
			left: '10%',
			right: '10%',
			top: '70%',
			height: '20%'
        }
		],
		xAxis: [
		{
			type: 'category',
			data: dates,
			scale: true,
			boundaryGap : false,
			axisLine: {onZero: false},
			splitLine: {show: false},
			splitNumber: 20,
			min: 'dataMin',
			max: 'dataMax'
		},
		{
			type: 'category',
			gridIndex: 1,
			data: dates,
			scale: true,
			boundaryGap : false,
			axisLine: {onZero: false},
			axisTick: {show: false},
			splitLine: {show: false},
			axisLabel: {show: false},
			splitNumber: 20,
			min: 'dataMin',
			max: 'dataMax'
		}
		],
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
				xAxisIndex:[0,1],
				start: 50,
				end: 100
			},
			{
				show: true,
				xAxisIndex:[0,1],
				type: 'slider',
				y: '90%',
				start: 50,
				end: 100
			}
		],
		series: [
			{
				name: 'K-Line',
				type: 'candlestick',
				data: values,
				markPoint: {
					label: {
						normal: {
							formatter: function (param) {
								return param != null ? Math.round(param.value) : '';
							}
						}
					},
					tooltip: {
						formatter: function (param) {
							return param.name + '<br>' + (param.data.coord || '');
						}
					}
				}
			},
			{
				name: 'MA5',
				type: 'line',
				data: calculateMA(5,closes),
				smooth: true,
				lineStyle: {
					normal: {opacity: 0.7}
				}
			},
	  
			{
				name: 'MA20',
				type: 'line',
				data: calculateMA(20,closes),
				smooth: true,
				lineStyle: {
					normal: {opacity: 0.5}
				}
			},
			
			{
				name: 'MA60',
				type: 'line',
				data: calculateMA(60,closes),
				smooth: true,
				lineStyle: {
					normal: {opacity: 0.3}
				}
			},
			{
                name: '成交量',
                type: 'bar',
                xAxisIndex: 1,
                yAxisIndex: 1,
                data: volumes
            },
			{
				name: '买入点',
				type: 'scatter',
				data: enterTrades,
				symbol: 'diamond',
				symbolSize: 10,
				itemStyle: {
					normal: {
					shadowBlur: 10,
					shadowColor: 'rgba(120, 36, 50, 0.5)',
					shadowOffsetY: 5,
					color: 'rgb(2, 200, 100)'
					}
				}
				
			},
			{
				name: '卖出点',
				type: 'scatter',
				data: exitTrades,
				symbol: 'triangle',
				symbolSize: 10,
				itemStyle: {
					normal: {
						shadowBlur: 10,
						shadowColor: 'rgba(25, 100, 150, 0.5)',
						shadowOffsetY: 5,
						color: 'rgb(2, 2, 200)'
					}
				}
			}
		]
	};
	// 使用刚指定的配置项和数据显示图表。
	myChart.setOption(option);
	 }