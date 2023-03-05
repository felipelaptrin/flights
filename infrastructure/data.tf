data "sops_file" "secrets" {
  source_file = "encrypted_secrets.yaml"
}
