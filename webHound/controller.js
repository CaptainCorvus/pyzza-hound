var app = angular.module('pyzzaApp', []);

Plotly.newPlot('temperaturePlot', []);
app.controller('pyzzaController', ['$scope', '$http',
function($scope, $http) {

    hostname = 'http://' + location.host;

    apis = {
        sensors: '/sensor-api'
    };

    var baseSensorUrl = hostname + apis.sensors;

    $scope.device = 'pecan';
    $scope.categories = ['Temperature', 'Moisture', 'Sound', 'Light'];
    $scope.tempData = null;
    $scope.tempTraces = [];
    $scope.currentTemp = null;
    $scope.sensorTypeSelected = $scope.categories[0];
    $scope.firstLoad = true;
    $scope.quickTimeRanges = [
        {
            name: '24 hours',
            value: new moment().subtract(24, 'hours')
        },
        {
            name: '72 hours',
            value: new moment().subtract(72, 'hours')
        },
        {
            name: '1 week',
            value: new moment().subtract(1, 'weeks')
        },
        {
            name: '1 month',
            value: new moment().subtract(1, 'months')
        },
        {
            name: '1 year',
            value: new moment().subtract(1, 'years')
        }
    ];
    $scope.timerangeSelected = $scope.quickTimeRanges[0];
    $scope.tstart = $scope.timerangeSelected.value;
    $scope.tstop = new moment();


    $scope.returno = function() {
        print("get request failed");
        return;
    };

    $scope.getNow = function() {
        var time = new moment();
        return time;
    };

    $scope.getInitialTimeWindow = function() {
        start = new moment().subtract(24, 'hours')
        stop  = new moment()
        $scope.tstart = start;
        $scope.tstop = stop;

    };

    $scope.getTempData = function() {

        device = 'pecan'
        $scope.tstart = $scope.timerangeSelected.value;
        // build url
        url = baseSensorUrl + '/getTemp';
        url = url + '?tstart=' + $scope.tstart.format('YYYY-MM-DD HH:mm:ss');
        url = url + '&tstop=' + $scope.tstop.format('YYYY-MM-DD HH:mm:ss');
        url = url + '&device=' + device;
        $http.get(url).then(function(response) {
            response.data;
            $scope.tempData = response.data;
        }, $scope.returno);
    };

    $scope.displayTemperature = function() {
        $scope.getTempData();
        if ($scope.tempData !== null) {
            len = $scope.tempData.tempf.length;
            $scope.currentTemp = $scope.tempData.tempf[len - 1];
            var tempf = {
                x: $scope.tempData.time,
                y: $scope.tempData.tempf,
                mode: 'markers',
                type: 'scatter'
            };
            $scope.tempTraces = [tempf];

        }
//        else {
//            var trace1 = {
//                x: [1, 2, 3, 4],
//                y: [10, 15, 13, 17],
//                mode: 'markers',
//                type: 'scatter'
//            };
//
//            var trace2 = {
//              x: [2, 3, 4, 5],
//              y: [16, 5, 11, 9],
//              mode: 'lines',
//              type: 'scatter'
//            };
//            $scope.tempTraces = [trace1, trace2];

//        }
        Plotly.newPlot('temperaturePlot', $scope.tempTraces);
    }

    // initial page load, get the temperature data and display it
//    $scope.getTempData();
//    $scope.displayTemperature();
}

]);