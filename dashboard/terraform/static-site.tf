module "static-site" {
  source = "../../modules/terraform/s3-static-site"

  tags = local.tags

  domain_website = local.domain_name
  source_ip_list = ["0.0.0/0"]
  policy_json = data.aws_iam_policy_document.s3_bucket_policy.json

}

data "aws_iam_policy_document" "s3_bucket_policy" {
  statement {
    sid = "1"

    actions = [
      "s3:GetObject",
    ]

    resources = [
      "arn:aws:s3:::${local.domain_name}/*",
    ]

    principals {
      type = "AWS"

      identifiers = [
        aws_cloudfront_origin_access_identity.origin_access_identity.iam_arn,
      ]
    }
  }
}