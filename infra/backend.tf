# Uncomment after creating the S3 bucket and DynamoDB table for Terraform state.
# terraform {
#   backend "s3" {
#     bucket         = "elite-terraform-state"
#     key            = "infra/terraform.tfstate"
#     region         = "us-east-1"
#     dynamodb_table = "elite-terraform-locks"
#     encrypt        = true
#   }
# }
