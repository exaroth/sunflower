(function(){

	var $window = $(window),
		$document = $(document),
		$body = $("body"),
		$accImgList = $("#account-info-image-list"),
		user_id = parseInt($("#user_hidden").val())

	var imgFragmentTemplate = '<a href="/image/{{pk}}"><img src="{{thumbnail}}"><div class="account-image-overlay"></div></a>'

	
		$document.ready(function(){
			init()
		})

		function init(){

			$window.load(function(){
				main()
			});

		};

		function main(){
			showAccImages();
		}

		function showAccImages(){
			$.ajax({
				url: "/user_image_list/" + user_id
			}).success(function(data, code){
				var images = data["data"];

				for (var i=0; i < images.length; i++ ){
					var imgData = {
						 thumbnail : images[i].thumb,
						 pk : images[i].pk
					};
					el = Mustache.render(imgFragmentTemplate, imgData);
					
					var item = document.createElement("div");
					item.className = "account-image-wrapper"
					salvattore["append_elements"]($accImgList[0], [item])
					item.innerHTML = el
				}
			})
		}



}());
