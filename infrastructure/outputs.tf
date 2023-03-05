output "crawler_repo_url" {
  description = "The URL of the repository (in the form aws_account_id.dkr.ecr.region.amazonaws.com/repositoryName)"
  value       = aws_ecr_repository.crawler.repository_url
}

output "crawler_lambda_arn" {
  description = "ARN of the Flight Crawler Lambda"
  value       = aws_lambda_function.crawler.arn
}

output "manager_repo_url" {
  description = "The URL of the repository (in the form aws_account_id.dkr.ecr.region.amazonaws.com/repositoryName)"
  value       = aws_ecr_repository.manager.repository_url
}

output "manager_lambda_arn" {
  description = "ARN of the Flight Manager Lambda"
  value       = aws_lambda_function.manager.arn
}
