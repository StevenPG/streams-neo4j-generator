docker-compose down -v --remove-orphans
podman stop app1
podman stop app2
podman stop app3
podman rm app1
podman rm app2
podman rm app3



