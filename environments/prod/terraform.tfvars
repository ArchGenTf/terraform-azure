subscription_id      = "65bf2554-8090-4538-9c38-8a6e9c5f6f22"
tenant_id            = "d8537334-bc24-4daf-95a8-bf4c9fb14394"
storage_account_name = "archgentfstateprod"
acr_name             = "acrarchgen"
keyvault_name        = "kvarchgenprod"
cosmos_account_name  = "cosmosarchgenprod"
admin_password       = "Praveen@1234"

# Network configurations
hub_vnet_address_space   = ["10.20.0.0/16"]
spoke_vnet_address_space = ["10.21.0.0/16"]
bastion_subnet_prefix    = ["10.20.1.0/26"]
vm_subnet_prefix         = ["10.20.2.0/27"]
appgw_subnet_prefix      = ["10.20.3.0/26"]
aks_subnet_prefix        = ["10.21.0.0/22"]
endpoint_subnet_prefix   = ["10.21.4.0/27"]

# Bastion configurations
bastion_sku               = "Standard"
bastion_tunneling_enabled = true

# AKS configurations
aks_dns_prefix         = "aks-archgen-prod-dns"
aks_kubernetes_version = "1.36"
aks_node_count         = 3
aks_node_size          = "Standard_D2lds_v6"