resource "aws_route53_record" "route53_record" {
  for_each = toset([local.domain_name, "www.${local.domain_name}"])
  zone_id = data.aws_route53_zone.route53_zone.zone_id
  name    = each.key
  type    = "A"

  alias {
    name    = aws_cloudfront_distribution.s3_distribution.domain_name
    zone_id = aws_cloudfront_distribution.s3_distribution.hosted_zone_id
    evaluate_target_health = false
  }
}

module "acm" {
  source = "../../modules/terraform/acm-cert"
  domain_name                 = data.aws_route53_zone.route53_zone.name
  subject_alternative_names   = ["*.${data.aws_route53_zone.route53_zone.name}"]
  wait_for_certificate_issued = false
  zone_name                   = data.aws_route53_zone.route53_zone.name
}
