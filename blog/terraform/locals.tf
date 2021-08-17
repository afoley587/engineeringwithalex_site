locals {
  domain_name = "blog.engineeringwithalex.io"
  acm_certs   = toset([data.aws_acm_certificate.issued.arn])
  tags        = {
    enabled         = true
    orgname         = "afoley"
    application     = "blog"
    service         = "s3"
  }
}