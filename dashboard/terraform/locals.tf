locals {
  domain_name = "dash.engineeringwithalex.io"
  acm_certs   = toset([data.aws_acm_certificate.issued.arn])
  tags        = {
    enabled         = true
    orgname         = "afoley"
    application     = "dash"
    service         = "s3"
  }
}