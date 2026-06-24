# User-Assigned Managed Identity for the AKS Control Plane
resource "azurerm_user_assigned_identity" "aks" {
  name                = "identity-aks-controlplane-${var.environment}"
  resource_group_name = var.resource_group_name
  location            = var.location

  tags = {
    Environment = var.environment
  }
}

# Private AKS Cluster
resource "azurerm_kubernetes_cluster" "aks" {
  name                    = var.cluster_name
  location                = var.location
  resource_group_name     = var.resource_group_name
  dns_prefix              = var.dns_prefix
  kubernetes_version      = var.kubernetes_version
  private_cluster_enabled = true

  # Enable Workload Identity & OIDC Issuer
  oidc_issuer_enabled       = true
  workload_identity_enabled = true

  default_node_pool {
    name            = "default"
    node_count      = var.node_count
    vm_size         = var.node_size
    os_disk_size_gb = 50
    vnet_subnet_id  = var.aks_subnet_id

    # Required for Azure CNI
    type = "VirtualMachineScaleSets"

    upgrade_settings {
      max_surge                     = "10%"
      drain_timeout_in_minutes      = 0
      node_soak_duration_in_minutes = 0
    }
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.aks.id]
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
    outbound_type     = "loadBalancer"
  }

  # AGIC Addon Integration
  ingress_application_gateway {
    subnet_id    = var.appgw_subnet_id
    gateway_name = "appgw-agic-${var.environment}"
  }

  monitor_metrics {
    annotations_allowed = null
    labels_allowed      = null
  }

  tags = {
    Environment = var.environment
  }
}

resource "azurerm_monitor_workspace" "amw" {
  name                = "amw-${var.cluster_name}"
  resource_group_name = var.resource_group_name
  location            = var.location
  tags = {
    Environment = var.environment
  }
}

resource "azurerm_dashboard_grafana" "grafana" {
  name                = "grafana-${var.environment}"
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = "Standard"
  identity {
    type = "SystemAssigned"
  }
  azure_monitor_workspace_integrations {
    resource_id = azurerm_monitor_workspace.amw.id
  }
  tags = {
    Environment = var.environment
  }
}

resource "azurerm_role_assignment" "grafana_monitoring_reader" {
  scope                = azurerm_monitor_workspace.amw.id
  role_definition_name = "Monitoring Data Reader"
  principal_id         = azurerm_dashboard_grafana.grafana.identity[0].principal_id
}

resource "azurerm_monitor_data_collection_endpoint" "dce" {
  name                = "dce-${var.cluster_name}"
  resource_group_name = var.resource_group_name
  location            = var.location
  kind                = "Linux"
}

resource "azurerm_monitor_data_collection_rule" "prometheus_dcr" {
  name                        = "dcr-prometheus-${var.cluster_name}"
  resource_group_name         = var.resource_group_name
  location                    = var.location
  data_collection_endpoint_id = azurerm_monitor_data_collection_endpoint.dce.id
  kind                        = "Linux"

  data_sources {
    prometheus_forwarder {
      name    = "PrometheusDataSource"
      streams = ["Microsoft-PrometheusMetrics"]
    }
  }

  destinations {
    monitor_account {
      monitor_account_id = azurerm_monitor_workspace.amw.id
      name               = "MonitoringAccount"
    }
  }

  data_flow {
    streams      = ["Microsoft-PrometheusMetrics"]
    destinations = ["MonitoringAccount"]
  }
}

resource "azurerm_monitor_data_collection_rule_association" "aks_prometheus_association" {
  name                    = "assoc-prometheus-${var.cluster_name}"
  target_resource_id      = azurerm_kubernetes_cluster.aks.id
  data_collection_rule_id = azurerm_monitor_data_collection_rule.prometheus_dcr.id
}

resource "azurerm_monitor_data_collection_rule_association" "aks_dce_association" {
  name                        = "assoc-dce-${var.cluster_name}"
  target_resource_id          = azurerm_kubernetes_cluster.aks.id
  data_collection_endpoint_id = azurerm_monitor_data_collection_endpoint.dce.id
}
