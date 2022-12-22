include MakefileHelp.mk

ETCD_VERSION?=v3.5.6
ETCD_DOWNLOAD_URL?=https://github.com/etcd-io/etcd/releases/download
ETCD_PROTO_SOURCE_URL?=https://raw.githubusercontent.com/etcd-io/jetcd/main/jetcd-grpc/src/main/proto/

.etcd:  ## installs etcd locally for running
	@mkdir -p .etcd
ifeq ($(shell uname -s),Linux)
	@curl -L -s \
		$(ETCD_DOWNLOAD_URL)/$(ETCD_VERSION)/etcd-$(ETCD_VERSION)-linux-amd64.tar.gz \
		| tar xz -C .etcd
	@mv .etcd/etcd-$(ETCD_VERSION)-linux-amd64/* .etcd/
	@rm -r .etcd/etcd-$(ETCD_VERSION)-linux-amd64
else ifeq ($(shell uname -s),Darwin)
	@curl -L -s \
		$(ETCD_DOWNLOAD_URL)/$(ETCD_VERSION)/etcd-$(ETCD_VERSION)-darwin-amd64.zip \
		-o .etcd/etcd-$(ETCD_VERSION)-darwin-amd64.zip
	@unzip -q -d .etcd .etcd/etcd-$(ETCD_VERSION)-darwin-amd64.zip
	@mv .etcd/etcd-$(ETCD_VERSION)-darwin-amd64/* .etcd/
	@rm -r .etcd/etcd-$(ETCD_VERSION)-darwin-amd64
	@rm .etcd/etcd-$(ETCD_VERSION)-darwin-amd64.zip
endif

start:  ## starts etcd
	@ETCD_VERSION=$(ETCD_VERSION) \
		docker stack deploy \
			--compose-file docker-compose.yml \
			etcd
	@docker run --rm \
		-v /var/run/docker.sock:/var/run/docker.sock \
	    sudobmitch/docker-stack-wait:latest \
	    etcd
.PHONY: start

stop:  ## stops etcd
	@docker stack rm etcd
.PHONY: stop

install: ## install local development dependencies
	@poetry install
.PHONY: install

uninstall: ## uninstalls local development dependencies
	@if [ -d .venv ]; then rm -rf .venv; fi
.PHONY: uninstall

clean: ## removes intermediate files and build artifacts
	@if [ -d .etcd ]; then rm -rf .etcd; fi
	@if [ -d .mypy_cache ]; then rm -rf .mypy_cache; fi
	@if [ -d .pytest_cache ]; then rm -rf .pytest_cache; fi
	@if [ -d .hypothesis ]; then rm -rf .hypothesis; fi
	@if [ -f .coverage ]; then rm .coverage; fi
	@if [ -d dist ]; then rm -rf dist; fi
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -delete
.PHONY: clean

lint:  ## lints all code
	@poetry run flake8
	@poetry run mypy etcd3 tests
.PHONY: lint

test: .etcd  ## runs the tests
	@PATH="$(PWD)/.etcd:$(PATH)"; \
		TEST_ETCD_VERSION="$(ETCD_VERSION)" \
		ETCDCTL_ENDPOINTS="http://localhost:2379,http://localhost:2380,http://localhost:2381" \
		poetry run pytest --cov -v
.PHONY: test

build:  ## builds the project to tar & wheel formats
	@poetry build
.PHONY: build

etcd3/etcdrpc:  ## generates etcd protobuf definitions
	@mkdir -p etcd3/etcdrpc
	@curl -L -s $(ETCD_PROTO_SOURCE_URL)/auth.proto -o etcd3/etcdrpc/auth.proto
	@curl -L -s $(ETCD_PROTO_SOURCE_URL)/kv.proto -o etcd3/etcdrpc/kv.proto
	@curl -L -s $(ETCD_PROTO_SOURCE_URL)/rpc.proto -o etcd3/etcdrpc/rpc.proto
	@sed -i -e 's\import "auth.proto"\import "etcd3/etcdrpc/auth.proto"\g' etcd3/etcdrpc/rpc.proto
	@sed -i -e 's\import "kv.proto"\import "etcd3/etcdrpc/kv.proto"\g' etcd3/etcdrpc/rpc.proto
	@poetry run python -m grpc.tools.protoc \
		-I . \
		--python_out=. \
		--grpc_python_out=. \
		--mypy_out=quiet:. \
		--mypy_grpc_out=quiet:. \
		$(shell find ./etcd3 -type f -name '*.proto')
.PHONY: etcd3/etcdrpc
