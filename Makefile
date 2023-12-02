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

# run/gui: run the cmd/gui application
.PHONY: run/gui
run/gui:
	@go run ./cmd/gui -admin-username${ADMIN_USERNAME} -admin-password=${ADMIN_PASSWORD}

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
