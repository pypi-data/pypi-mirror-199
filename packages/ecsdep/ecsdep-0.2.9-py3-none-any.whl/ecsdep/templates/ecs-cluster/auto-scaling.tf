# cluster auto scaling --------------------------------
resource "aws_autoscaling_group" "ecs_cluster" {
    vpc_zone_identifier  = var.vpc.cidr_block == "" ? toset(data.aws_subnets.default.ids) : [ for each in aws_subnet.public: each.id ]
    name                 = "ecs-${var.cluster_name}"
    min_size             = var.autoscale ["min"]
    max_size             = var.autoscale ["max"]
    desired_capacity     = var.autoscale ["desired"]
    health_check_type    = "EC2"
    # launch_configuration = aws_launch_configuration.host.name

    launch_template {
      id      = aws_launch_template.host.id
      version = "$Latest"
    }

    tag {
      key                 = "Name"
      value               = var.cluster_name
      propagate_at_launch = true
    }
    tag {
      key                 = "system"
      value               = var.cluster_name
      propagate_at_launch = true
    }
}

resource "aws_autoscaling_policy" "memory-reservation" {
  count = var.autoscale.memory > 0 ? 1 : 0
  name                   = "${var.cluster_name}-memory-reservation"
  policy_type            = "TargetTrackingScaling"
  adjustment_type        = "ChangeInCapacity"
  autoscaling_group_name = aws_autoscaling_group.ecs_cluster.name

  target_tracking_configuration {
    customized_metric_specification {
      metric_dimension {
        name  = "ClusterName"
        value = var.cluster_name
      }

      metric_name = "MemoryReservation"
      namespace   = "AWS/ECS"
      statistic   = "Average"
    }
    target_value = var.autoscale.memory
  }
}

# policy for service addition ---------------------------
resource "aws_autoscaling_policy" "cpu-tracking" {
  name                      = "${var.cluster_name}-cpu-tracking"
  policy_type               = "TargetTrackingScaling"
  adjustment_type           = "ChangeInCapacity"
  autoscaling_group_name    = aws_autoscaling_group.ecs_cluster.name

  target_tracking_configuration {
    customized_metric_specification {
      metric_dimension {
        name  = "ClusterName"
        value = var.cluster_name
      }

      metric_name = "CPUReservation"
      namespace   = "AWS/ECS"
      statistic   = "Average"
    }
    target_value = var.autoscale.cpu
  }
}

resource "aws_ecs_capacity_provider" "provider" {
  name = "${var.cluster_name}-capacity-provider"
  auto_scaling_group_provider {
    auto_scaling_group_arn = aws_autoscaling_group.ecs_cluster.arn

    managed_termination_protection = var.autoscale.cpu == 0 && var.autoscale.memory == 0 ? "ENABLED" : "DISABLED"
    managed_scaling {
      maximum_scaling_step_size = 1000
      minimum_scaling_step_size = 1
      status                    = var.autoscale.cpu == 0 && var.autoscale.memory == 0 ? "ENABLED" : "DISABLED"
      target_capacity           = 100
    }
  }
}

resource "aws_ecs_cluster_capacity_providers" "providers" {
  cluster_name = var.cluster_name
  capacity_providers = [aws_ecs_capacity_provider.provider.name]

  default_capacity_provider_strategy {
    base              = 1
    weight            = 100
    capacity_provider = aws_ecs_capacity_provider.provider.name
  }
}
