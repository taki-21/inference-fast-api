help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

create_s3: ## Create s3 bucket.
	aws cloudformation create-stack \
	--stack-name sample-detection-s3 \
	--template-body file://cloudformation/s3.yml \
	--capabilities CAPABILITY_NAMED_IAM \
	--profile taki

create_acm: ## Create acm.
	aws cloudformation create-stack \
  --stack-name sample-detection-acm \
  --template-body file://cloudformation/acm.yml \
  --capabilities CAPABILITY_NAMED_IAM \
	--profile taki

create_worker: ## Create worker of Elastic Beanstalk.
	aws cloudformation create-stack \
  --stack-name sample-detection-worker \
  --template-body file://cloudformation/worker.yml \
  --capabilities CAPABILITY_NAMED_IAM \
	--profile taki
