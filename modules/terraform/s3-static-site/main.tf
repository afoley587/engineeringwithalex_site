resource "aws_s3_bucket" "static-site" {
  bucket        = var.domain_website
  acl           = "public-read"
  force_destroy = var.force_destroy

  policy = var.policy_json
  website {
    index_document = var.index_document
    error_document = var.error_document
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  dynamic "logging" {
    for_each = var.logging_configs
    content {
      target_bucket = logging.value["bucket_id"]
      target_prefix = logging.value["prefix"]
    }
  }

  tags = merge(
    var.tags,
    { domain = var.domain_website }
  )

}

locals {
  source_ips = join("\", \"", var.source_ip_list)
}

