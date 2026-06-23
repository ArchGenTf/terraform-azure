variable "resource_group_name" {
  description = "The name of the resource group."
  type        = string
}

variable "location" {
  description = "The Azure region."
  type        = string
}

variable "environment" {
  description = "The environment name."
  type        = string
}

variable "bastion_subnet_id" {
  description = "The ID of the AzureBastionSubnet."
  type        = string
}

variable "vm_subnet_id" {
  description = "The ID of the subnet where the jumpbox VM will be deployed."
  type        = string
}

variable "vm_size" {
  description = "The virtual machine size (SKU)."
  type        = string
  default     = "Standard_D2lds_v6"
}

variable "admin_username" {
  description = "The administrator username for the jumpbox VM."
  type        = string
  default     = "praveen"
}

variable "admin_password" {
  description = "The administrator password for the jumpbox VM. Must be at least 12 characters."
  type        = string
  sensitive   = true
}

variable "sku" {
  description = "The SKU of the Bastion Host."
  type        = string
  default     = "Basic"
}

variable "tunneling_enabled" {
  description = "Enable tunneling for the Bastion Host."
  type        = bool
  default     = false
}

