output "dynamodb_table" {
  value = aws_dynamodb_table.incidents.name
}

output "ecs_cluster" {
  value = aws_ecs_cluster.incident_bot.name
}

output "ecs_service" {
  value = aws_ecs_service.bot.name
}
