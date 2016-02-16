import gulp from 'gulp'
import gulpPlugins from 'gulp-load-plugins'

import {webpackConfig} from './config'

const $ = gulpPlugins()

const exec = (watch) => {
  webpackConfig.watch = watch
  return gulp.src(webpackConfig.entry)
    .pipe($.webpack(webpackConfig))
    .pipe(gulp.dest(webpackConfig.output.path))
}

gulp.task('js', () => {
  return exec(false)
})

gulp.task('js:watch', () => {
  return exec(true)
})
