variable "aws_region" {
  default = "us-east-1"
}

variable "slack_bot_token" {
  type      = string
  sensitive = true
}

variable "slack_signing_secret" {
  type      = string
  sensitive = true
}

variable "slack_app_token" {
  type      = string
  sensitive = true
}

variable "subnet_ids" {
  type = list(string)
}
