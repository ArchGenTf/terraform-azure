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

variable "servicebus_namespace_name" {
  type        = string
  description = "The globally unique name of the Service Bus namespace."
}
