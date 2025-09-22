data "local_file" "new_public_key" {
  filename = var.keyfile
}

resource "harvester_ssh_key" "new_key" {
  name      = var.keyname
  namespace = var.namespace

  public_key = data.local_file.new_public_key.content
}

