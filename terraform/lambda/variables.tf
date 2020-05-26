variable "region" {
  default = "eu-central-1"
}

variable "function_name" {
  default = "vpn-lab-alexa-skill"
}

variable "source_zip" {
  default = ""
}

variable "iot_ats_endpoint" {
  description = "Endpoint for the IoT shadow queue"
  default     = ""
}

variable "iot_thing_name" {
  description = "Name of the device in IoT Service"
  default     = "rbpi-lab"
}
