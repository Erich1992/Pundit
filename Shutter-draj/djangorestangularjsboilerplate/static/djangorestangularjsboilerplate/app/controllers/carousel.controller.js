(function () {
    'use strict';
    
	angular
    .module('angularjsboilerplate')
    .controller('CarouselCtrl', CarouselCtrl);

CarouselCtrl.$inject = ['$scope'];

function CarouselCtrl ($scope) {

    var vm = this;
    vm.myInterval = 5000;
    vm.noWrapSlides = false;

   
   var slides = vm.slides = [];

  vm.addSlide = function() {
    var newWidth = 600 + slides.length + 1;
    slides.push({
      image: '//placekitten.com/' + newWidth + '/300',
      text: ['More','Extra','Lots of','Surplus'][slides.length % 4] + ' ' +
        ['Cats', 'Kittys', 'Felines', 'Cutes'][slides.length % 4]
    });
  };

  for (var i=0; i<4; i++) {
    vm.addSlide();
  }

    // goog login
      function onSuccess(googleUser) {
        $('#googat').val(googleUser.po.access_token);
        angular.element($('#googat')).triggerHandler('input');
        $('#googloginFormSubmit').click();
        console.log('finished clicking googloginFormSubmit');
      }

      function onFailure(error) {
        console.log(error);
      }
      function onLoad() {
        console.log('in onLoad');
        gapi.load('auth2', function() {
          gapi.auth2.init();
          renderButton();
        });
      }

      function renderButton(buttonName) {
        gapi.signin2.render(buttonName, {
          'scope': 'https://www.googleapis.com/auth/plus.login',
          'width': 200,
          'height': 50,
          'longtitle': true,
          'theme': 'dark',
          'onsuccess': onSuccess,
          'onfailure': onFailure
        });
      }
}


}());