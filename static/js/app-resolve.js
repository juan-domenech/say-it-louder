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

    when('/resolve/movie_selected/keywords/', {
        templateUrl: '/resolve/movie_selected/keywords/',
        controller: 'ResolveKeywordsCtrl'
      }).

    when('/resolve/movie_selected/keywords/check/', {
        templateUrl: '/resolve/movie_selected/keywords/check/',
        controller: 'ResolveKeywordsCheckCtrl'
      }).

    otherwise({
        redirectTo: '/resolve/movie_selected/'
      });

  }]);
