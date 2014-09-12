all: addons

design/clinic.xmi: design/clinic.zargo
	-echo "REBUILD clinic.xmi from clinic.zargo. I cant do it"

addons: clinic

clinic: design/clinic.uml
	xmi2oerp -r -i $< -t addons -v 2
	mv addons/i18n addons/clinic/

clean:
	mv addons/clinic/i18n/ addons/
	sleep 1
	touch design/clinic.uml
