FROM debian:bookworm

RUN apt update
RUN apt install -y apache2 php libapache2-mod-php build-essential git

RUN apt install -y python3 python3-flask python3-lxml python3-nltk python3-mysqldb
RUN python3 -m nltk.downloader -d /usr/share/nltk_data punkt_tab
RUN python3 -m nltk.downloader -d /usr/share/nltk_data punkt

RUN apt install -y libarchive-dev cmake libz-dev
RUN cd /tmp && git clone https://github.com/SWI-Prolog/swipl.git -b V8.0.1 --depth 1 && cd swipl && git submodule update --init
RUN cd /tmp/swipl && mkdir build && cd build && cmake .. -DINSTALL_DOCUMENTATION=OFF -DX11_X11_INCLUDE_PATH=
RUN cd /tmp/swipl/build && make -j 4 && make install

RUN apt install -y xsltproc
RUN apt install -y default-jre-headless

VOLUME /langpro

RUN rm /etc/apache2/sites-enabled/*
COPY httpd.conf /etc/apache2/sites-enabled/langpro.conf

RUN a2enmod cgid proxy_http

RUN apt install -y tmux

EXPOSE 80
WORKDIR /langpro
CMD ["bash", "session.sh"]
