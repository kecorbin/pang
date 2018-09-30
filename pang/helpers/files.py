MAKEFILE_BASE = """

clean:  netsim-clean nso-clean ansible-clean

dev: netsim start-netsim nso dev-sync-to deploy-dev

nso:
	-@ncs-setup --dest .
	-@echo "Starting local NSO instance..."
	-@ncs

ansible-clean:
	-@rm *.retry > /dev/null

start-netsim:
	-@ncs-netsim start

netsim-clean:
	-@echo "Stopping All Netsim Instances..."
	-@killall confd
	-@rm -Rf netsim/
	-@rm README.netsim

nso-clean:
	-@echo "Stopping NSO..."
	-@ncs --stop
	-@rm -Rf README.ncs agentStore state.yml logs/ ncs-cdb/ ncs-java-vm.log ncs-python-vm.log ncs.conf state/ storedstate target/

deploy-dev:
	-@ansible-playbook -i inventory/dev.yaml site.yaml

deploy:
	-@ansible-playbook -i inventory/prod.yaml site.yaml

dev-sync-to:
	-@echo "Performing devices sync-to..."
	-@curl -X POST -u admin:admin http://localhost:8080/api/running/devices/_operations/sync-from

sync-to:
	-@echo "Performing devices sync-to..."
	-@curl -X POST -u admin:admin {base_url}/api/running/devices/_operations/sync-from

sync-from:
	-@echo "Performing devices sync-from..."
	-@curl -X POST -u admin:admin {base_url}/api/running/devices/_operations/sync-from
"""
