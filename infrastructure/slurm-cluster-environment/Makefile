tfiles = *.tf *.yml
ansiblefiles = *.yaml

default: deploy

terraforminit: $(tfiles)
	terraform init
	touch terraforminit

buildvms: terraforminit Makefile $(tfiles)
	terraform apply
	sleep 300
	touch buildvms

deploy: buildvms Makefile $(ansiblefiles)
	ansible-playbook -i generate_inventory.py full.yaml
	touch deploy

clean:
	rm -rf .generated/ terraforminit buildvms deploy
	terraform destroy

.PHONY: clean 