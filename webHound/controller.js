var app = angular.module('pyzzaApp', ['ngMaterial']);

Plotly.newPlot('temperaturePlot', [{}]);

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
    $scope.deviceList = ['Peach', 'Pumpkin', 'Pecan'];
    $scope.deviceSelected = [$scope.deviceList[0]];

    $scope.tempData = null;
    $scope.tempTraces = [];
    $scope.currentTemp = null;
    $scope.sensorTypeSelected = $scope.categories[0];
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

    $scope.checkboxToggle = function(item, list) {
        var idx = list.indexOf(item);

        if (idx > -1) {
            list.splice(idx, 1);
        }
        else {
            list.push(item);
        }
    };

    $scope.exists = function(item, list) {
        return list.indexOf(item) > -1;
    };

    $scope.getTimeWindow = function(value) {
        tstart = new moment().subtract(value, 'days');
        tstop  = new moment();
        return [tstart, tstop];

    };

    $scope.returno = function() {
        print("get request failed");
        return;
    };

    $scope.plotSelected = function() {
        for (i = 0; i < $scope.deviceSelected.length; i++) {
            $scope.getTempData($scope.deviceSelected[i]);
        }
    };

    $scope.getTempData = function(device) {

        timeRange = $scope.getTimeWindow($scope.timerangeSelected.value);
        var tstart = timeRange[0];
        var tstop = timeRange[1];

        // build url
        var url = baseSensorUrl + '/getTemp';
        url = url + '?tstart=' + tstart.utc().format();
        url = url + '&tstop=' + tstop.utc().format();
        url = url + '&device=' + device;

        var data = null;

        $http.get(url).then(function(response) {
            $scope.tempData = response.data;
            data = response.data;
            len = $scope.tempData.tempf.length;
            $scope.currentTemp = $scope.tempData.tempf[len - 1];
            $scope.displayTemperature(response.data);
        }, $scope.returno);
//      $scope.displayTemperature(data)
    };

    $scope.displayTemperature = function(data) {
//        $scope.getTempData();

        if (data !== null) {
//            len = data.tempf.length;
            // $scope.currentTemp = $scope.tempData.tempf[len - 1];
            var tempf = {
                name: data.name,
                x: data.time,
                y: data.tempf,
                mode: 'markers',
                type: 'scatter'
            };
//            $scope.tempTraces = [tempf];
//            Plotly.newPlot('temperaturePlot', [tempf]);
        }
        Plotly.react('temperaturePlot', [tempf]);
    };

}

]);