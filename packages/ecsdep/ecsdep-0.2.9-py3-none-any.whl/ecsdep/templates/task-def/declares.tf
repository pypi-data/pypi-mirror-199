terraform {
  required_version = ">= 1.1.2"
  backend "s3" {
    bucket  = "states-data.sycbas"
    key     = "terraform/ecs-cluster/sycbas-ai/task-def/fetchd/terraform.tfstate"
    region  = "ap-northeast-2"
    encrypt = true
    acl     = "bucket-owner-full-control"
  }
}

provider "aws" {
  region  = "ap-northeast-2"
}

variable "template_version" {
  default = "1.1"
}

variable "cluster_name" {
  default = "sycbas-ai"
}

# variables -----------------------------------------------
variable "awslog_region" {
  default = "ap-northeast-2"
}

variable "stages" {
  default = {
    default = {
        env_service_stage = "production"
        service_name = "fetchd"
        task_definition_name = "fetchd"
    }
  }
}

variable "service_auto_scaling" {
  default = {
    desired = 1
    min = 1
    max = 1
    cpu = 0
    memory = 0
  }
}

variable "deployment_strategy" {
  default = {
    minimum_healthy_percent = 100
    maximum_percent = 200
  }
}

variable "exposed_container" {
  default = []
}

variable "target_group" {
  default = {
    protocol = "HTTP"
    healthcheck = {
        path = "/"
        timeout = 10
        interval = 60
        healthy_threshold = 2
        unhealthy_threshold = 10
        matcher = "200,301,302,404"
    }
  }
}

variable "loggings" {
  default = ["sycbas-fetchd"]
}

variable "loadbalancing_pathes" {
  default = ["/*"]
}

variable "requires_compatibilities" {
  default = ["EC2"]
}

variable "service_resources" {
  default = {
    memory = 360
    cpu = 360
  }
}

variable "vpc_name" {
  default = ""
}