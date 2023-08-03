# Blackbox prober exporter

```yaml
scrape_configs:
  - job_name: "blackbox"
    metrics_path: /probe
    params:
      module: [http_2xx] # Look for a HTTP 200 response.
    static_configs:
      - targets:
          - http://prometheus.io # Target to probe with http.
          - https://prometheus.io # Target to probe with https.
          - http://example.com:8080 # Target to probe with http on port 8080.
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: 127.0.0.1:9115 # The blackbox exporter's real hostname:port.
```

首先获取 targets 实例的 **\_\_address\_\_** 值写进 **\_\_param_target**，**\_\_param_name** 形式的标签里的 **name** 和它的值会被添加到发送到黑盒的 http 的 header 的 params 当作键值。

然后获取 **\_\_param_target** 的值，并覆写到 **instance** 标签中。

最后覆写 Target 实例的 **\_\_address\_\_** 标签值为 BlockBox Exporter 实例的访问地址，向 127.0.0.1:9115 发送请求获取实例的 metrics 信息。
