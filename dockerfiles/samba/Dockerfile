FROM base

# 安装 samba
RUN apt-get update \
    && apt-get install -y --no-install-recommends samba openssl \
    && rm -rf /var/lib/apt/lists/* 

# 删除默认配置文件
RUN sed -i \
    -e '172,999d' \
    -e 's/\(^\s*map to guest = bad user\)/#\1/' \
    /etc/samba/smb.conf \
    && echo >> /etc/samba/smb.conf "   socket options = IPTOS_LOWDELAY TCP_NODELAY" \
    && echo >> /etc/samba/smb.conf "   security = user" \
    && echo >> /etc/samba/smb.conf "[smb]" \
    && echo >> /etc/samba/smb.conf "   path = /mount" \
    && echo >> /etc/samba/smb.conf "   writeable = yes" \
    && echo >> /etc/samba/smb.conf "   guest ok = no" \
    && echo >> /etc/samba/smb.conf "   valid users = @sambashare"\
    && echo >> /etc/samba/smb.conf "   create mask = 0644" \
    && echo >> /etc/samba/smb.conf "   directory mask= 0755" \
    && echo >> /etc/samba/smb.conf "   force user = root" \
    && echo >> /etc/samba/smb.conf "   force group = root"

WORKDIR  /mount

# 暴露　smbd　端口
EXPOSE 445 139

COPY  entrypoint.sh /
RUN  chmod 0755 /entrypoint.sh 
ENTRYPOINT ["/entrypoint.sh"]

COPY s6 /s6
CMD ["/bin/s6-svscan", "/s6"]
