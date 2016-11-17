# preparations:
#   apt-get install uwsgi
#   apt-get install uwsgi-plugin-python
#   vim /etc/rc.local

/usr/bin/uwsgi --plugin python,http --http :8080 --wsgi-file index.py --chdir {workdir} -d {workdir}/uwsgi.log --touch-reload /tmp/uwsgi_reload
