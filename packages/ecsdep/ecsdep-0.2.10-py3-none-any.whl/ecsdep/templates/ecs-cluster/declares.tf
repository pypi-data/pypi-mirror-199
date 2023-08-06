terraform {
  required_version = ">= 1.1.2"
  backend "s3" {
    bucket  = "states-data.sycbas"
    key     = "terraform/ecs-cluster/sycbas-ai/terraform.tfstate"
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

variable "instance_type" {
  default = "t3.small"
}

variable "ami" {
  default = "amzn2-ami-ecs-hvm-*-x86_64-*"
}

variable "cors_hosts" {
  default = []
}

variable "cert_name" {
  default = "ai.sycbas.com"
}

variable "public_key_file" {
  default = "/app/sycbas/building-control/dep/sycbas.pub"
}

variable "autoscale" {
  default = {
    desired = 2
    min = 2
    max = 3
    cpu = 75
    memory = 75
    target_capacity = 0
  }
}

variable "az_count" {
  default = 3
}

variable "task_iam_policies" {
  default = ["arn:aws:iam::aws:policy/AmazonS3FullAccess"]
}

variable "vpc" {
  default = {
    cidr_block = ""
    octet3s = [10, 20, 30]
    peering_vpc_ids = []
  }
}