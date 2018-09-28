DEFAULT_PLAYBOOK = """
---
- name: Push Desired Configuration to Devices
  hosts: localhost
  connection: local
  gather_facts: no

  tasks:

    - name: NSO sync-to action
      nso_action:
        url: "{{ nso.url }}"
        username: "{{ nso.username }}"
        password: "{{ nso.password }}"
        path: /ncs:devices/sync-to
        input: {}

- name: Push Device Configuration to NSO
  hosts: all
  connection: local
  gather_facts: no

  tasks:
    - name: Device configuration
      nso_config:
        url: "{{ nso.url }}"
        username: "{{ nso.username }}"
        password: "{{ nso.password }}"
        data:
          tailf-ncs:devices:
            device:
            - name: "{{ inventory_hostname }}"
              tailf-ncs:config:
                "{{ config }}"

- name: Push Desired Configuration to Devices
  hosts: localhost
  connection: local
  gather_facts: no

  tasks:

    - name: NSO sync-to action
      nso_action:
        url: "{{ nso.url }}"
        username: "{{ nso.username }}"
        password: "{{ nso.password }}"
        path: /ncs:devices/sync-to
        input: {}
"""
