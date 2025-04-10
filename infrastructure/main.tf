terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC and Networking
module "vpc" {
  source = "./modules/vpc"
  
  vpc_cidr        = var.vpc_cidr
  azs             = var.availability_zones
  private_subnets = var.private_subnets
  public_subnets  = var.public_subnets
}

# Database
module "database" {
  source = "./modules/database"
  
  vpc_id            = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  db_name           = var.db_name
  db_username       = var.db_username
  db_password       = var.db_password
}

# Backend API
module "backend" {
  source = "./modules/backend"
  
  vpc_id            = module.vpc.vpc_id
  public_subnet_ids = module.vpc.public_subnet_ids
  db_host           = module.database.db_host
  db_name           = var.db_name
  db_username       = var.db_username
  db_password       = var.db_password
}

# Frontend
module "frontend" {
  source = "./modules/frontend"
  
  api_endpoint = module.backend.api_endpoint
}

