resource "azurerm_monitor_action_group" "slack_action_group" {
  name                = "ag-slack-${var.environment}"
  resource_group_name = var.resource_group_name
  short_name          = "slackalerts"

  webhook_receiver {
    name                    = "slack-webhook"
    service_uri             = var.slack_webhook_url
    use_common_alert_schema = true
  }
}

resource "azurerm_monitor_metric_alert" "aks_node_ready_alert" {
  name                = "alert-aks-node-not-ready-${var.environment}"
  resource_group_name = var.resource_group_name
  scopes              = [var.aks_cluster_id]
  severity            = 1 # Error

  criteria {
    metric_namespace = "Microsoft.ContainerService/managedClusters"
    metric_name      = "kube_node_status_condition"
    aggregation      = "Total"
    operator         = "GreaterThanOrEqual"
    threshold        = 1

    dimension {
      name     = "status2"
      operator = "Include"
      values   = ["NotReady"]
    }
  }

  action {
    action_group_id = azurerm_monitor_action_group.slack_action_group.id
  }

  tags = {
    Environment = var.environment
  }
}
