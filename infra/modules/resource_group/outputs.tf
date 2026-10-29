output "resource_group_data" {
  value = {
    for rg_key, rg in azurerm_resource_group.rg :
    rg_key => {
      name     = rg.name
      location = rg.location
      id       = rg.id
    }
  }
}
