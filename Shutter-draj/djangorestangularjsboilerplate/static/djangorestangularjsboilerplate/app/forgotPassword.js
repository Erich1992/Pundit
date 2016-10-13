angular.module('forgotPassword', []).controller(
        'forgotPasswordCtrl',
        [
            '$scope',
            '$http',
            function($scope, $http)
            {
                $scope.success = false;
                $scope.error = false;
                $scope.email = '';
                $scope.message = '';
                $scope.processing = false;

                $scope.sendResetEmail = function()
                {
                   $scope.processing = true;
                   csrf_token = angular.element(
                    'input[name=csrfmiddlewaretoken]'
                    ).val()
                    data = {
                        email: $scope.email,
                        csrfmiddlewaretoken: csrf_token
                    }
                    headers = {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                   $http.post(
                    CONFIG.url,
                    $.param(data),
                    {headers:headers}
                    ).then(
                        function()
                        {
                            $scope.success = true;
                            $scope.error = false;
                            $scope.message = 'Check your email for the password reset link'
                        },
                        function(response)
                        {
                            if(response.status == 404)
                            {
                                $scope.message = 'No user has that email, kindly try again.'
                            }
                            else
                            {
                                $scope.message = 'An error occurred, kindly try again.'
                            }
                            $scope.error = true;
                        }
                    ).then(
                        function(){
                            $scope.processing = false;
                        }
                    );
                }
            }
        ]
);
