output "servicebus_namespace_name" {
  value = azurerm_servicebus_namespace.sb.name
}

output "servicebus_primary_connection_string" {
  value     = azurerm_servicebus_namespace_authorization_rule.rule.primary_connection_string
  sensitive = true
}
