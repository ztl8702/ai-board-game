const gulp = require('gulp');
const webpack = require('webpack');
const del = require('del');
const webpackConfigFrontend = require('./webpack.config.frontend.js')

gulp.task('frontend:build', ['frontend:build:webpack'],()=> {
    return gulp.src('./www-src/index.html')
    .pipe(gulp.dest('./public'));
});

gulp.task('frontend:build:webpack', (done)=> {
    webpack(webpackConfigFrontend).run((err,stats) => {
        done();
    })
});

gulp.task('frontend:clean', ()=>{
    return del('public/**', {force:true});
});

gulp.task('frontend:rebuild',['frontend:clean','frontend:build']);