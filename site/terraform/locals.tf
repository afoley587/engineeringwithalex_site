locals {
  domain_name = "engineeringwithalex.io"
  acm_certs   = toset([module.acm.arn])
  tags        = {
    enabled         = true
    orgname         = "afoley"
    application     = "web"
    service         = "s3"
  }
}