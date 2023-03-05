variable "crawler_lambda_name" {
  description = "Name of Lambda that will contain the Flight Crawler code"
  type        = string
  default     = "flights-crawler"
}

variable "crawler_ecr_name" {
  description = "Name of ECR repo that will contain the Flight Crawler code"
  type        = string
  default     = "flights-crawler"
}

variable "crawler_role_name" {
  description = "Name of the IAM Role and IAM Policy for the Flight Crawler Lambda"
  type        = string
  default     = "flights-crawler"
}

variable "crawler_timeout" {
  description = "Lambda timeout of the Flight Crawler Lambda"
  type        = number
  default     = 120
}

variable "crawler_memory_size" {
  description = "Memory size of the Flight Crawler Lambda"
  type        = number
  default     = 512
}

variable "manager_lambda_name" {
  description = "Name of Lambda that will contain the Flight Manager code"
  type        = string
  default     = "flights-manager"
}

variable "manager_ecr_name" {
  description = "Name of ECR repo that will contain the Flight Manager code"
  type        = string
  default     = "flights-manager"
}

variable "manager_role_name" {
  description = "Name of the IAM Role for the Flight Manager Lambda"
  type        = string
  default     = "flights-manager"
}

variable "manager_timeout" {
  description = "Lambda timeout of the Flight Manager Lambda"
  type        = number
  default     = 60
}

variable "manager_memory_size" {
  description = "Memory size of the Flight Manager Lambda"
  type        = number
  default     = 128
}

variable "database_secrets_name" {
  description = "Name of the secrets containing DB credentials"
  type        = string
  default     = "flights-crawler-database"
}
