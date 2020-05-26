provider "aws" {
  region = var.region
}

data "aws_caller_identity" "current" {}

resource "aws_iam_role" "this" {
  name = "vpn-tunnel-alexa-skill"

  path = "/service-role/"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "execution_policy" {
  name        = "execution_policy"
  description = "execution_policy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
              "logs:PutLogEvents",
              "logs:DescribeLogStreams",
              "logs:CreateLogStream",
              "logs:CreateLogGroup"
            ],
            "Resource": [
                "arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:*"
            ]
        }
    ]
}
EOF
}

resource "aws_iam_policy" "iot_publish" {
  name        = "iot_publish_test"
  description = "iot_publish"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "iot:Publish",
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "attach_publish" {
  role       = aws_iam_role.this.name
  policy_arn = aws_iam_policy.iot_publish.arn
}

resource "aws_iam_role_policy_attachment" "attach_execution" {
  role       = aws_iam_role.this.name
  policy_arn = aws_iam_policy.execution_policy.arn
}


resource "aws_lambda_function" "this" {
  function_name = var.function_name
  description   = "VPN LAB lambda function"
  filename      = var.source_zip

  role    = aws_iam_role.this.arn
  handler = "index.handler"
  publish = true

  source_code_hash = filebase64sha256(var.source_zip)

  runtime     = "nodejs12.x"
  memory_size = "128"

  environment {
    variables = {
      ATS_ENDPOINT = var.iot_ats_endpoint
      THINGS_NAME  = var.iot_thing_name
    }
  }
}

resource "aws_cloudwatch_log_group" "this" {
  name = "/aws/lambda/${var.function_name}"
}

resource "aws_lambda_permission" "alexa-trigger" {
  statement_id  = "AllowExecutionFromAlexa"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal     = "alexa-appkit.amazon.com"
}
