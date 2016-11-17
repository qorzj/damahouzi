mkdir -p static/js
mkdir -p static/css
mkdir -p static/fonts/roboto/
wget https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.8/css/materialize.min.css -O static/css/materialize.min.css
wget https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.8/fonts/roboto/Roboto-Regular.woff2 -O static/fonts/roboto/Roboto-Regular.woff2
wget https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.8/fonts/roboto/Roboto-Regular.woff -O static/fonts/roboto/Roboto-Regular.woff
wget https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.8/fonts/roboto/Roboto-Regular.ttf -O static/fonts/roboto/Roboto-Regular.ttf
wget https://code.jquery.com/jquery-3.1.1.min.js -O static/js/jquery-3.1.1.min.js
wget https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.8/js/materialize.min.js -O static/js/materialize.min.js
wget https://raw.githubusercontent.com/qorzj/builtins-proto/master/python-builtins.js -O static/js/python-builtins.js
wget https://raw.githubusercontent.com/qorzj/builtins-proto/master/python-format.js -O static/js/python-format.js