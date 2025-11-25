# Interpret namespace and network name based on user name
locals {
  namespace = "${var.username}-comp0235-ns"
  network_name = "${var.username}-comp0235-ns/ds4eng"
}

data "harvester_image" "img" {
  display_name = var.img_display_name
  namespace    = "harvester-public"
}

data "harvester_ssh_key" "mysshkey" {
  name      = var.keyname
  namespace = local.namespace
}

resource "random_id" "secret" {
  byte_length = 5
}

resource "harvester_cloudinit_secret" "cloud-config" {
  name      = "cloud-config-${random_id.secret.hex}"
  namespace = local.namespace

  user_data = templatefile("cloud-init.tmpl.yml", {
      public_key_openssh = data.harvester_ssh_key.mysshkey.public_key
    })
}

resource "harvester_virtualmachine" "vm" {
  
  count = var.vm_count

  name                 = "${var.username}-harbor-${format("%02d", count.index + 1)}-${random_id.secret.hex}"
  namespace            = local.namespace
  restart_after_update = true

  description = "Base VM"

  cpu    = 2
  memory = "16Gi"

  efi         = true
  secure_boot = true

  run_strategy    = "RerunOnFailure"
  hostname        = "${var.username}-harbor-${format("%02d", count.index + 1)}-${random_id.secret.hex}"
  reserved_memory = "100Mi"
  machine_type    = "q35"

  network_interface {
    name           = "nic-1"
    wait_for_lease = true
    type           = "bridge"
    network_name   = local.network_name
  }

  disk {
    name       = "rootdisk"
    type       = "disk"
    size       = "50Gi"
    bus        = "virtio"
    boot_order = 1

    image       = data.harvester_image.img.id
    auto_delete = true
  }

  tags = {
    condenser_ingress_isEnabled = true
    condenser_ingress_reg_hostname = "${var.username}-reg"
    condenser_ingress_reg_port = 443
    condenser_ingress_reg_protocol = "https"
    condenser_ingress_reg_nginx_proxy-body-size = "100000m"
  }

  cloudinit {
    user_data_secret_name = harvester_cloudinit_secret.cloud-config.name
  }

  timeouts {
    create = "20m"
    update = "20m"
    delete = "20m"
  }
}
