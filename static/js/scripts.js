(function(){

	// Initialization

	var $document = $(document),
		$window = $(window),
		$images_list_container = $("#index-images-list")

	var images_list,
		number_of_images,
		images_count

	// Templates
	var imageItemTemplate = "<li><img src='{{ thumb }}' title='{{ title  }}' class='index-image-item'></li>"
	$document.ready(function(){
		init();
	})

	function init(){


		$window.load(function(){
			main();
		});

	};

	function main(){
		console.log("running main function")
		getImages(1, appendIndexImages);
	};

	function getImages(page, successFunc){
		 // Get image list from the server
		$.ajax({
			url: "/image_list/10/" + page
		}).success(function(data, code){
			imagesList = data["data"];
			imagesCount = data["_meta"].images_count;
			successFunc(imagesList);
			return
		});

	};

	function appendIndexImages(imageData){
			for(var count = 0; count < imageData.length; count +=1){
				url = imageData[count].thumb;
				title = imageData[count].title;
				el = Mustache.render(imageItemTemplate, imageData[count])
				$images_list_container.append(el)
			}
		 
	}


}());
