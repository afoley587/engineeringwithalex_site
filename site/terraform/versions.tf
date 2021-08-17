terraform {
  required_version = ">= 0.14"

  backend "s3" {
    key            = "site/engineeringwithalex.tfstate"
    region         = "us-east-1"
    bucket         = "afoley-terraform-state"
  }
}