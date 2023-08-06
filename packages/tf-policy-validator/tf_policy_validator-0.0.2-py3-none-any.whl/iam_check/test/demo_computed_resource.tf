resource "aws_s3_bucket" "demo" {
  bucket = "demo-bucket"

  tags = {
    Name        = "Demo bucket"
    Environment = "Dev"
  }
}

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
        Resource = "${aws_s3_bucket.demo.arn}"
      },
    ]
  })
}

