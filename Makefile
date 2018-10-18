all:
	-$(MAKE) doxy
	$(MAKE) log.log

log.log: src.src py.py
	python py.py $< > $@ && tail $(TAIL) $@
	
doxy:
	doxygen doxy.gen 1> /dev/null
