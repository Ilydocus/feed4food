FROM grafana/grafana


COPY /datasource.yml /etc/grafana/provisioning/datasources/
COPY /dashboards.yml /etc/grafana/provisioning/dashboards/
COPY /scaphandre_dashboard.json /var/lib/grafana/dashboards/metrics/
COPY /node_dashboard.json /var/lib/grafana/dashboards/metrics/
COPY /django_dashboard.json /var/lib/grafana/dashboards/metrics/

