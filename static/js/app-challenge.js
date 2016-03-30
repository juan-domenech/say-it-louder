var ChallengeApp = angular.module('ChallengeApp', [
  'ngRoute',
  'ChallengeControllers',
]);

ChallengeApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.

    when('/challenge/movie/', {
        templateUrl: '/challenge/search_movie',
        controller: 'MovieSearchCtrl'
      }).
    when('/challenge/movie/:Search', {
        templateUrl: '/challenge/search_movie',
        controller: 'MovieSearchCtrl'
      }).
    when('/challenge/movie_selected/:movieID', {
        templateUrl: '/challenge/movie_selected/',
        controller: 'MovieSelectedCtrl'
      }).

    otherwise({
        redirectTo: '/challenge/movie'
      });
  }]);
