var ResolveApp = angular.module('ResolveApp', [
  'ngRoute',
  'ResolveControllers',
]);

ResolveApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.


    when('/resolve/movie/:Search', {
        templateUrl: '/challenge/search_movie',
        controller: 'MovieSearchCtrl'
      }).


    when('/resolve/movie_selected/', {
        templateUrl: '/resolve/movie_selected/',
        controller: 'MovieSelectedCtrl'
      }).
    when('/resolve/movie_selected/:game_id', {
        templateUrl: '/resolve/movie_selected/',
        controller: 'MovieSelectedCtrl'
      }).

    when('/resolve/keywords/', {
        templateUrl: '/resolve/keywords',
        controller: 'ResolveKeywordsCtrl'
      }).

    otherwise({
        redirectTo: '/resolve/movie_selected/'
      });
  }]);
