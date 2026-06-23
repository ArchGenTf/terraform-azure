variable "subscription_id" {
  description = "The Azure Subscription ID."
  type        = string
}

variable "tenant_id" {
  description = "The Azure AD Tenant ID."
  type        = string
}

variable "resource_group_name" {
  description = "The name of the Resource Group to create."
  type        = string
  default     = "rg-archgen-prod"
}

variable "location" {
  description = "The Azure region for prod resources."
  type        = string
  default     = "centralus"
}

variable "environment" {
  description = "The environment name."
  type        = string
  default     = "prod"
}

variable "storage_account_name" {
  description = "The globally unique name of the Azure Storage Account."
  type        = string
}

variable "acr_name" {
  description = "The globally unique name of the Azure Container Registry."
  type        = string
}

variable "keyvault_name" {
  description = "The globally unique name of the Azure Key Vault."
  type        = string
}

variable "cosmos_account_name" {
  description = "The globally unique name of the Cosmos DB account."
  type        = string
}

variable "cluster_name" {
  description = "The name of the AKS cluster."
  type        = string
  default     = "aks-archgen-prod"
}

variable "admin_password" {
  description = "The administrator password for the jumpbox VM."
  type        = string
  sensitive   = true
}

variable "hub_vnet_address_space" {
  description = "The address space for the Hub VNet."
  type        = list(string)
}

variable "spoke_vnet_address_space" {
  description = "The address space for the Spoke VNet."
  type        = list(string)
}

variable "bastion_subnet_prefix" {
  description = "The address prefix for the Bastion subnet."
  type        = list(string)
}

variable "vm_subnet_prefix" {
  description = "The address prefix for the Jumpbox VM subnet."
  type        = list(string)
}

variable "appgw_subnet_prefix" {
  description = "The address prefix for the App Gateway subnet."
  type        = list(string)
}

variable "aks_subnet_prefix" {
  description = "The address prefix for the AKS subnet."
  type        = list(string)
}

variable "endpoint_subnet_prefix" {
  description = "The address prefix for the Endpoints subnet."
  type        = list(string)
}

variable "bastion_sku" {
  description = "The SKU of the Bastion Host."
  type        = string
}

variable "bastion_tunneling_enabled" {
  description = "Enable tunneling for the Bastion Host."
  type        = bool
}

variable "aks_dns_prefix" {
  description = "The DNS prefix for the AKS cluster."
  type        = string
}

variable "aks_kubernetes_version" {
  description = "The Kubernetes version for the AKS cluster."
  type        = string
}

variable "aks_node_count" {
  description = "The node count for the AKS default node pool."
  type        = number
}

variable "aks_node_size" {
  description = "The VM size for the AKS default node pool nodes."
  type        = string
}
