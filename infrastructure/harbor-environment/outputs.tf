output vm_ips {
  value = harvester_virtualmachine.vm[*].network_interface[0].ip_address
}

output vm_ids {
  value = harvester_virtualmachine.vm.*.id
}

output external_url {
  value =  "${var.username}-reg.comp0235.condenser.arc.ucl.ac.uk"
}
