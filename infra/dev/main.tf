module "resource_group" {
  source         = "../modules/resource_group"
  resource_group = var.rgs
}
module "container_registry" {
  source = "../modules/container_registry"
  container_registry = {
    for acr_key, acr in var.container_registry :
    acr_key => {
      name                = acr.name
      resource_group_name = module.resource_group.resource_group_data[acr.resource_group_key].name
      location            = module.resource_group.resource_group_data[acr.resource_group_key].location
      sku                 = acr.sku
      admin_enabled       = acr.admin_enabled
    }

  }
}