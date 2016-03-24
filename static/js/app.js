var IMDBAPIApp = angular.module('IMDBAPIApp', [
  'ngRoute',
  'IMDBAPIControllers',
  'IMDBAPIFilters'
]);

IMDBAPIApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/movie/', {
        templateUrl: '/static/html/search.html',
        controller: 'ArtistListCtrl'
      }).
      when('/movie/:Search', {
        templateUrl: '/static/html/search.html',
        controller: 'ArtistListCtrl'
      }).
      when('/albums/:ArtistId/:ArtistName', {
        templateUrl: '/static/html/albums.html',
        controller: 'AlbumsCtrl'
      }).
      when('/tracks/:AlbumId/:AlbumName/:ArtistName', {
        templateUrl: '/static/html/tracks.html',
        controller: 'TracksCtrl'
      }).
      when('/play/:TrackId/:TrackName/:AlbumName/:ArtistName', {
        templateUrl: '/static/html/play.html',
        controller: 'PlayCtrl'
      }).
      otherwise({
        redirectTo: '/movie'
      });
  }]);
