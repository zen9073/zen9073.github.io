# webdav
FROM base

# 安装 nginx 和 dav 扩展模块
RUN set -x \
    && apt update \
    && apt install -y --no-install-recommends nginx-light libnginx-mod-http-dav-ext \
    && apt clean \
    && rm -fr /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY etc /etc

EXPOSE 7000

COPY --chmod=0755 entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]

COPY s6 /s6
CMD ["/bin/s6-svscan", "/s6"]
