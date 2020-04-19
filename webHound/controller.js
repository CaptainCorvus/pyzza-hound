var app = angular.module('pyzzaApp', []);

Plotly.newPlot('temperaturePlot', []);
app.controller('pyzzaController', ['$scope', '$http',
function($scope, $http) {

    hostname = 'http://' + location.host;

    apis = {
        sensors: '/sensor-api'
    };

    var baseSensorUrl = hostname + apis.sensors;

    $scope.selectedDevices = [];

    $scope.device = 'pecan';
    $scope.categories = ['Temperature', 'Moisture', 'Sound', 'Light'];
    $scope.tempFields = ['Device', 'Current temp', 'Min Temp', 'Max Temp', 'Mean Temp'];
    $scope.deviceList = ['Pecan', 'Pumpkin', 'Peach'];
    $scope.deviceSelected = $scope.deviceList[0];

    $scope.tempData = null;
    $scope.tempTraces = [];
    $scope.currentTemp = null;
    $scope.sensorTypeSelected = $scope.categories[0];
    $scope.firstLoad = true;
    $scope.inputDate = {
        start: null,
        stop: null
    };
    $scope.quickTimeRanges = [
        {
            name: '24 hours',
            value: 1
        },
        {
            name: '72 hours',
            value: 3
        },
        {
            name: '1 week',
            value: 7
        },
        {
            name: '1 month',
            value: 30
        },
        {
            name: '1 year',
            value: 365
        }
    ];
    $scope.timerangeSelected = $scope.quickTimeRanges[0];


    $scope.getTimeWindow = function(value) {
        tstart = new moment().subtract(value, 'days');
        tstop  = new moment();
        return [tstart, tstop];

    };

    $scope.returno = function() {
        print("get request failed");
        return;
    };


    $scope.getTempData = function() {

        device = 'pecan'
        timeRange = $scope.getTimeWindow($scope.timerangeSelected.value);
        var tstart = timeRange[0];
        var tstop = timeRange[1];

        // build url
        url = baseSensorUrl + '/getTemp';
        url = url + '?tstart=' + tstart.format('YYYY-MM-DD HH:mm:ss');
        url = url + '&tstop=' + tstop.format('YYYY-MM-DD HH:mm:ss');
        url = url + '&device=' + $scope.deviceSelected;

        data = null;

        $http.get(url).then(function(response) {
            $scope.tempData = response.data;
            data = response.data;
            len = $scope.tempData.tempf.length;
            $scope.currentTemp = $scope.tempData.tempf[len - 1]
        }, $scope.returno);
        return data;
    };

    $scope.displayTemperature = function() {
        $scope.getTempData();
        if ($scope.tempData !== null) {
            len = $scope.tempData.tempf.length;
            // $scope.currentTemp = $scope.tempData.tempf[len - 1];
            var tempf = {
                x: $scope.tempData.time,
                y: $scope.tempData.tempf,
                mode: 'markers',
                type: 'scatter'
            };
            $scope.tempTraces = [tempf];
            Plotly.react('temperaturePlot', [tempf]);
        }
//        Plotly.relayout('temperaturePlot', []);
    };

}

]);