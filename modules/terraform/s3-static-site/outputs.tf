output "bucket_domain_name" {
  value       = var.enabled ? join("", aws_s3_bucket.static-site.*.bucket_domain_name) : ""
  description = "FQDN of bucket"
}

output "bucket_regional_domain_name" {
  value       = var.enabled ? join("", aws_s3_bucket.static-site.*.bucket_regional_domain_name) : ""
  description = "The bucket region-specific domain name"
}

output "bucket_id" {
  value       = var.enabled ? join("", aws_s3_bucket.static-site.*.id) : ""
  description = "Bucket Name (aka ID)"
}

output "bucket_arn" {
  value       = var.enabled ? join("", aws_s3_bucket.static-site.*.arn) : ""
  description = "Bucket ARN"
}

output "enabled" {
  value       = var.enabled
  description = "Is module enabled"
}

output "bucket_website_endpoint" {
  value       = var.enabled ? join("", aws_s3_bucket.static-site.*.website_endpoint) : ""
  description = "Website endpoint"
}
