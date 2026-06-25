terraform {
  backend "s3" {
    bucket = "incident-bot-terraform-state"
    key    = "infra/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_dynamodb_table" "incidents" {
  name         = "incidents"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "incident_id"

  attribute {
    name = "incident_id"
    type = "S"
  }

  attribute {
    name = "status"
    type = "S"
  }

  global_secondary_index {
    name            = "status-index"
    hash_key        = "status"
    projection_type = "ALL"
  }

  tags = { Name = "incident-bot" }
}

resource "aws_ecs_cluster" "incident_bot" {
  name = "incident-bot"
}

resource "aws_ecs_task_definition" "bot" {
  family                   = "incident-bot"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn
  container_definitions = jsonencode([
    {
      name  = "bot"
      image = "ghcr.io/pkalab/incident-bot:latest"
      environment = [
        { name = "SLACK_BOT_TOKEN", value = var.slack_bot_token },
        { name = "SLACK_SIGNING_SECRET", value = var.slack_signing_secret },
        { name = "SLACK_APP_TOKEN", value = var.slack_app_token },
        { name = "DYNAMODB_TABLE", value = aws_dynamodb_table.incidents.name },
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/incident-bot"
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "bot"
        }
      }
    }
  ])
}

resource "aws_ecs_service" "bot" {
  name            = "incident-bot"
  cluster         = aws_ecs_cluster.incident_bot.id
  task_definition = aws_ecs_task_definition.bot.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.subnet_ids
    assign_public_ip = true
    security_groups = [aws_security_group.bot.id]
  }
}

resource "aws_security_group" "bot" {
  name        = "incident-bot-sg"
  description = "Allow outbound traffic for incident bot"
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_role" "ecs_execution" {
  name = "incident-bot-ecs-execution"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
  ]
}

resource "aws_iam_role" "ecs_task" {
  name = "incident-bot-ecs-task"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "dynamodb" {
  name = "incident-bot-dynamodb"
  role = aws_iam_role.ecs_task.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:Query",
        "dynamodb:Scan",
      ]
      Resource = aws_dynamodb_table.incidents.arn
    }]
  })
}
