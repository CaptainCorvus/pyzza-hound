var app = angular.module('pyzzaApp', []);

app.controller('pyzzaController', ['$scope', '$http',
function($scope) {

    $scope.tstart = null;
    $scope.tstop = null;
    $scope.device = 'Pecan';
    $scope.categories = ['Temperature', 'Moisture', 'Sound', 'Light'];
}

]);