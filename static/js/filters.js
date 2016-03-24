// Filter to whitelist the IMDB CDN as valid external resource
//https://docs.angularjs.org/api/ng/provider/$sceDelegateProvider
//
angular.module('IMDBAPIFilters', []).config(function($sceDelegateProvider) {
  $sceDelegateProvider.resourceUrlWhitelist([
    // Allow same origin resource loads.
    'self',
    // Allow loading from our assets domain.  Notice the difference between * and **.
    'https://*.scdn.co/**'
  ]);
});
