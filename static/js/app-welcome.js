var WelcomeApp = angular.module('WelcomeApp', [
  'ngRoute',
  'WelcomeControllers',
]);

WelcomeApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.

    when('/welcome/movie/', {
        templateUrl: '/welcome/movie/',
        controller: 'MovieSearchCtrl'
      }).
    when('/welcome/movie/:Search', {
        templateUrl: '/welcome/movie/',
        controller: 'MovieSearchCtrl'
      }).

    otherwise({
        redirectTo: '/welcome/movie'
      });
  }]);
