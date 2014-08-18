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
	var imageItemTemplate = "<a href='#' class='index-img-open' data-img='{{img}}' data-author='{{author}}' data-description='{{description}}' data-title='{{title}}'><img src='{{ thumb }}' title='{{ title  }}' class='index-image-item' data-img-href={{img}}><div class='image-overlay'><span>X</span></div></a>",
		imageDetailModalTemplate='<a href="#" class="md-modal-close">&times;</a> <div class="md-modal-image "><img src="{{img}}" alt="{{title}}" /> </div><div class="md-modal-desc"><h3 class="md-modal-title">{{title}}</h3><h6>Uploaded by {{author}}</h6> <p>{{description}}</p> </div>'

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

		$document.keyup(function(e){
			if (e.keyCode == 27){
				if ($body.hasClass("modal-open")){
					closeModalWindow();
				}
			}
		});

		$document.on("click", ".md-modal-close", function(e){
			e.preventDefault();
			closeModalWindow();
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
		salvattore["register_grid"]($indexImageGrid[0]);
		getImages(1, appendIndexImages);
	};

	function imageModalDisplay(el){
		data = new Object();
		for(var i = 0; i < modalFields.length; i++){
			if ((modalFields[i] === "description") & !el.data("description")){
				data["description"] = "No description given";
				continue;
			}
			 data[modalFields[i]] = el.data(modalFields[i]);
		};

		var template = Mustache.render(imageDetailModalTemplate, data);
		$imageModal.append(template).addClass("md-show")
		$body.addClass("modal-open");
	}

	function closeModalWindow(){
		 $body.removeClass("modal-open");
		 $imageModal.removeClass("md-show").empty();
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
			 if(page === 1){
				$indexImageGrid.append("<h3>No images uploaded yet</h3>");
			 }
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
				salvattore["append_elements"]($indexImageGrid[0], [item])
				item.innerHTML = el;
				$(item).fadeIn("fast");
			}
	}

}());
