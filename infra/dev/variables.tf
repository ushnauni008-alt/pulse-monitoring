variable "rgs" {
  type = map(object({
    name        = string
    location    = string
    environment = string
  }))
}
variable "container_registry" {
  type = map(object({
    name               = string
    resource_group_key = string
    location           = string
    sku                = string
    admin_enabled      = bool
  }))
}