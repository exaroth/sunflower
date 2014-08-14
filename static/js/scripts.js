(function(){

	// Initialization

	var $document = $(document),
		$window = $(window),
		$indexImageGrid = $("#index-image-grid"),
		images_per_page = 10,
		page = 1,
		bottom = false

	var images_list,
		number_of_images,
		images_count,
		images_shown

	// Templates
	var imageItemTemplate = "<img src='{{ thumb }}' title='{{ title  }}' class='index-image-item' data-img-href={{img}}>"

	$document.ready(function(){
		init();
	});

	function init(){
		$window.load(function(){
			main();
		});

	};

	function main(){
		$window.scroll(function(){
			if($window.scrollTop() + $window.height() == $document.height()){
				if (!bottom){
					page += 1;
					getImages(page, appendIndexImages);
				}
			}
		})
		images_shown = images_per_page;
		getImages(1, appendIndexImages);
	};

	function getImages(page, successFunc){
		 // Get image list from the server
		$.ajax({
			url: "/image_list/"+ images_per_page + "/" + page
		}).success(function(data, code){
			imagesList = data["data"];
			imagesCount = data["_meta"].images_count;
			successFunc(imagesList);
			return
		}).error(function(){
			 bottom = true;
			 return
		})

	};

	function appendIndexImages(imageData){
			for(var count = 0; count < imageData.length; count +=1){
				var i = count + 1
				url = imageData[count].thumb;
				title = imageData[count].title;
				el = Mustache.render(imageItemTemplate, imageData[count])
				var item = document.createElement("div");
				item.className = "image-container";
				salvattore["append_elements"]($indexImageGrid.get()[0], [item])
				item.innerHTML = el;
				$(item).fadeIn("fast");
			}
		 
	}


}());
