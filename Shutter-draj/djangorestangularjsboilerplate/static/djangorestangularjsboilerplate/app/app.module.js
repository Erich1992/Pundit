// https://scotch.io/tutorials/angularjs-best-practices-directory-structure
// https://github.com/toddmotto/angularjs-styleguide

// from http://joelsaupe.com/programming/angularjs-post-data-dictionary-http/
function httpAcceptJson($httpProvider){
	// Use x-www-form-urlencoded Content-Type
	$httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
	// Override $http service's default transformRequest
	$httpProvider.defaults.transformRequest = [function(data){
		/**
		 * The workhorse; converts an object to x-www-form-urlencoded serialization.
		 * @param {Object} obj
		 * @return {String}
		 */
		var param = function(obj){
			var query = '';
			var name, value, fullSubName, subName, subValue, innerObj, i;

			for(name in obj) {
				value = obj[name];
				if(value instanceof Array){
					for(i=0; i<value.length; ++i){
						subValue = value[i];
						fullSubName = name + '[' + i + ']';
						innerObj = {};
						innerObj[fullSubName] = subValue;
						query += param(innerObj) + '&';
					}
				}
				else if(value instanceof Object){
					for(subName in value){
						subValue = value[subName];
						fullSubName = name + '[' + subName + ']';
						innerObj = {};
						innerObj[fullSubName] = subValue;
						query += param(innerObj) + '&';
					}
				}
				else if(value !== undefined && value !== null){
					query += encodeURIComponent(name) + '=' + encodeURIComponent(value) + '&';
				}
			}
			return query.length ? query.substr(0, query.length - 1) : query;
		};
		return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
	}];
}

function appConfig($interpolateProvider, $httpProvider, $locationProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$locationProvider.html5Mode(true);
	$locationProvider.hashPrefix('!');
}

function appController($scope,$http, USER_ROLES, authService) {

	vm = this;
	vm.activateAccount = activateAccount;

	init();

    $scope.forgotPassword = function()
    {
        window.location = CONFIG.URLS.forgotPassword;
    }


	$scope.setCurrentUser = function (user) {
		console.log('in setCurrentUser, user is: ', user);
		$scope.currentUser = user;
		localStorage.setItem('userId', user.userId);
		localStorage.setItem('userIdno', user.userIdno);
		localStorage.setItem('role', user.role);
		localStorage.setItem('at', user.at);
		localStorage.setItem('rt', user.rt);
	};

	$scope.clearCurrentUser = function() {
		$scope.currentUser = null;
		localStorage.removeItem('userId');
		localStorage.removeItem('userIdno');
		localStorage.removeItem('role');
		localStorage.removeItem('at');
		localStorage.removeItem('rt');
	}


	function init(){
		if (localStorage.getItem("userId") && localStorage.getItem("role")) {
			checkStatus(localStorage.getItem("userIdno"));
			$scope.currentUser = {
				'userId': localStorage.getItem("userId"),
				'userIdno': localStorage.getItem("userIdno"),
				'role': localStorage.getItem("role"),
				'at': localStorage.getItem("at"),
				'rt': localStorage.getItem("rt")
			};
		} else{
			$scope.currentUser = null;
			$scope.userRoles = USER_ROLES;
			$scope.isAuthorized = authService.isAuthorized;
			$scope.loginFailed = false;
			$scope.signupFailed = false;
			$scope.signupSuccess = false;
		}
	}

	function checkStatus(userId) {
		return $http.get('/api/user-status/'+ userId+'/').then(function(res){
			$scope.userStatus = res.data.is_active;
			console.log($scope.userStatus);
		}, function(err){
			console.log(err);
		});
	}

   function activateAccount(){
		return $http.post('/djoser-auth/activate/',{
			'uid': $scope.currentUser.userIdno,
			'token': $scope.currentUser.at
		}).then(function(res){
			console.log(res);
		}, function(err){
			console.log(err);
		});
   }


}

// signup

function signupController ($scope, $rootScope, AUTH_EVENTS, authService){
	$scope.credentials = {
		username: '',
		password: ''
	};
	$scope.loading = false;
	$scope.buttonDisabled = false;

	$scope.signup = function (credentials) {
		$scope.loading = true;
		$scope.buttonDisabled = true;
		$scope.loginFailed = false;
		authService.signup(credentials).then(function (user) {
			$scope.signupFailed = false;
			$scope.signupSuccess = true;
			$scope.loading = false;
			$scope.buttonDisabled = false;
			$rootScope.$broadcast(AUTH_EVENTS.signupSuccess);
		}, function () {
			$scope.signupFailed = true;
			$scope.signupSuccess = false;
			$scope.loading = false;
			$scope.buttonDisabled = false;
			$rootScope.$broadcast(AUTH_EVENTS.signupFailed);
		});
	};
}

function signupFailureService(AUTH_EVENTS, $scope) {
	this.listen = function(callback) {
		$rootScope.$on(AUTH_EVENTS.signupFailed, function(){
			$scope.signupFailed = true;
		})
	}
}

// login

function loginController ($location, $scope, $rootScope, AUTH_EVENTS, authService) {
	$scope.credentials = {
		username: '',
		password: ''
	};
	$scope.buttonDisabled = false;

	$scope.login = function (credentials) {
		$scope.loading = true;
		$scope.buttonDisabled = true;

		authService.login(credentials).then(function (user) {
			if (user) {
				$rootScope.$broadcast(AUTH_EVENTS.loginSuccess);
				$scope.loading = false;
				$scope.buttonDisabled = false;
				$scope.setCurrentUser(user);
				$location.path('/home').replace();
			}
			else {
				$scope.loginFailed = true;
				$scope.loading = false;
				$scope.buttonDisabled = false;
				$rootScope.$broadcast(AUTH_EVENTS.loginFailed);
			}
		}, function () {
			$scope.loginFailed = true;
			$scope.loading = false;
			$scope.buttonDisabled = false;
			$rootScope.$broadcast(AUTH_EVENTS.loginFailed);
		});
	};
}

function loginFailureService(AUTH_EVENTS, $scope) {
	this.listen = function(callback) {
		$rootScope.$on(AUTH_EVENTS.loginFailed, function(){
			$scope.loginFailed = true;
		})
	}
}

// fblogin

function fbloginController ($location, $scope, $rootScope, AUTH_EVENTS, authService) {
	$scope.fbat = '';
	$scope.fblogin = function (fbat) {
		$scope.loading = true;
		authService.fblogin(fbat).then(function (user) {
			if (user) {
				$rootScope.$broadcast(AUTH_EVENTS.loginSuccess);
				$scope.loginFailed = false;
				$scope.loading = false;
				$scope.setCurrentUser(user);
				$location.path('/home').replace();
			}
			else {
				$scope.loginFailed = true;
				$rootScope.$broadcast(AUTH_EVENTS.loginFailed);
			}
			$scope.loading = false;
		}, function () {
			$scope.loginFailed = true;
			$scope.loading = false;
			$rootScope.$broadcast(AUTH_EVENTS.loginFailed);
		});
	};
}

// googlogin

function googloginController ($location, $scope, $rootScope, AUTH_EVENTS, authService) {
	$scope.googat = '';
	$scope.googlogin = function (googat) {
		$scope.loading = true;
		$scope.buttonDisabled = true;
		authService.googlogin(googat).then(function (user) {
			if (user) {
				$rootScope.$broadcast(AUTH_EVENTS.loginSuccess);
				$scope.loginFailed = false;
				$scope.loading = false;
				$scope.setCurrentUser(user);
				$location.path('/home').replace();
			}
			else {
				$scope.loginFailed = true;
				$rootScope.$broadcast(AUTH_EVENTS.loginFailed);
			}
			$scope.loading = false;
		}, function () {
			$scope.loginFailed = true;
			$scope.loading = false;
			$rootScope.$broadcast(AUTH_EVENTS.loginFailed);
		});
	};
}

// logout

function logoutController ($location, $scope, $rootScope, AUTH_EVENTS, authService, sessionService) {
	$scope.logout = function () {
		sessionService.destroy();
		$rootScope.$broadcast(AUTH_EVENTS.logoutSuccess);
		$scope.clearCurrentUser();
		console.log('in logout');
		var auth2 = gapi.auth2.getAuthInstance();
		auth2.signOut().then(function () {
			$rootScope.$apply(function() {
				$location.path('/');
				console.log($location.path());
				return;
			});
		});
	};
}

function sessionService($http, $rootScope) {
	this.create = function (userId, userIdno , userRole, at, rt) {
		this.id = userId;
		this.userIdno = userIdno;
		this.userId = userId;
		this.userRole = userRole;
		this.at = at;
		this.rt = rt;
	};
	this.destroy = function () {
		this.id = null;
		this.userId = null;
		this.userRole = null;
		this.at = null;
		this.rt = null;
	};
}

function authService($http, sessionService, CLIENT_ID, CLIENT_SECRET, USER_ROLES) {
	var authService = {};

	authService.login = function (credentials) {
		return $http.post('/auth/token', {
			'client_id': CLIENT_ID,
			'client_secret': CLIENT_SECRET,
			'grant_type': 'password',
			'username': credentials.username,
			'password': credentials.password
		}).then(function(res){
			at = res.data.access_token;
			rt = res.data.refresh_token;
			return $http.get('/djoser-auth/me/', {
				headers: {'Authorization': 'Django ' + at}
			}).then(function(res){
				user = {'userId': credentials.username, 'userIdno': res.data.id, 'role': USER_ROLES.user, 'at': at, 'rt': rt};
				sessionService.create(user['username'], user['userIdno'], user['userRole'], user['at'], user['rt']);
				return user;
			});
	   });
	};

	authService.fblogin = function (fbat) {
		return $http.post('/auth/convert-token', {
			'grant_type': 'convert_token',
			'client_id': CLIENT_ID,
			'client_secret': CLIENT_SECRET,
			'backend': 'facebook',
			'token': fbat,
		}).then(function(res){
			at = res.data.access_token;
			rt = res.data.refresh_token;
			return $http.get('/djoser-auth/me/', {
				headers: {'Authorization': 'Django ' + at}
			}).then(function(res){
				user = {'userId': res.data.username, 'userIdno': res.data.id, 'role': USER_ROLES.user, 'at': at, 'rt': rt};
				sessionService.create(user['userId'], user['userIdno'], user['userRole'], user['at'], user['rt']);
				return user;
			});
		});
	};

	authService.googlogin = function (googat) {
		return $http.post('/auth/convert-token', {
			'grant_type': 'convert_token',
			'client_id': CLIENT_ID,
			'client_secret': CLIENT_SECRET,
			'backend': 'google-oauth2',
			'token': googat,
		}).then(function(res){
			at = res.data.access_token;
			rt = res.data.refresh_token;
			return $http.get('/djoser-auth/me/', {
				headers: {'Authorization': 'Django ' + at}
			}).then(function(res){
				user = {'userId': res.data.username, 'userIdno':res.data.id ,'role': USER_ROLES.user, 'at': at, 'rt': rt};
				sessionService.create(user['userId'], user['userIdno'], user['userRole'], user['at'], user['rt'], res);
				return user;
			});
	   });
	};

	authService.signup = function (credentials) {
		return $http.post('/djoser-auth/register/', {
			'username': credentials.username,
			'email': credentials.username,
			'password': credentials.password,
		}).then(function(res){
			if (res && res.data && res.data.id > 0)
				return res['username'];
			else
				throw 'SignupExpception';
		});
	};

	// no need for logout service since backend is stateless

	authService.isAuthenticated = function () {
		return !!sessionService.userId;
	};

	authService.isAuthorized = function (authorizedRoles) {
		if (!angular.isArray(authorizedRoles)) {
			authorizedRoles = [authorizedRoles];
		}
		return (authService.isAuthenticated() && authorizedRoles.indexOf(sessionService.userRole) !== -1);
	};

	return authService;
}

function CarouselDemoCtrl($scope){
	$scope.Interval = 5000;
	$scope.noWrapSlides = false;

	$scope.slides = [{
		title: "Django REST AngularJS Boilerplate",
		subtitle: "Welcome to Django REST AngularJS Boilerplate! - ES1",
		active : true,
		image: "/static/djangorestangularjsboilerplate/assets/img/logo.jpg",
		gbutton: 'gsignin0',
		socialbuttons: true,
	}];

	$scope.stopSlider = function () {
		$scope.noWrapSlides = true;
		console.log('slider stoped');
	}

	$scope.addSlide = function() {
		var newWidth = 600 + slides.length + 1;
		slides.push({
			title: "Django REST AngularJS Boilerplate",
			subtitle: "Welcome to Django REST AngularJS Boilerplate!",
			active : true,
			image: "/static/djangorestangularjsboilerplate/assets/img/logo.jpg"
		});
	};
}

function ajaxLoader(){
	return {
		restrict: 'E',
		replace:true,
		template: '<div class="loading"><br><img src="/static/djangorestangularjsboilerplate/assets/img/ajax-loader.gif" width="20" height="20"/> Loading...</div>',
		link: function (scope, element, attr) {
			scope.$watch('loading', function (val) {
				if (val)
					$(element).show();
				else
					$(element).hide();
			});
		}
	}
}

angular
	.module('angularjsboilerplate', ['ui.bootstrap', 'ngRoute', 'angularjsboilerplate.home', 'angularjsboilerplate.profile'], httpAcceptJson)
	// configs:
	.config(appConfig)
	.config(['$routeProvider', function($routeProvider) {
		$routeProvider.otherwise({redirectTo: '/'});
	}])
	// constants:
	.constant('USER_ROLES', {'all': '*', 'usermanager': 1, 'user': 0})
	.constant('AUTH_EVENTS', { loginSuccess: 'auth-login-success', loginFailed: 'auth-login-failed', signupSuccess: 'auth-signup-success', signupFailed: 'auth-signup-failed', logoutSuccess: 'auth-logout-success', sessionTimeout: 'auth-session-timeout', notAuthenticated: 'auth-not-authenticated', notAuthorized: 'auth-not-authorized' })
	.constant('CLIENT_ID', 'GwTf8YnLb4giiPa3mhEpj1MwfKN9HFUYL6yGwpXw')
	.constant('CLIENT_SECRET', 'Fwb9AgayN7RN5Gn3HlwKebw2XZS2jSvMP7yZHTNs8HYyzK9l0wiaecpm8PY9DsBX7urL2w8L0UYw14j2A7bIRZqrqyeiUatvw3ccWf81bR904SMt056OAE5FUK0edqi8')
	// controllers:
	.controller('appController', appController)
	.directive('loading', ajaxLoader)
	.controller('CarouselDemoCtrl',CarouselDemoCtrl)
	// signup
	.controller('signupController', signupController)
	.service('signupFailureService', signupFailureService)
	// login
	.controller('loginController', loginController)
	.service('loginFailureService', loginFailureService)
	// fblogin
	.controller('fbloginController', fbloginController)
	// googlogin
	.controller('googloginController', googloginController)
	// logout
	.controller('logoutController', logoutController)
	// session
	.service('sessionService', sessionService)
	.factory('authService', authService);
