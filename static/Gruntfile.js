module.exports = function(grunt) {

	grunt.initConfig({

		pkg: grunt.file.readJSON("package.json"),

		clean: ["build"],

		concat: {

			indexjs:{
				options: {
					separator: ";",
				},
				src: [
					"bower_components/salvattore/dist/salvattore.js",
					"js/index.js"
				],
				dest: "js/index.concat.js"
			},

			js: {
				options: {
					separator: ";",
				},
				src: [
					"bower_components/mustache/mustache.js",
					"js/main.js"
				],
					//file output
				dest: "js/main.concat.js"
			},
			css: {
				src: [
				"css/kube.min.css",
				"css/fontello.css",
				"css/styles.css"
				],
				dest: "css/styles.concat.css"
			}

		},

		cssmin: {
			minify: {
				expand: true,
				cwd: "css",
				src: ["styles.concat.css"],
				dest: "css",
				ext: ".min.css"
			}
		},
		uglify: {
			scripts: {
				files: {
					"js/main.min.js": ["js/main.concat.js"],
					"js/index.min.js": ["js/index.concat.js"]

				}
			}
		},

		watch: {
			options: {
				livereload: true
			},
			main: {
				files: [
					"css/less/*.less",
					"css/less/_partials/*.less",
					"js/*.js",
					"../templates/*.html",
					"../templates/_partials/*.html",
					"../templates/auth/*.html"
				],
				tasks: ["less:devel"]
			}

		},

		less: {
			devel: { 
				files: {
					"css/styles.css": "css/less/main.less"
				}
			}

		}

	});

	grunt.loadNpmTasks("grunt-contrib-less");
	grunt.loadNpmTasks("grunt-contrib-watch");
	grunt.loadNpmTasks("grunt-contrib-cssmin");
	grunt.loadNpmTasks("grunt-contrib-clean");
	grunt.loadNpmTasks("grunt-contrib-uglify");
	grunt.loadNpmTasks("grunt-contrib-copy"); 
	grunt.loadNpmTasks("grunt-contrib-concat"); 


	grunt.registerTask("default", ["watch:main"]);
	grunt.registerTask("build", ["less:devel", "concat:css", "concat:indexjs", "concat:js", "uglify", "cssmin" ]);

}

