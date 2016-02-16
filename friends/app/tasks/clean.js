//
// Cleanup task
// ============
//

import gulp from 'gulp'
import del from 'del'

import {dist} from './config'

gulp.task('clean', () => {
  return del([dist], {force: true})
})
