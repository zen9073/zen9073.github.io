FROM ubuntu

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai

RUN set -x && apt update && apt install -y --no-install-recommends \
    ca-certificates curl dirmngr gnupg gosu htop netcat-openbsd net-tools s6 tzdata vim wget \
    && apt clean \
    && rm -fr /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN set -x && mkdir -p ~/.config/htop \
    && echo >> ~/.config/htop/htoprc "tree_view=1" \
    && echo >> ~/.config/htop/htoprc "tree_view_always_by_pid=1"

RUN set -x && echo >> ~/.vimrc "syntax on" \
    && echo >> ~/.vimrc "hi Comment ctermfg=6" \
    && echo >> ~/.vimrc "let loaded_matchparen=1" \
    && echo >> ~/.vimrc "set encoding=utf-8" \
    && echo >> ~/.vimrc "set tabstop=4" \
    && echo >> ~/.vimrc "set softtabstop=4" \
    && echo >> ~/.vimrc "set expandtab" \
    && echo >> ~/.vimrc "set ruler" \
    && echo >> ~/.vimrc "set showcmd" \
    && echo >> ~/.vimrc "set showmatch" \ 
    && echo >> ~/.vimrc "set hlsearch" \
    && echo >> ~/.vimrc "set incsearch"

RUN set -x && apt update && apt install -y --no-install-recommends \
    apache2-utils squid-openssl squid-langpack \
    && apt clean \
    && rm -fr /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY squid.conf /etc/squid/squid.conf
WORKDIR /etc/squid

COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]

COPY s6 /s6
CMD ["/bin/s6-svscan", "/s6"]
