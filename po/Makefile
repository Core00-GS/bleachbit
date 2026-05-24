APP = bleachbit
POFILES = $(wildcard *.po)
MOFILES = $(patsubst %.po,%.mo,$(POFILES))
PYSRC = $(wildcard ../bleachbit/*.py)
UISRC = ../data/app-menu.ui
POTFILE = $(APP).pot

# Use PYTHON environment variable if available, otherwise default to python3
PYTHON ?= python3

# Download GNOME gtkbuilder ITS rules on demand (MSYS2 gettext lacks them)
ITS_URL = https://raw.githubusercontent.com/GNOME/gtk/gtk-3-24/gtk

.PHONY: refresh-po spelling local install clean all

its/gtkbuilder.its:
	mkdir -p its
	curl -fsSL -o $@ $(ITS_URL)/gtkbuilder.its

its/gtkbuilder.loc:
	mkdir -p its
	curl -fsSL -o $@ $(ITS_URL)/gtkbuilder.loc

cleanerml.pot: ../bleachbit/CleanerML.py ../cleaners/*xml
	$(PYTHON) ../bleachbit.py --pot

ui.pot: $(UISRC) its/gtkbuilder.its its/gtkbuilder.loc
	xgettext -o ui.pot \
		--add-comments=TRANSLATORS \
		--add-location=file \
		--keyword="_p:1c,2" \
		--default-domain=$(APP) \
		--from-code=UTF-8 \
		--its=its/gtkbuilder.its \
		$(UISRC)

$(POTFILE): $(PYSRC) cleanerml.pot ui.pot
	@echo "* Generating $(APP).pot"
	echo " Words before update: " \
		`tail -n +20 bleachbit.pot | grep -v ^# | sed "s/\(msgstr\|msgid\)//g" | sort | wc --words`
	cat cleanerml.pot > $(APP).pot
	xgettext -o $(APP).pot \
		--join-existing \
		--add-comments=TRANSLATORS \
		--add-location=file \
		--keyword="_p:1c,2" \
		--default-domain=$(APP) \
		--from-code=UTF-8 \
		$(PYSRC)
	msgcat -o $(APP).pot $(APP).pot ui.pot
	sed -i 's/charset=CHARSET/charset=utf-8/g' bleachbit.pot
	# Remove carriage return characters
	sed -i 's/\r//g' bleachbit.pot
	# Convert backslashes to forward slashes in file paths
	sed -i '/^#:/ s/\\/\//g' bleachbit.pot
	echo " Words after update: " \
		`tail -n +20 bleachbit.pot | grep -v ^# | sed "s/\(msgstr\|msgid\)//g" | sort | wc --words`


refresh-po: $(POTFILE)
	@echo "* Refreshing .po files"
	for oldpo in $(POFILES); do \
		lang=`basename $$oldpo .po`; \
		echo $$lang; \
		msgmerge --no-fuzzy-matching -v $${lang}.po $(POTFILE) > $${lang}.pot; \
		mv $$lang.pot $$lang.po; \
	done

spelling: $(POTFILE)
	@echo "* Checking spelling"
	@echo
	@echo Word count: `msggrep -Kie . --no-wrap $(POTFILE)  | grep ^msgid  | cut -c 8- | wc --words`
	@echo
	msggrep -Kie . --no-wrap $(POTFILE)  | grep ^msgid  | cut -c 8- | aspell --personal=./aspell.pws list | sort -u

%.mo: %.po
	@echo "* Generating $@"
	msgfmt --statistics -o $@ $<

local: $(MOFILES)
	@echo "* Copy locally for running without system installation"
	for mofile in $(MOFILES); do \
		lang=`basename $$mofile .mo`; \
		mkdir -p ../locale/$$lang/LC_MESSAGES/; \
		cp -lf $$mofile ../locale/$$lang/LC_MESSAGES/bleachbit.mo; \
	done
	@echo "Now you can run cd ..; $(PYTHON) bleachbit/GUI.py"

install: $(MOFILES)
	echo "* Installing in $(DESTDIR)/usr/share/locale"
	for MO in $(MOFILES); do \
		lang=`basename $$MO .mo`; \
		DST=$(DESTDIR)/usr/share/locale/$$lang/LC_MESSAGES/; \
		mkdir -p $$DST; \
		cp $$MO $$DST/bleachbit.mo; \
done

clean:
	echo "* Cleaning"
	@rm -fv *.mo
	@rm -fv $(APP).pot cleanerml.pot ui.pot
	@rm -rfv ../locale
	@rm -rfv its

all: $(APP).pot $(MOFILES)

