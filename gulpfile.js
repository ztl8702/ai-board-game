const gulp = require('gulp');
const webpack = require('webpack');
const del = require('del');
const webpackConfigFrontend = require('./webpack.config.frontend.js')

gulp.task('frontend:build', ['frontend:build:webpack'],()=> {
    return gulp.src(['./www-src/index.html','./www-src/main.css'])
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

gulp.task('frontend:watch', ()=>{
    return gulp.watch('www-src/**/*', ["frontend:build"]);
});

gulp.task('frontend:rebuild',['frontend:clean','frontend:build']);