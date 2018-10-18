all:
	-$(MAKE) doxy
	$(MAKE) log.log

log.log: src.src py.py
	python py.py $< > $@ && tail $(TAIL) $@
	
doxy:
	doxygen doxy.gen 1> /dev/null

https: cert.pem key.pem
cert.pem key.pem:
	openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
	