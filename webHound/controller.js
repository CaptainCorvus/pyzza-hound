var app = angular.module('pyzzaApp', []);

app.controller('pyzzaController', ['$scope', '$http',
function($scope, $http) {

    hostname = 'http://' + location.host;

    apis = {
        sensors: '/sensor-api'
    };

    var baseSensorUrl = hostname + apis.sensors;

    $scope.tstart = null;
    $scope.tstop = null;
    $scope.device = 'Pecan';
    $scope.categories = ['Temperature', 'Moisture', 'Sound', 'Light'];
    $scope.tempData = null;
    $scope.tempTraces = [];
    $scope.currentTemp = null;

    $scope.returno = function() {
        return;
    };

    $scope.getNow = function() {
        var time = new moment().format('YYYY-MM-DD HH:mm:ss');
        //var formatted = time.getFullYear() + '-' + time.getMonth() + '-' + time.getDay();
        //formatted = formatted + ' ' + time.getHours() + ':' + time.getMinutes() + ':' + time.getSeconds();
        return time;
    };

    $scope.getTempData = function() {
        // TODO get user input tstart/tstop/device
        tstart = '2019-05-01 00:00:00';
        tstop = $scope.getNow();
        device = 'Pecan'

        // build url
        url = baseSensorUrl + '/getTemp';
        url = url + '?tstart=' + tstart;
        url = url + '&tstop=' + tstop;
        url = url + '&device=' + device;
        $http.get(url).then(function(response) {
            $scope.tempData = response.data;
        }, $scope.returno);
    };

    $scope.displayTemperature = function() {
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
        else {
            var trace1 = {
                x: [1, 2, 3, 4],
                y: [10, 15, 13, 17],
                mode: 'markers',
                type: 'scatter'
            };

            var trace2 = {
              x: [2, 3, 4, 5],
              y: [16, 5, 11, 9],
              mode: 'lines',
              type: 'scatter'
            };
            $scope.tempTraces = [trace1, trace2];

        }
        Plotly.newPlot('temperaturePlot', $scope.tempTraces);
    }

}

]);