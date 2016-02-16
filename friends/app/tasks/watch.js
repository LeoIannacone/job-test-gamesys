import gulp from 'gulp'

// watch less, html and js file changes
gulp.task('watch', () => {
  gulp.start('js:watch')
  gulp.watch('styles/**/*.less', ['styles'])
})
