import gulp from 'gulp'
import gulpPlugins from 'gulp-load-plugins'
import NpmImportPlugin from 'less-plugin-npm-import'
import lessPluginGlob from 'less-plugin-glob'

const $ = gulpPlugins()

import {browsers, dist} from './config'

gulp.task('styles', () => {
  return gulp.src('styles/main.less')
  .pipe($.less({
    plugins: [
      new NpmImportPlugin(),
      lessPluginGlob
    ]
  }))
  .pipe($.autoprefixer({browsers}))
  .pipe(gulp.dest(dist))
})
