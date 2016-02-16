/* eslint no-var:0 */

//
// Gulpfile
// ========
//

var gulp = require('gulp')

// Setup babel transforms for tests and other task definitions
require('babel-core/register')({
  ignore: ['node_modules']
})

// Load all tasks from the tasks directory
require('require-dir')('tasks')

gulp.task('build', ['clean', 'js'])

gulp.task('build:dev', ['clean', 'js:watch'])

gulp.task('default', ['build'])

