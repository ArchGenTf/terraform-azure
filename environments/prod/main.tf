resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location

  tags = {
    Environment = var.environment
  }
}

# Network Module (Hub-Spoke architecture)
module "network" {
  source                   = "../../modules/network"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  environment              = var.environment
  hub_vnet_address_space   = var.hub_vnet_address_space
  spoke_vnet_address_space = var.spoke_vnet_address_space
  bastion_subnet_prefix    = var.bastion_subnet_prefix
  vm_subnet_prefix         = var.vm_subnet_prefix
  appgw_subnet_prefix      = var.appgw_subnet_prefix
  aks_subnet_prefix        = var.aks_subnet_prefix
  endpoint_subnet_prefix   = var.endpoint_subnet_prefix
}

# Storage Account Module (TF State file host)
module "storage" {
  source               = "../../modules/storage"
  resource_group_name  = azurerm_resource_group.rg.name
  location             = azurerm_resource_group.rg.location
  environment          = var.environment
  storage_account_name = var.storage_account_name
  container_name       = "tfstate"
}

# Container Registry Module (Premium SKU for Private Endpoint)
module "acr" {
  source               = "../../modules/acr"
  resource_group_name  = azurerm_resource_group.rg.name
  location             = azurerm_resource_group.rg.location
  environment          = var.environment
  acr_name             = var.acr_name
  subnet_id            = module.network.endpoint_subnet_id
  private_dns_zone_ids = [module.network.acr_dns_zone_id]
}




# Key Vault Module
module "keyvault" {
  source               = "../../modules/keyvault"
  resource_group_name  = azurerm_resource_group.rg.name
  location             = azurerm_resource_group.rg.location
  environment          = var.environment
  keyvault_name        = var.keyvault_name
  subnet_id            = module.network.endpoint_subnet_id
  private_dns_zone_ids = [module.network.vault_dns_zone_id]
  tenant_id            = var.tenant_id
}

# Cosmos DB Module (MongoDB API)
module "cosmosdb" {
  source               = "../../modules/cosmosdb"
  resource_group_name  = azurerm_resource_group.rg.name
  location             = azurerm_resource_group.rg.location
  environment          = var.environment
  cosmos_account_name  = var.cosmos_account_name
  subnet_id            = module.network.endpoint_subnet_id
  private_dns_zone_ids = [module.network.cosmos_dns_zone_id]
}

# Bastion VM Host Module (Private Jumpbox Access)
module "bastion" {
  source              = "../../modules/bastion"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  environment         = var.environment
  bastion_subnet_id   = module.network.bastion_subnet_id
  vm_subnet_id        = module.network.vm_subnet_id
  sku                 = var.bastion_sku
  tunneling_enabled   = var.bastion_tunneling_enabled
  admin_password      = var.admin_password
}

# Private AKS Cluster with AGIC
module "aks" {
  source              = "../../modules/aks"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  environment         = var.environment
  cluster_name        = var.cluster_name
  dns_prefix          = var.aks_dns_prefix
  aks_subnet_id       = module.network.aks_subnet_id
  appgw_subnet_id     = module.network.appgw_subnet_id
  kubernetes_version  = var.aks_kubernetes_version
  node_count          = var.aks_node_count
  node_size           = var.aks_node_size
}

module "servicebus" {
  source                    = "../../modules/servicebus"
  resource_group_name       = azurerm_resource_group.rg.name
  location                  = azurerm_resource_group.rg.location
  environment               = var.environment
  servicebus_namespace_name = var.servicebus_namespace_name
}

module "monitoring" {
  source              = "../../modules/monitoring"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  environment         = var.environment
  slack_webhook_url   = var.slack_webhook_url
  aks_cluster_id      = module.aks.cluster_id
}
