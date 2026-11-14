# infra/backend.hcl
bucket       = "tfstate-calculadora-scadavidzea"
key          = "calculadora/terraform.tfstate"
region       = "us-east-1"
use_lockfile = true
