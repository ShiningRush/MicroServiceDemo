IMAGE_NAME = fm-dnsmasq
CURRENT_VERSION := `head -1 releaselog `

init:
	# 为kong和它相关联的容器创建一个网络，便于通信
	docker network create kong-net

    # 拉取网关镜像
	docker pull dockerhub.followme.com/deploy/fm-dnsmasq:last

    # run
    docker run --name fm-dnsmasq --network=kong-net --ip 172.20.0.10 -d -e "ENV=dev" --cap-add=NET_ADMIN dockerhub.followme.com/deploy/fm-dnsmasq:last


build:
	docker build --build-arg build=build --rm -t $(IMAGE_NAME):$(CURRENT_VERSION) .
	docker tag $(IMAGE_NAME):$(CURRENT_VERSION) $(DH_URL)$(IMAGE_NAME):$(CURRENT_VERSION)
	docker login -u $(DH_USER) -p $(DH_PASS) $(DH_URL) && docker push $(DH_URL)$(IMAGE_NAME):$(CURRENT_VERSION)

.PHONY: init build