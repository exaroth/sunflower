module.exports = function(grunt) {

	grunt.initConfig({

		pkg: grunt.file.readJSON("package.json"),

		clean: ["build"],

		concat: {

			js: {
				options: {
					separator: ";",
				},
				src: [
					// Files to be concatenated
				],
					//file output
				dest: "src/js/scripts.js"
			},
			css: {
				src: [
				// "src/css/main.css"
				],
				// dest: "css/styles.css"
			}

		},

		cssmin: {
			minify: {
				// expand: true,
				// cwd: "src/css",
				// src: ["styles.css"],
				// dest: "src/css",
				// ext: ".min.css"
			}
		},
		uglify: {
			scripts: {
				files: {
					// "src/js/scripts.min.js": ["src/js/scripts.js"]

				}
			}
		},

		copy: {
			main: {
				files: [
				// { expand: true, cwd: "src/img/", src: "*", dest: "build/img" },
				// { expand: true, cwd: "src/font/", src: "*", dest: "build/font" },
				// { expand: true, cwd: "src/css/", src: "styles.min.css", dest: "build/css/" },
				// { expand: true, cwd: "src/js/", src: "scripts.min.js", dest: "build/js/" },
				]
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
	grunt.registerTask("build", ["clean", "less:devel", "concat:css", "concat:js", "uglify", "cssmin", "copy"]);
	grunt.registerTask("bootstrap_compile", ["less:bootstrap"]);

}

