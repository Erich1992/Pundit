'use strict';

function dataFactory($http) {
    var dataFactory = {};
    // users
    dataFactory.readUser = function (userIdno) {
        console.log('userIdno: ', userIdno);
        return $http.get('/api/users/' + userIdno + '/');
    };
    dataFactory.updateUser = function (userIdno, at, first_name, last_name) {
        console.log('at: ', at, 'first_name: ', first_name, 'last_name: ', last_name);
        var req = {
            method: 'PATCH',
            url: '/api/users/' + userIdno + '/',
            headers: {'Authorization': 'Django ' + at},
            data: angular.toJson({ first_name: first_name, last_name: last_name })
        };
        return $http(req);
        /*return $http.patch('/api/users/' + userIdno + '/', {
            headers: {'Authorization': 'Django ' + at},
            data: { first_name: first_name, last_name: last_name }
        }).then(function(res){
            console.log('res: ', res);
        });*/
    };
    return dataFactory;
}

function profileCtrl($scope, dataFactory) {
    $scope.buttonDisabled = false;
    $scope.loading = false;

    $scope.user = {};

    function  readUser(userId) {
        $scope.buttonDisabled = true;
        $scope.loading = true;
        dataFactory.readUser(userId).then(function(res){
            $scope.user = res.data;
            $scope.buttonDisabled = false;
            $scope.loading = false;
        });
    };
    
    this.updateUser = function () {
        console.log('in updateUser');
        $scope.buttonDisabled = true;
        $scope.loading = true;
        dataFactory.updateUser($scope.$parent.currentUser.userIdno, $scope.$parent.currentUser.at, $scope.user.first_name, $scope.user.last_name).then(function(res){
            $scope.user = res.data;
            $scope.buttonDisabled = false;
            $scope.loading = false;
        });
    }
    readUser($scope.$parent.currentUser.userIdno);
}

angular.module('angularjsboilerplate.profile', ['ngRoute'])
    .config(['$routeProvider', function($routeProvider) {
        console.log('in route provider config callback of profile');
        $routeProvider.when('/profile', {
            templateUrl: '/static/djangorestangularjsboilerplate/app/components/profile/profileView.html',
            controller: 'profileCtrl'
        });
    }])
    .factory('dataFactory', ['$http', dataFactory])
    .controller('profileCtrl', profileCtrl);
