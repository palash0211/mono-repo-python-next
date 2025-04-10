output "api_endpoint" {
  description = "API endpoint URL"
  value       = aws_lb.api.dns_name
}

