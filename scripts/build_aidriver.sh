#!/bin/bash
set -o allexport
source ./.env
set +o allexport

cd ./ai_driver

IMAGE_NAME="fearnworks/aidriver"
RELEASE_TAG="$IMAGE_NAME:release"

GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
GIT_COMMIT=$(git rev-parse --short HEAD)

# Authenticate with the GitHub Container Registry
echo "$REG_TOKEN" | docker login ghcr.io -u USERNAME --password-stdin

# Authenticate with Docker Hub
echo "$DOCKER_HUB_PASSWORD" | docker login -u $DOCKER_HUB_USERNAME --password-stdin

docker pull "$RELEASE_TAG" || true
docker build -t "$IMAGE_NAME:$GIT_BRANCH" \
-t "$IMAGE_NAME:$GIT_COMMIT"  \
--label git-commit=$GIT_COMMIT \
--label git-branch=$GIT_BRANCH \
--build-arg BUILDKIT_INLINE_CACHE=1 \
--cache-from=$RELEASE_TAG .

# Security scanners:
trivy image --ignore-unfixed --exit-code 1 \
$IMAGE_NAME:$GIT_BRANCH

docker push "$IMAGE_NAME:$GIT_BRANCH"
docker push "$IMAGE_NAME:$GIT_COMMIT"

# Push to Docker Hub
docker push "$IMAGE_NAME:$GIT_BRANCH"
docker push "$IMAGE_NAME:$GIT_COMMIT"
