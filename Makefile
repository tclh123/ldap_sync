SHELL = bash

.PHONY : install

install: venv install-dependecies
	source venv/bin/activate; pip install --upgrade pip
	source venv/bin/activate; pip install -e .

venv:
	if dpkg -s python3.8; then \
		sudo apt install -y python3.8-venv ;\
		python3.8 -mvenv venv ;\
	elif type virtualenv && type python3; then \
		export LC_ALL="en_US.UTF-8" ;\
		virtualenv venv --python=python3 ;\
	else \
		echo Error: You need install at least python3.6 or virtualenv first. ;\
	fi

install-dependecies:
	# for building python-ldap
	sudo apt install -y python3.8-dev libsasl2-dev libldap2-dev libssl-dev
