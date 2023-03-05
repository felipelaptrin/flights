## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.3.4 |
| <a name="requirement_sops"></a> [sops](#requirement\_sops) | ~> 0.5 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 4.57.0 |
| <a name="provider_sops"></a> [sops](#provider\_sops) | 0.7.2 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_ecr_repository.crawler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecr_repository) | resource |
| [aws_ecr_repository.manager](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecr_repository) | resource |
| [aws_iam_policy.crawler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role.crawler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role.manager](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_lambda_function.crawler](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function.manager](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_secretsmanager_secret.database](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/secretsmanager_secret) | resource |
| [aws_secretsmanager_secret_version.database](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/secretsmanager_secret_version) | resource |
| [sops_file.secrets](https://registry.terraform.io/providers/carlpett/sops/latest/docs/data-sources/file) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_crawler_ecr_name"></a> [crawler\_ecr\_name](#input\_crawler\_ecr\_name) | Name of ECR repo that will contain the Flight Crawler code | `string` | `"flights-crawler"` | no |
| <a name="input_crawler_lambda_name"></a> [crawler\_lambda\_name](#input\_crawler\_lambda\_name) | Name of Lambda that will contain the Flight Crawler code | `string` | `"flights-crawler"` | no |
| <a name="input_crawler_memory_size"></a> [crawler\_memory\_size](#input\_crawler\_memory\_size) | Memory size of the Flight Crawler Lambda | `number` | `512` | no |
| <a name="input_crawler_role_name"></a> [crawler\_role\_name](#input\_crawler\_role\_name) | Name of the IAM Role and IAM Policy for the Flight Crawler Lambda | `string` | `"flights-crawler"` | no |
| <a name="input_crawler_timeout"></a> [crawler\_timeout](#input\_crawler\_timeout) | Lambda timeout of the Flight Crawler Lambda | `number` | `120` | no |
| <a name="input_database_secrets_name"></a> [database\_secrets\_name](#input\_database\_secrets\_name) | Name of the secrets containing DB credentials | `string` | `"flights-crawler-database"` | no |
| <a name="input_manager_ecr_name"></a> [manager\_ecr\_name](#input\_manager\_ecr\_name) | Name of ECR repo that will contain the Flight Manager code | `string` | `"flights-manager"` | no |
| <a name="input_manager_lambda_name"></a> [manager\_lambda\_name](#input\_manager\_lambda\_name) | Name of Lambda that will contain the Flight Manager code | `string` | `"flights-manager"` | no |
| <a name="input_manager_memory_size"></a> [manager\_memory\_size](#input\_manager\_memory\_size) | Memory size of the Flight Manager Lambda | `number` | `128` | no |
| <a name="input_manager_role_name"></a> [manager\_role\_name](#input\_manager\_role\_name) | Name of the IAM Role for the Flight Manager Lambda | `string` | `"flights-manager"` | no |
| <a name="input_manager_timeout"></a> [manager\_timeout](#input\_manager\_timeout) | Lambda timeout of the Flight Manager Lambda | `number` | `60` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_crawler_lambda_arn"></a> [crawler\_lambda\_arn](#output\_crawler\_lambda\_arn) | ARN of the Flight Crawler Lambda |
| <a name="output_crawler_repo_url"></a> [crawler\_repo\_url](#output\_crawler\_repo\_url) | The URL of the repository (in the form aws\_account\_id.dkr.ecr.region.amazonaws.com/repositoryName) |
| <a name="output_manager_lambda_arn"></a> [manager\_lambda\_arn](#output\_manager\_lambda\_arn) | ARN of the Flight Manager Lambda |
| <a name="output_manager_repo_url"></a> [manager\_repo\_url](#output\_manager\_repo\_url) | The URL of the repository (in the form aws\_account\_id.dkr.ecr.region.amazonaws.com/repositoryName) |
