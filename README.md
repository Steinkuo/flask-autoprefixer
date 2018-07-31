# flask-autoprefixer
扩展阅读
http://flask-assets.readthedocs.io/en/latest/ 
Flask-Assets实例学习 
Flask-Assets中文参考

Flask-Assets
在访问 Web 应用的时候浏览器会在加载和解析为 HTML 文件之后, 再下载大量的 CSS/JS 文件, 发送了大量的 HTTP 请求. 虽然现在很多浏览器能够支持并行下载, 但也是由限制的, 所以这就成为了网页加载速度的另外一个瓶颈.

Flask-Assets 能够帮助我们将多个 CSS 或 JS 文件合并成为一个大的文件, 并且将这个文件中的空白符和换行符去除, 这样能够让文件的 Size 减少近 30%. 而且 Flask-Assets 还会使用特定的 HTTP Response Header, 让浏览器缓存这些文件, 只有在这些文件的内容被修改时, 才会再次下载, 这个功能一般的 HTTP 方式是不会有的.

而Autoprefixer解析CSS文件并且添加浏览器前缀到CSS规则里，使用Can I Use的数据来决定哪些前缀是需要的。

安装 Flask-Assets和Autoprefixer
pip install Flask Flask-Assets cssmin jsmin
pip freeze > requirements.txt
将 Flask-Assets 应用到项目中
初始化 assets 对象, 并创建打包对象 
vim assets.py
from flask import Flask
from flask_assets import Environment, Bundle
 
app = Flask(__name__)
 
# Flask-Assets's config
# Can not compress the CSS/JS on Dev environment.
app.config['ASSETS_DEBUG'] = True
 
#### Create the Flask-Assets's instance
assets_env = Environment(app)
 
# Define the set for js and css file.
css = Bundle(
    'css/test.css',
    'css/test1.css',
    filters='cssmin',
    output='assets/css/common.css')
 
js = Bundle(
    'js/test.js',
    filters='jsmin',
    output='assets/js/common.js')
 
# register
assets_env.register('js', js)
assets_env.register('css', css)
 
if __name__ == '__main__':
    app.run()
       NOTE 5: ProdConfig 不需要修改, 默认是自动打包压缩的 

NOTE 1: Bundel() 的构造器能够接受无限个文件名作为非关键字参数, 定义那些文件需要被打包, 这里主要打包本地 static 下的 CSS 和 JS 两种类型文件. 
NOTE 2: 关键字参数 filters 定义了这些需要被打包的文件通过那些过滤器(可以为若干个)进行预处理, 这里使用了 cssmin/jsmin 会将 CSS/JS 文件中的空白符和换行符去除. 
NOTE 3: 关键字参数 output 定义了打包后的包文件的存放路径 
NOTE 4: 上述的所有路径的前缀都会默认为 ./static/
注意: 在开发环境下不应该将 CSS/JS 文件打包, 因为我们可能会经常对这些文件进行修改, 所以需要设定在开发环境中不打包, 但生产环境中会自动进行打包.

使用特殊的 Jinja 控制代码来修改 templates 中的 CSS/JS 引用标签 <link> 或 <script>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Flask Assets GAE Example</title>
    <!--  assets应用 -->
  {% assets "css" %}
    <link href="{{ ASSET_URL }}" rel="stylesheet">
  {% endassets %}
    <!--  常规引用 -->
    <link href="{{ url_for('static', filename='css/test.css') }}" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/test1.css') }}" rel="stylesheet">
</head>
<body>
 
  <p id="main-text" class="center">beautiful</p>
    <!--  assets应用 -->
  {% assets "js" %}
    <script type="text/javascript" src="{{ ASSET_URL }}"></script>
  {% endassets %}
    <!--  常规引用 -->
    <script type="text/javascript" src="{{ url_for('static', filename='js/test.js') }}"></script>
</body>
</html>
 

经过这些处理之后, 如果 templates 文件的 link 或 script 使用的 css/js 文件路径已经被包含在了 Bunble 中, 那么这些原来会被加载到浏览器中 CSS/JS 文件, 将不会再被加载, 取而代之的是被压缩过的 Size 更小的文件.

FLASK_DEBUG=1 python app.py


现在将app.config['ASSETS_DEBUG'] = False，将会直接打包



这里可以看到打包的效果，速度和容量都有优化，特别是多个文件的情况。

将 autoprefixer应用到Flask-Assets中
由于需要使用postcss，用npm或者yarn下载一个

# 由于pip库里没有postcss，自己下一个吧
npm install postcss-cli autoprefixer --save-dev
配置autoprefixer， Flask-assets中已有相关类，直接配置参数就行

 AUTOPREFIXER_BIN 是指向postcss运行绝对路径下的bin

AUTOPREFIXER_BROWSERS 是配置浏览器版本的

import os
# get work root
basedir = os.path.abspath(os.path.dirname(__file__))
 
# Flask-Assets's config
# Can not compress the CSS/JS on Dev environment.
app.config['ASSETS_DEBUG'] = True
app.config['AUTOPREFIXER_BIN'] = basedir + '/node_modules/postcss-cli/bin/postcss'
app.config['AUTOPREFIXER_BROWSERS'] = ['> 1%', 'last 2 versions', 'firefox 24', 'opera 12.1']
最后加到flask-assets 就行了

# Define the set for js and css file.
css = Bundle(
    'css/test.css',
    'css/test1.css',
    filters='autoprefixer6, cssmin',
    output='assets/css/common.css')
注：autoprefixer >=6 时需要使用autoprefixer6，不然会失败的。

我们可以使用 flask 指令的方式来打包 CSS/JS 文件

(venv) ➜ flask assets clean
Cleaning generated assets...
Deleted asset: assets/js/common.js
Deleted asset: assets/css/common.css
 
(venv) ➜ flask assets build
Building bundle: assets/js/common.js
Building bundle: assets/css/common.css
 
来查看一下

<!--   编译前    -->
a {
background : linear-gradient(to top, black, white);
display : flex
}
::placeholder {
color : #ccc
}
 
<!--   编译后   -->
:-ms-input-placeholder {
color : #ccc
}
::-ms-input-placeholder {
color : #ccc
}
::placeholder {
color : #ccc
}
/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInN0ZGluIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7QUFDQTtBQUNBLG1EQUFtRDtBQUNuRCxjQUFjO0NBQ2I7QUFDRDtBQUNBLFlBQVk7Q0FDWDtBQUZEO0FBQ0EsWUFBWTtDQUNYO0FBRkQ7QUFDQSxZQUFZO0NBQ1g7QUFGRDtBQUNBLFlBQVk7Q0FDWCIsImZpbGUiOiJzdGRpbiIsInNvdXJjZXNDb250ZW50IjpbIlxuYSB7XG5iYWNrZ3JvdW5kIDogbGluZWFyLWdyYWRpZW50KHRvIHRvcCwgYmxhY2ssIHdoaXRlKTtcbmRpc3BsYXkgOiBmbGV4XG59XG46OnBsYWNlaG9sZGVyIHtcbmNvbG9yIDogI2NjY1xufSJdfQ== */
这样就完成了
这样我们就能够通过指令 flask  assets --help 来查看其使用方法了:
项目地址: https://github.com/Steinkuo/flask-autoprefixer.git
(venv) ➜ flask assets --help
Usage: flask assets [OPTIONS] COMMAND [ARGS]...
 
  Web assets commands.
 
Options:
  --help  Show this message and exit.
 
Commands:
  build  Build bundles.
  clean  Clean bundles.
  watch  Watch bundles for file changes.
