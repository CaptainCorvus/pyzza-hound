var app = angular.module('pyzzaApp', ['ngMaterial']);

var layout = {
  title: {
    text:'Temperature',
    font: {
      family: 'Courier New, monospace',
      size: 24
    },
    xref: 'paper',
    x: 0.05,
  },
  yaxis: {
    title: {
      text: 'Temperature [Degrees F]',
      font: {
        family: 'Courier New, monospace',
        size: 18,
        color: '#7f7f7f'
      }
    }
  }
};

Plotly.newPlot('temperaturePlot', [{}], layout);

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

    $scope.tempData = [];
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

    $scope.getTempData = function(device) {
        Plotly.react('temperaturePlot', [], layout);
        $scope.tempTraces = [];
        $scope.tempData   = [];
        for (i = 0; i < $scope.deviceSelected.length; i++) {
            var device = $scope.deviceSelected[i];
            timeRange = $scope.getTimeWindow($scope.timerangeSelected.value);
            var tstart = timeRange[0];
            var tstop = timeRange[1];

            // build url
            var url = baseSensorUrl + '/getTemp';
            url = url + '?tstart=' + tstart.utc().format();
            url = url + '&tstop=' + tstop.utc().format();
            url = url + '&device=' + device;

            $http.get(url).then(function(response) {

                $scope.tempData.push(response.data);

                var trace = {
                    name: response.data.name,
                    x: response.data.time,
                    y: response.data.tempf,
                    mode: 'markers',
                    type: 'scatter',
                    showlegend: true
                };

                $scope.tempTraces.push(trace);
                Plotly.addTraces('temperaturePlot', [trace]);

            }, $scope.returno);
        }
    };


}

]);