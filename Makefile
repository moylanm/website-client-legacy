# Include variables from .envrc
include .envrc

# ==================================================================================== #
# HELPERS
# ==================================================================================== #

## help: print this help message
.PHONY: help
help:
	@printf 'Usage:\n'
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' | sed -e 's/^/ /'

# ==================================================================================== #
# DEVELOPMENT
# ==================================================================================== #

# run/local: run the application, pointing to localhost
.PHONY: run/local
run/local:
	@go run ./cmd/gui -admin-username=${LOCAL_USERNAME} -admin-password=${LOCAL_PASSWORD}

# run/remote: run the application, pointing to production
.PHONY: run/remote
run/remote:
	@go run ./cmd/gui -server-host='mylesmoylan.net' -server-port=443 -admin-username=${REMOTE_USERNAME} -admin-password=${REMOTE_PASSWORD}

# ==================================================================================== #
# QUALITY CONTROL
# ==================================================================================== #

## audit: tidy dependencies and format, vet, and test all code
.PHONY: audit
audit: vendor
	@printf 'Formatting code...\n'
	go fmt ./...
	@printf 'Vetting code...\n'
	go vet ./...
	staticcheck ./...
	@printf 'Running tests...\n'
	go test -race -vet=off ./...

## vendor: tidy and vendor dependencies
.PHONY: vendor
vendor:
	@printf 'Tidying and verifying module dependencies...\n'
	go mod tidy
	go mod verify
	@printf 'Vendoring dependencies...\n'
	go mod vendor

# ==================================================================================== #
# BUILD
# ==================================================================================== #

## build/api: build the cmd/api application
.PHONY: build/api
build/api:
	@printf 'Building cmd/api...\n'
	go build -ldflags='-s -w' -o=./bin/api ./cmd/api

