
var IMDBAPIControllers = angular.module('IMDBAPIControllers', []);

// Artists Search (Main page)
IMDBAPIControllers.controller('ArtistListCtrl', ['$scope', '$routeParams', '$http', '$location',

  // Function executed when we get an artist name at the URL Parameters
  function ($scope, $routeParams, $http, $location) {

    // Make sure we have something in the URL to work with
    if ($routeParams.Search){
      // Search Artist using the string in the URL
      $http.get('http://127.0.0.1:5000/api/search/'+ $routeParams.Search +'/movie').success(function(data) {
        $scope.artists = data;
      });
    }

    //
    // Function executed everytime Input has changed
    $scope.typeSearch = function(Search) {

      // Make sure the user has entered something in Input (it might be a backspace)
      if (Search != undefined && Search != ''){

        // Search Artist with whatever we have in the search box
        $http.get('http://127.0.0.1:5000/api/search/'+ Search +'/movie').success(function(data) {
          $scope.artists = data;
          //console.log(data)
        });
      }
    };

    $scope.typeEnter = function(Search) {

      // Make sure the user has entered something in Input (it might be a backspace)
      if (Search != undefined && Search != ''){

        // Search Artist with whatever we have in the search box
        $http.get('http://127.0.0.1:5000/api/search/'+ Search +'/movie').success(function(data) {
          $scope.artists = data;
          //console.log(data)
          // After Enter Key detected send user to Albums choosing the first artist of the list
          $location.path("albums/"+data[0].movieID+"/"+data[0].title)
        });

      }
    };

  }]
);


// Show Albums
IMDBAPIControllers.controller('AlbumsCtrl', ['$scope', '$routeParams', '$http',
  function($scope, $routeParams, $http) {

    $http.get('https://api.IMDB.com/v1/artists/'+ $routeParams.ArtistId +'/albums').success(function(data) {
        $scope.albums = data.items;
      });

    //$scope.GetAlbumYear= function(AlbumId) {
    //  $http.get('https://api.IMDB.com/v1/albums/'+ AlbumId ).success(function(data) {
    //      //$scope.albums[i].AlbumYear = data.release_date.slice(0,4);
    //      //console.log(data.release_date.slice(0,4) );
    //      $scope.Year =  data.release_date.slice(0,4);
    //      console.log($scope.Year)
    //  });
    //}

    $scope.ArtistId = $routeParams.ArtistId;
    $scope.ArtistName = $routeParams.ArtistName;

  }]
);


// Show Tracks
IMDBAPIControllers.controller('TracksCtrl', ['$scope', '$routeParams', '$http',
  function($scope, $routeParams, $http) {

    $http.get('https://api.IMDB.com/v1/albums/'+ $routeParams.AlbumId).success(function(data) {
      // Get Album Thumbnail
      $scope.AlbumThumbnail = data.images[1].url;
      // Get Release Year
      $scope.AlbumYear = data.release_date.slice(0,4)
      //
      $scope.ArtistId = data.artists[0].id;
    });


    // Get Track List
    $http.get('https://api.IMDB.com/v1/albums/'+ $routeParams.AlbumId +'/tracks').success(function(data) {
      $scope.tracks = data.items;
      });

    $scope.AlbumName = $routeParams.AlbumName;
    $scope.ArtistName = $routeParams.ArtistName;

  }]
);


// Play Track
IMDBAPIControllers.controller('PlayCtrl', ['$scope', '$routeParams', '$http',
  function($scope, $routeParams, $http) {

    $http.get('https://api.IMDB.com/v1/tracks/'+ $routeParams.TrackId).success(function(data) {
      $scope.track = data;
      // Get Album Thumbnail
      $scope.AlbumThumbnail = data.album.images[1].url;
      //
      $scope.ArtistId = data.artists[0].id;
      $scope.ArtistName = data.artists[0].name;
      $scope.AlbumId = data.album.id;

        // Get Release Year using the previously obtained AlbumId
        $http.get('https://api.IMDB.com/v1/albums/'+ $scope.AlbumId).success(function(data) {
          $scope.AlbumYear = data.release_date.slice(0,4)
        });

      });

    $scope.TrackName = $routeParams.TrackName;
    $scope.AlbumName = $routeParams.AlbumName;
    $scope.ArtistName = $routeParams.ArtistName;

  }]
);
