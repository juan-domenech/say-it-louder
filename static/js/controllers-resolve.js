var ResolveControllers = angular.module('ResolveControllers', []);

//
ResolveControllers.controller('ResolveCtrl', ['$scope', '$routeParams', '$http',
  function($scope, $routeParams, $http) {

      //console.log("Login Called")

  }]
);


// Resolve Movie Search
ResolveControllers.controller('MovieSearchCtrl', ['$scope', '$routeParams', '$http', '$location',

  // Function executed when we get a movie name at the URL Parameters
  function ($scope, $routeParams, $http, $location) {

    // Make sure we have something in the URL to work with
    if ($routeParams.Search){
      // Search Artist using the string in the URL
      $http.get('http://127.0.0.1:5000/api/v0/search/'+ $routeParams.Search +'/movie').success(function(data) {
        $scope.movies = data;
      });
    }

    //
    // Function executed every time Input has changed
    $scope.typeSearch = function(Search) {

      // Make sure the user has entered something in Input (it might be a backspace)
      if (Search != undefined && Search != ''){

        // Search Movie with whatever we have in the search box
        $http.get('http://127.0.0.1:5000/api/v0/search/'+ Search +'/movie').success(function(data) {
          $scope.movies = data;
          //console.log(data)
        });
      }
    };

    // Function executed when Enter
    $scope.typeEnter = function(Search) {

      // Make sure the user has entered something in Input (it might be a backspace)
      if (Search != undefined && Search != ''){

        // Search Movie with whatever we have in the search box
        $http.get('http://127.0.0.1:5000/api/v0/search/'+ Search +'/movie').success(function(data) {
          $scope.movies = data;
          //console.log(data)
          // After Enter Key detected send user to Albums choosing the first artist of the list
          $location.path("Resolve/movie_selected/"+data[0].movieID);

        });

      }
    };

  }]
);



//
ResolveControllers.controller('MovieSelectedCtrl', ['$scope', '$routeParams', '$http',
  function($scope, $routeParams, $http) {

    $http.get('http://127.0.0.1:5000/api/v0/secure/get/game_id/').success(function(data) {

        $scope.movieID = data.movieID;

        $http.get('http://127.0.0.1:5000/api/v0/get/title/'+ $scope.movieID).success(function(data2) {

        $scope.title = data2.title;
        $scope.year = data2.year;

        });

    });


  }]
);


//
ResolveControllers.controller('ResolveKeywordsCtrl', ['$scope', '$routeParams', '$http',
  function($scope, $routeParams, $http) {


  }]
);


//
ResolveControllers.controller('ResolveKeywordsCheckCtrl', ['$scope', '$routeParams', '$http',
  function($scope, $routeParams, $http) {

    $http.get('http://127.0.0.1:5000/api/v0/secure/get/game_id/').success(function(data) {

        $scope.movieID = data.movieID;

        $http.get('http://127.0.0.1:5000/api/v0/get/title/'+ $scope.movieID).success(function(data2) {

        $scope.title = data2.title;
        $scope.year = data2.year;

        });

    });

  }]
);
