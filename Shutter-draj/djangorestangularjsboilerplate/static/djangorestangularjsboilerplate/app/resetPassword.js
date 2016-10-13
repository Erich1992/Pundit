angular.module('resetPassword', []).controller(
        'resetPasswordCtrl',
        [
            '$scope',
            '$http',
            function($scope, $http)
            {
                $scope.newPassword = '';
                $scope.newPasswordRe = '';
                $scope.success = false;
                $scope.error = false;
                $scope.message = '';
                $scope.processing = false;

                $scope.resetPassword = function()
                {
                    if($scope.newPassword == '' || $scope.newPasswordRe == '')
                    {
                        $scope.message = 'All fields are required.';
                        $scope.error = true;
                        return;
                    }
                    if($scope.newPassword != $scope.newPasswordRe)
                    {
                        $scope.message = 'Password mismatch';
                        $scope.error = true;
                        return;
                    }
                    $scope.processing = true;
                    $http.post(
                    CONFIG.url,
                    {
                        'uid': CONFIG.uid,
                        'token': CONFIG.token,
                        'new_password': $scope.newPassword,
                        're_new_password': $scope.newPasswordRe
                    }
                    ).then(
                        function()
                        {
                            $scope.success = true;
                            $scope.error = false;
                            $scope.message = 'Password reset successful'
                        }, 
                        function()
                        {
                            $scope.error = true;
                            $scope.message = 'An error occurred, kindly try again.'
                        }
                    ).then(
                        function()
                        {
                            $scope.processing = false;
                        }
                    );
                }
            }
        ]
);
