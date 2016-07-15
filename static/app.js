angular.module('myApp', []);

angular.module('myApp')
  .controller('aCtrl', function($scope, $http, $location, $anchorScroll, $interval) {

    $scope.distances = [];
	$scope.info = "";
	
	$scope.readDistances = true;
	$scope.baseURL = '';//'http://192.168.43.49:8080';
	
	$scope.getDistances = function(){
		$scope.apicall('distance', function(response){
			$scope.distances = response.data;
		});
	};
	
	
	$scope.init = function(){
		$interval(function(){
			if($scope.readDistances){
				$scope.getDistances();
			}
		}, 800);
	};
	
	$scope.apicall = function(apimethod, callback){
		
		$http({
		  method: 'GET',
		  url: $scope.baseURL + '/' + apimethod
		}).then(function successCallback(response) {
			$scope.info = "";
			if(callback){
				callback(response);
			}
		  }, function errorCallback(response) {
			$scope.info = response;
		  });
	};
	
	$scope.vor = function(){
		$scope.apicall('vor');
	}
	
	$scope.zurueck = function(){
		$scope.apicall('zurueck');
	}
	
	$scope.lampeAn = function(){
		$scope.apicall('an');
	}
	
	$scope.lampeAus = function(){
		$scope.apicall('aus');
	}
	
	$scope.links = function(){
		$scope.apicall('links');
	}
	
	$scope.rechts = function(){
		$scope.apicall('rechts');
	}
	
	
});
