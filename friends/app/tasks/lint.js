import gulp from 'gulp'
import gulpPlugins from 'gulp-load-plugins'

const $ = gulpPlugins()

gulp.task('lint', () => {
  return gulp.src([
    'scripts/**/*.js',
    'gulpfile.js',
    'tasks/*.js'
  ])
    .pipe($.eslint())
    .pipe($.eslint.format())
    .pipe($.eslint.failAfterError())
})
