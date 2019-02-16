
// requirements
var gulp = require('gulp');
var concat = require('gulp-concat');
var react = require('gulp-react');
var uglify = require('gulp-uglify');

var gulpBrowser = require("gulp-browser");
var reactify = require('reactify');
var del = require('del');
var size = require('gulp-size');


var path = {
  JS: ['./src/jsx/*.js', './src/js/**/*.js'],
  MINIFIED_OUT: 'build.min.js',
  DEST_SRC: '../backend/app/static/scripts/js/src',
  DEST_BUILD: '../backend/app/static/scripts/js/build',
  DEST: '../backend/app/static/scripts/js/src'
}

// gulp.task('copy', function(){
//   gulp.src(path.HTML)
//     .pipe(gulp.dest(path.DEST));
// });

// tasks
function transform() {
  return gulp.src(path.JS)
    .pipe(react())
    .pipe(gulp.dest(path.DEST_SRC));
    // .pipe(gulpBrowser.browserify({transform: ['reactify']}))
    // .pipe(gulp.dest("../backend/app/static/scripts/js"))
    // .pipe(size());
}
gulp.task('build', function(){
  gulp.src(path.JS)
    .pipe(react())
    .pipe(concat(path.MINIFIED_OUT))
    .pipe(uglify(path.MINIFIED_OUT))
    .pipe(gulp.dest(path.DEST_BUILD));
});

function clean() {
  return del(path.DEST_SRC, {force: true});
}

var build = gulp.series(clean, transform)
gulp.task('default', function() {
  gulp.watch(path.JS, build);
});
