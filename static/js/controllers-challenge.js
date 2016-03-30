var ChallengeControllers = angular.module('ChallengeControllers', []);

//
ChallengeControllers.controller('ChallengeCtrl', ['$scope', '$routeParams', '$http',
  function($scope, $routeParams, $http) {

      console.log("Login Called")

  }]
);


// Challenge Movie Search
ChallengeControllers.controller('MovieSearchCtrl', ['$scope', '$routeParams', '$http', '$location',

  // Function executed when we get an artist name at the URL Parameters
  function ($scope, $routeParams, $http, $location) {

    // Make sure we have something in the URL to work with
    if ($routeParams.Search){
      // Search Artist using the string in the URL
      $http.get('http://127.0.0.1:5000/api/v0/search/'+ $routeParams.Search +'/movie').success(function(data) {
        $scope.artists = data;
      });
    }

    //
    // Function executed everytime Input has changed
    $scope.typeSearch = function(Search) {

      // Make sure the user has entered something in Input (it might be a backspace)
      if (Search != undefined && Search != ''){

        // Search Artist with whatever we have in the search box
        $http.get('http://127.0.0.1:5000/api/v0/search/'+ Search +'/movie').success(function(data) {
          $scope.artists = data;
          //console.log(data)
        });
      }
    };

    $scope.typeEnter = function(Search) {

      // Make sure the user has entered something in Input (it might be a backspace)
      if (Search != undefined && Search != ''){

        // Search Artist with whatever we have in the search box
        $http.get('http://127.0.0.1:5000/api/v0/search/'+ Search +'/movie').success(function(data) {
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
ChallengeControllers.controller('MovieSelectedCtrl', ['$scope', '$routeParams', '$http',
  function($scope, $routeParams, $http) {

    //$http.get('https://api.spotify.com/v1/artists/'+ $routeParams.ArtistId +'/albums').success(function(data) {
    //    $scope.albums = data.items;
    //  });

    //$scope.GetAlbumYear= function(AlbumId) {
    //  $http.get('https://api.spotify.com/v1/albums/'+ AlbumId ).success(function(data) {
    //      //$scope.albums[i].AlbumYear = data.release_date.slice(0,4);
    //      //console.log(data.release_date.slice(0,4) );
    //      $scope.Year =  data.release_date.slice(0,4);
    //      console.log($scope.Year)
    //  });
    //}

    $scope.movieID = $routeParams.movieID;
      console.log($routeParams.movieID)
    //$scope.ArtistName = $routeParams.ArtistName;

  }]
);
