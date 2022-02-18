path "secret/data/ansible" {
  capabilities = ["read"]
}

path "secret/data/ansible/*" {
  capabilities = ["read"]
}
