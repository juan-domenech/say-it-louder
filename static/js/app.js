var IMDBAPIApp = angular.module('IMDBAPIApp', [
  'ngRoute',
  'IMDBAPIControllers',
  'IMDBAPIFilters'
]);

IMDBAPIApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.

    when('/login', {
        templateUrl: '/login',
        controller: 'Login'
      }).

    when('/movie/', {
        templateUrl: '/static/html/search.html',
        controller: 'ArtistListCtrl'
      }).
    when('/movie/:Search', {
        templateUrl: '/static/html/search.html',
        controller: 'ArtistListCtrl'
      }).

    when('/status', {
        templateUrl: '/status.html',
        controller: 'StatusCtrl'
      }).

    otherwise({
        redirectTo: '/login'
      });
  }]);
