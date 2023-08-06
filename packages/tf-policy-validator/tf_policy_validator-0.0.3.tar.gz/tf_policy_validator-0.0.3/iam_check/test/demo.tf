resource "aws_iam_policy" "demo_policy" {
  name        = "demo-policy"
  description = "This is an IAM policy for demo purpose"
  #policy = data.aws_iam_policy_document.demo_policy.json
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ec2:Describe*",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:s3:::thursdemobucket"
      },
    ]
  })
}

