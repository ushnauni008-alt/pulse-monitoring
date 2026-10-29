output "container_registry_data" {
  value = {
    for acr_key, acr in azurerm_container_registry.acr :
    acr_key => {
      name                = acr.name
      resource_group_name = acr.resource_group_name
      location            = acr.location
      sku                 = acr.sku
      admin_enabled       = acr.admin_enabled
      id                  = acr.id
      login_server        = acr.login_server
    }
  }
}