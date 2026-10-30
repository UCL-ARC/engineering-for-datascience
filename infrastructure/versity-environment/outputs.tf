output vm_ips {
  value = harvester_virtualmachine.vm[*].network_interface[0].ip_address
}

output vm_ids {
  value = harvester_virtualmachine.vm.*.id
}

output s3_url {
  value = "${var.username}-s3.comp0235.condenser.arc.ucl.ac.uk"
}

output webui_url {
  value = "https://${var.username}-s3.comp0235.condenser.arc.ucl.ac.uk/ui/"
}