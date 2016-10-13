'use strict';

angular.module('angularjsboilerplate.home', ['ngRoute'])
    .config(['$routeProvider', function($routeProvider) {
        console.log('in route provider config callback of home');
        $routeProvider.when('/home', {
            templateUrl: '/static/djangorestangularjsboilerplate/app/components/home/homeView.html',
            controller: 'homeCtrl'
        });
    }])
    .controller('homeCtrl', ['$http', '$scope',
    function($http, $scope) {
        console.log('in home controller');
        //this.checkStatus(userId);
        return;
    }]);
