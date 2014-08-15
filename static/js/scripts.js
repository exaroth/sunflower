(function(){

	// Initialization

	var $document = $(document),
		$window = $(window),
		$body = $("body"),
		$indexImageGrid = $("#index-image-grid"),
		$imageModal = $(".md-modal"),
		images_per_page = 10,
		page = 1,
		bottom = false,
		modalFields = ["title", "description", "author", "img"]

	var images_list,
		number_of_images,
		images_count,
		images_shown

	// Templates
	var imageItemTemplate = "<a href='#' class='index-img-open' data-img='{{img}}' data-author='{{author}}' data-desc='{{description}}' data-title='{{title}}'><img src='{{ thumb }}' title='{{ title  }}' class='index-image-item' data-img-href={{img}}></a>",
		imageDetailModalTemplate='<a href="#" class="md-modal-close">&times;</a> <div class="md-modal-image "><img src="{{img}}" alt="{{title}}" /> </div><div class="md-modal-desc"><h3 class="md-modal-title">{{title}}</h3> <h6>Uploaded by: {{author}}</h6> <p>{{description}}</p> </div>'

	$document.ready(function(){
		init();
	});

	function init(){
		$window.load(function(){
			main();
		});

	};

	function main(){

		$indexImageGrid.on("click", ".index-img-open", function(e){
			e.preventDefault();
			imageModalDisplay($(this));
		});

		$window.scroll(function(){
			if($window.scrollTop() + $window.height() == $document.height()){
				if (!bottom){
					page += 1;
					getImages(page, appendIndexImages);
				}
			}
		});
		images_shown = images_per_page;
		getImages(1, appendIndexImages);
	};

	function imageModalDisplay(el){
		data = new Object();

		for(var i = 0; i < modalFields.length; i++){
			 data[modalFields[i]] = el.data(modalFields[i]);
		};

		var template = Mustache.render(imageDetailModalTemplate, data);
		$imageModal.append(template);
		$imageModal.addClass("md-show");
	}

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
