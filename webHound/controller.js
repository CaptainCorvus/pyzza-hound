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

        }
        Plotly.newPlot('temperaturePlot', $scope.tempTraces);
    };

}

]);