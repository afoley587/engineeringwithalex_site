terraform {
  required_version = ">= 1.1.9"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    key    = "site/engineeringwithalex.tfstate"
    region = "us-east-1"
    bucket = "afoley-terraform-state"
  }
}
