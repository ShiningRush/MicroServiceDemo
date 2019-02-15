IMAGE_NAME = fm-kong-apigateway
CURRENT_VERSION := `head -1 releaselog `

init:
	# 为kong和它相关联的容器创建一个网络，便于通信
	docker network create kong-net --subnet=172.20.0.0/16
	# 创建pg作为kong的database
	docker run -d --name kong-database \
               --network=kong-net \
               -p 5432:5432 \
               -e "POSTGRES_USER=kong" \
               -e "POSTGRES_DB=kong" \
               postgres:9.6

    # 拉取dnsmasq镜像
	docker pull dockerhub.followme.com/deploy/fm-dnsmasq:v1.0

    # 运行dnsmasq
    docker run --name fm-dnsmasq --network=kong-net --ip 172.20.0.10 -d -e "ENV=dev" --cap-add=NET_ADMIN dockerhub.followme.com/deploy/fm-dnsmasq:v1.0

	# 使用kong的官方镜像在正式运行之前对pg进行数据结构迁移
	docker run --rm \
     --network=kong-net \
     -e "KONG_DATABASE=postgres" \
     -e "KONG_PG_HOST=kong-database" \
     kong:0.14.1 kong migrations up
	
    # 拉取网关镜像
    docker pull dockerhub.followme.com/deploy/fm-kong-apigateway:v1.0

	# 运行网关镜像
	docker run -d --name fm-kong-apigateway \
     --network=kong-net \
     -e "KONG_DATABASE=postgres" \
     -e "KONG_PG_HOST=kong-database" \
     -e "KONG_PROXY_ACCESS_LOG=/dev/stdout" \
     -e "KONG_ADMIN_ACCESS_LOG=/dev/stdout" \
     -e "KONG_PROXY_ERROR_LOG=/dev/stderr" \
     -e "KONG_ADMIN_ERROR_LOG=/dev/stderr" \
     -e "KONG_ADMIN_LISTEN=0.0.0.0:8001, 0.0.0.0:8444 ssl" \
	 -e "ENV=dev" \
     -p 8000:8000 \
     -p 8001:8001 \
     dockerhub.followme.com/deploy/fm-kong-apigateway:v1.0

     # kong dahsboard 需要配置一下挂载端口
     docker run -d --name fm-kong-dashboard --rm --network=kong-net -p 8080:8080 pgbi/kong-dashboard start --kong-url http://fm-kong-apigateway:8001

build:
	chmod +x ./custom-kong-entrypoint.sh
	docker build --no-cache --build-arg build=build --rm -t $(IMAGE_NAME):$(CURRENT_VERSION) .
	docker tag $(IMAGE_NAME):$(CURRENT_VERSION) $(DH_URL)$(IMAGE_NAME):$(CURRENT_VERSION)
	docker login -u $(DH_USER) -p $(DH_PASS) $(DH_URL) && docker push $(DH_URL)$(IMAGE_NAME):$(CURRENT_VERSION)

.PHONY: init build