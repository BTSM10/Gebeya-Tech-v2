# Gebeya Week 1 — Hello World Terraform Script
# This provisions a basic AWS EC2 instance to host the Streamlit dashboard

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS provider — region where resources will be created
provider "aws" {
  region = "us-east-1"
}

# EC2 instance — a virtual server to run the dashboard
resource "aws_instance" "dashboard_server" {
  ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 (us-east-1)
  instance_type = "t2.micro"               # free tier eligible

  tags = {
    Name    = "Gebeya-Dashboard-Server"
    Project = "Gebeya-Week1-Challenge"
  }
}

# S3 bucket — cloud storage for data and artefacts
resource "aws_s3_bucket" "data_bucket" {
  bucket = "gebeya-slack-analysis-data"

  tags = {
    Name    = "Gebeya-Data-Bucket"
    Project = "Gebeya-Week1-Challenge"
  }
}

# Output the public IP of the server after creation
output "server_public_ip" {
  description = "Public IP address of the dashboard server"
  value       = aws_instance.dashboard_server.public_ip
}

output "s3_bucket_name" {
  description = "Name of the S3 data bucket"
  value       = aws_s3_bucket.data_bucket.bucket
}
