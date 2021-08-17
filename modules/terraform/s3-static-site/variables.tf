variable "domain_website" {
  default     = "example.com"
  description = "Top level domain name of the website to deploy to, eg website.com"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = ""
}

variable "enabled" {
  type        = bool
  default     = true
  description = ""
}

variable "index_document" {
  default = "index.html"
}

variable "error_document" {
  default = "error.html"
}

variable "source_ip_list" {
  default = ["127.0.0.1/32"]
  type    = list(any)
}

variable "logging_configs" {
  default     = []
  type        = list(any)
  description = "Enable AWS Logging Buckets"
}

variable "force_destroy" {
  type        = bool
  default     = false
  description = "A boolean string that indicates all objects should be deleted from the bucket so that the bucket can be destroyed without error. These objects are not recoverable"
}

variable "policy_json" {}