build:
	docker buildx build --tag foodeas/afraid-autologin:latest .
build-push:
	docker buildx build --push --tag foodeas/afraid-autologin:latest .
