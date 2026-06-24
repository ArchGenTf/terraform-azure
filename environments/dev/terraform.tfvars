subscription_id      = "65bf2554-8090-4538-9c38-8a6e9c5f6f22"
tenant_id            = "d8537334-bc24-4daf-95a8-bf4c9fb14394"
storage_account_name = "archgentfstate"
acr_name             = "acrarchgen"
keyvault_name        = "kvarchgen"
cosmos_account_name  = "cosmosarchgen"
admin_password       = "Praveen@1234"

# Network configurations
hub_vnet_address_space   = ["10.10.0.0/16"]
spoke_vnet_address_space = ["10.11.0.0/16"]
bastion_subnet_prefix    = ["10.10.1.0/26"]
vm_subnet_prefix         = ["10.10.2.0/27"]
appgw_subnet_prefix      = ["10.10.3.0/26"]
aks_subnet_prefix        = ["10.11.0.0/22"]
endpoint_subnet_prefix   = ["10.11.4.0/27"]

# Bastion configurations
bastion_sku               = "Standard"
bastion_tunneling_enabled = true

# AKS configurations
aks_dns_prefix         = "aks-archgen-dev-dns"
aks_kubernetes_version = "1.36"
aks_node_size          = "Standard_D2lds_v6"

# Service Bus & Slack Webhook Alert configurations
servicebus_namespace_name = "sbarchgendev"
grafana_name              = "grafana-archgen-dev"