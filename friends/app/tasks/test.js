import gulp from 'gulp'
import gulpPlugins from 'gulp-load-plugins'

const $ = gulpPlugins()

function _getTest() {
  return gulp.src([
    'test/bootstrap.js',
    'test/components/**/*.js'
  ], {read: false})
  .pipe($.mocha({
    timeout: 10000
  }))
}

gulp.task('_test', () => {
  return _getTest()
})

gulp.task('test', () => {
  return _getTest().on('end', () => process.exit(0))
})

gulp.task('bdd', () => {
  gulp.watch('scripts/**/*.js', ['_test'])
  gulp.watch('test/**/*.js', ['_test'])
})
