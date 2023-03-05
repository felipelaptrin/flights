##################
### ECR
##################
resource "aws_ecr_repository" "crawler" {
  name                 = var.crawler_ecr_name
  image_tag_mutability = "MUTABLE"
}

resource "aws_ecr_repository" "manager" {
  name                 = var.manager_ecr_name
  image_tag_mutability = "MUTABLE"
}

##################
### SECRETS
##################
resource "aws_secretsmanager_secret" "database" {
  name        = var.database_secrets_name
  description = "Stores credential of the Slack Bot."
}

resource "aws_secretsmanager_secret_version" "database" {
  secret_id     = aws_secretsmanager_secret.database.id
  secret_string = <<EOF
  {
    "CLUSTER_ID": "${data.sops_file.secrets.data["CLUSTER_ID"]}",
    "DB_CLUSTER": "${data.sops_file.secrets.data["DB_CLUSTER"]}",
    "DB_COLLECTION": "${data.sops_file.secrets.data["DB_COLLECTION"]}",
    "DB_NAME": "${data.sops_file.secrets.data["DB_NAME"]}",
    "DB_PASSWORD": "${data.sops_file.secrets.data["DB_PASSWORD"]}",
    "DB_USER": "${data.sops_file.secrets.data["DB_USER"]}"
  }
  EOF
}

##################
## IAM
##################
resource "aws_iam_policy" "crawler" {
  name        = var.crawler_role_name
  path        = "/"
  description = "Allows Lambda to retrieve Database secrets"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "SecretsManagerActions",
        "Effect" : "Allow",
        "Action" : [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ],
        "Resource" : [
          "${aws_secretsmanager_secret_version.database.arn}"
        ]
      }
    ]
  })
}

resource "aws_iam_policy" "manager" {
  name        = var.manager_role_name
  path        = "/"
  description = "Allows Lambda to block/delete old Lambdas"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "SecretsManagerActions",
        "Effect" : "Allow",
        "Action" : [
          "lambda:InvokeFunctionUrl",
          "lambda:InvokeFunction",
          "lambda:InvokeAsync"
        ],
        "Resource" : [
          "${aws_lambda_function.crawler.arn}"
        ]
      }
    ]
  })
}

resource "aws_iam_role" "crawler" {
  name        = var.crawler_role_name
  description = "Allows Lambda to block/delete old Lambdas"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
    aws_iam_policy.crawler.arn
  ]
}

resource "aws_iam_role" "manager" {
  name        = var.manager_role_name
  description = "Allows Lambda to block/delete old Lambdas"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
    aws_iam_policy.manager.arn
  ]
}


##################
### LAMBDA
##################
resource "aws_lambda_function" "crawler" {
  function_name = var.crawler_lambda_name
  description   = "Runs the latest image of ${var.crawler_ecr_name}"
  role          = aws_iam_role.crawler.arn

  memory_size  = var.crawler_memory_size
  package_type = "Image"
  timeout      = var.crawler_timeout
  image_uri    = "${aws_ecr_repository.crawler.repository_url}:latest"

  environment {
    variables = {
      RUN_LOCALLY_WITH_HEADER = "FALSE"
      DATABASE_SECRET_NAME    = aws_secretsmanager_secret_version.database.arn
    }
  }
}

resource "aws_lambda_function" "manager" {
  function_name = var.manager_lambda_name
  description   = "Runs the latest image of ${var.manager_ecr_name}"
  role          = aws_iam_role.manager.arn

  memory_size  = var.manager_memory_size
  package_type = "Image"
  timeout      = var.manager_timeout
  image_uri    = "${aws_ecr_repository.manager.repository_url}:latest"

  environment {
    variables = {
      CRAWLER_LAMBDA_NAME = var.crawler_lambda_name
      DRY_RUN             = "FALSE"
      MAX_CRAWLERS        = "500"
    }
  }
}
