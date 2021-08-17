data "aws_route53_zone" "route53_zone" {
  name         = "engineeringwithalex.io"
}

data "aws_acm_certificate" "issued" {
  domain   = "engineeringwithalex.io"
  statuses = ["ISSUED"]
}