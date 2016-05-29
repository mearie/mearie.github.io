LANGS = ko en
SRC = src/templates.m4
FILES = main index softwares documents sitemap keywords journal
OUT = \
	$(foreach FILE,$(FILES),$(patsubst %,$(FILE).%.html,$(LANGS))) \
	multichoice.html \
	redirect.html \
	notfound.html

.PHONY: all
all: $(OUT)

.PHONY: clean
clean:
	-@rm -f $(OUT)

main.%.html: $(SRC)
	@m4 -DLANG=$* $< > $@
index.%.html: $(SRC) src/index.m4
	@m4 -DLANG=$* -DBODYCLASS=mearie-index -DAFTER=index -DHIDETITLE $< > $@
softwares.%.html: $(SRC) src/softwares.m4
	@m4 -DLANG=$* -DAFTER=softwares $< > $@
documents.%.html: $(SRC) src/documents.m4
	@m4 -DLANG=$* -DAFTER=documents $< > $@
sitemap.%.html: $(SRC) src/sitemap.m4
	@m4 -DLANG=$* -DAFTER=sitemap $< > $@
keywords.%.html: $(SRC) src/keywords.m4
	@m4 -DLANG=$* -DAFTER=keywords $< > $@
journal.%.html: $(SRC) src/journal.m4
	@m4 -DLANG=$* -DAFTER=journal $< > $@

multichoice.html: $(SRC)
	@m4 -DLANG=en -DPAGE=multichoice $< > $@
redirect.html: $(SRC)
	@m4 -DLANG=en -DPAGE=redirect $< > $@
notfound.html: $(SRC)
	@m4 -DLANG=en -DPAGE=notfound $< > $@

