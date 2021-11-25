terraform {
  required_providers {
    snowflake = {
      source = "chanzuckerberg/snowflake"
      version = "0.25.22"
    }
  }
}

provider "snowflake"{
	username = var.snowflake_username
	account = var.snowflake_account
	region = "west-europe.azure"
  password = var.snowflake_password
}


resource "snowflake_warehouse" "appwh" {
	name           = "appwh"
	comment        = "created appwh"
	warehouse_size = "small"
	auto_resume = true
}

resource "snowflake_database" "txtappdb" {
	name = "txtappdb"
	comment = "created txtappdb"
	
}

resource "snowflake_schema" "schema" {
  database            = snowflake_database.txtappdb.name
  name                = "schema"
  data_retention_days = 1
}

resource "snowflake_sequence" "sequence" {
  database = snowflake_schema.schema.database
  schema   = snowflake_schema.schema.name
  name     = "sequence"
}

resource "snowflake_table" "table" {
  database            = snowflake_schema.schema.database
  schema              = snowflake_schema.schema.name
  name                = "example_table"
  comment             = "A table."
  data_retention_days = snowflake_schema.schema.data_retention_days
  change_tracking     = false

  column {
    name     = "id"
    type     = "NUMBER(38,0) NOT NULL AUTOINCREMENT CONSTRAINT WE_PK PRIMARY KEY"
  }
  column {
    name     = "docId"
    type     = "text"
  }
  column {
    name    = "Quelle"
    type    = "text"
  }
  column {
    name     = "Text"
    type     = "text"
  }
  column {
    name    = "Datum"
    type    = "text"
  }
  
  column {
    name    = "Titel"
    type    = "text"
  }
  column {
    name    = "Vorkommen"
    type    = "text"
  }
  column {
    name    = "Extra-Info"
    type    = "text"
  }
  column {
    name    = "Ressort"
    type    = "text"
  }
  column {
    name    = "Fachgebiet"
    type    = "text"
  }
}

