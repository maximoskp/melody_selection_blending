console.log('main called 1');

var static_dat_1 = []
var static_dat_2 = []

var dat_1 = [];
var dat_2 = [];

var hc = []

function initialise_chart(pca_1, pca_2, names_1, names_2){
    dat_1 = merge_pca_names(pca_1, names_1);
    static_dat_1 = JSON.parse(JSON.stringify(dat_1));
    console.log('dat_1: ', dat_1);
    dat_2 = merge_pca_names(pca_2, names_2);
    static_dat_2 = JSON.parse(JSON.stringify(dat_2));
    hc = Highcharts.chart('container', {
        chart: {
            type: 'scatter',
            zoomType: 'xy',
            width: 800,
            height: 800
        },
        title: {
            text: 'German and Han melodies'
        },
        subtitle: {
            text: 'Plotted according to feature values'
        },
        xAxis: {
            title: {
                enabled: true,
                text: 'PCA axis 1'
            },
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true
        },
        yAxis: {
            title: {
                text: 'PCA axis 2'
            }
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 70,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF',
            borderWidth: 1
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 5,
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100,100,100)'
                        }
                    }
                },
                states: {
                    hover: {
                        marker: {
                            enabled: false
                        }
                    }
                },
                tooltip: {
                    headerFormat: '<b>{point.key}</b><br>',
                    pointFormat: '{point.x:.3f} , {point.y:.3f} '
                }
            }
        },
        series: [{
            turboThreshold: 0,
            events: {
                click: function (event) {
                    console.log('event: ', event.point.name);
                    // console.log(
                    //     this.data + ' clicked\n' +
                    //     'Alt: ' + event.altKey + '\n' +
                    //     'Control: ' + event.ctrlKey + '\n' +
                    //     'Meta: ' + event.metaKey + '\n' +
                    //     'Shift: ' + event.shiftKey
                    // );
                }
            },
            name: 'German',
            color: 'rgba(223, 83, 83, .5)',
            data: dat_1
        }, {
            turboThreshold: 0,
            events: {
                click: function (event) {
                    console.log(
                        this.name + ' clicked\n' +
                        'Alt: ' + event.altKey + '\n' +
                        'Control: ' + event.ctrlKey + '\n' +
                        'Meta: ' + event.metaKey + '\n' +
                        'Shift: ' + event.shiftKey
                    );
                }
            },
            name: 'Han',
            color: 'rgba(119, 152, 191, .5)',
            data: dat_2
        }]
    });
}

function update_data_with_percentage(p){
    var new_dat_1 = [];
    var new_dat_2 = [];
    var tmp_dat_1 = JSON.parse(JSON.stringify(static_dat_1));
    var tmp_dat_2 = JSON.parse(JSON.stringify(static_dat_2));
    console.log('dat_1.length: ', tmp_dat_1.length);
    console.log('p*dat_1.length: ', p*tmp_dat_1.length);
    for (var i=0; i<p*tmp_dat_1.length; i++){
        new_dat_1.push( tmp_dat_1[i] );
    }
    for (var i=0; i<p*tmp_dat_2.length; i++){
        new_dat_2.push( tmp_dat_2[i] );
    }
    hc.series[0].setData(new_dat_1);
    hc.series[1].setData(new_dat_2);
}

function merge_pca_names(p, n){
    var d = [];
    for (var i=0; i<n.length; i++){
        d.push( {name: n[i], x: p[i][0], y:p[i][1]} );
    }
    return d;
}