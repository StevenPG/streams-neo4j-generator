podman build app1 -f app1/Dockerfile -t app1:latest;
podman build app2 -f app2/Dockerfile -t app2:latest;
podman build app3 -f app3/Dockerfile -t app3:latest;
docker-compose up -d