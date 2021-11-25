

resource "azurerm_resource_group" "rg" {
  name     = "txtapprg"
  location = "West Europe"
}

resource "azurerm_container_registry" "acr" {
  name                = "txtappregistry"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = false
}


resource "azuredevops_project" "project" {
  name       = "txtconverter_comsas2"
  description        = "Creates a website that allows for cosmas2 search result .txt files to be converted into a table format for analytic uses"
}
