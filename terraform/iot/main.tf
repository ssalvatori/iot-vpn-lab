provider "aws" {
  region = var.region
}

resource "aws_iot_thing_type" "this" {
  name = "rbpi"
}

resource "aws_iot_thing" "this" {
  name = "rbpi-lab"

  thing_type_name = aws_iot_thing_type.this.name

  attributes = {
    Type = "rbpi3"
  }
}

resource "aws_iot_certificate" "this" {
  active = true
}

resource "aws_iot_policy" "pubsub" {
  name = "PubSubToAnyTopic"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "iot:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iot_policy_attachment" "att" {
  policy = aws_iot_policy.pubsub.name
  target = aws_iot_certificate.this.arn
}

resource "local_file" "things_cert" {
  content  = aws_iot_certificate.this.certificate_pem
  filename = "${path.module}/certs/cert.pem"
}

resource "local_file" "things_private_key" {
  content  = aws_iot_certificate.this.private_key
  filename = "${path.module}/certs/private_key.pem"
}

resource "local_file" "things_public_key" {
  content  = aws_iot_certificate.this.public_key
  filename = "${path.module}/certs/public_key.pem"
}

resource "aws_iot_thing_principal_attachment" "this" {
  principal = aws_iot_certificate.this.arn
  thing     = aws_iot_thing.this.name
}

output "thing" {
  value = aws_iot_thing.this
}

data "aws_iot_endpoint" "example" {
  endpoint_type = "iot:Data-ATS"
}

output "endpoint" {
  value = data.aws_iot_endpoint.example
}
