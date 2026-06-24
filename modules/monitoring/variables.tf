variable "resource_group_name" {
  type        = string
  description = "The name of the resource group."
}

variable "location" {
  type        = string
  description = "The Azure region."
}

variable "environment" {
  type        = string
  description = "The environment name."
}

variable "slack_webhook_url" {
  type        = string
  description = "The Slack webhook URL for alerts."
}

variable "aks_cluster_id" {
  type        = string
  description = "The Resource ID of the AKS cluster."
}
