# base
FROM ubuntu:24.04 

# 设置非交互式
ARG DEBIAN_FRONTEND=noninteractive

# 使用中国时区
ENV TZ=Asia/Shanghai

# 使用国内源
RUN sed -i 's/[a-z]*\.[a-z]*\.[a-z]*/repo.huaweicloud.com/' /etc/apt/sources.list.d/ubuntu.sources

# 安装常用基础工具
RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    ca-certificates curl dirmngr gnupg gosu htop netcat net-tools s6 tzdata vim wget \
    && apt-get clean \
    && rm -fr /var/lib/apt/lists/* /tmp/* /var/tmp/*

# htop 配置
RUN set -x \
    && mkdir -p ~/.config/htop \
    && echo >> ~/.config/htop/htoprc "tree_view=1" \
    && echo >> ~/.config/htop/htoprc "shadow_other_users=1" \
    && echo >> ~/.config/htop/htoprc "hide_kernel_threads=1" \
    && echo >> ~/.config/htop/htoprc "hide_userland_threads=1"

# vim 配置
RUN set -x \
    && echo >> ~/.vimrc "syntax on" \
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

CMD ["/bin/bash"]
