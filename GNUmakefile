# a part of mearie.org

INPUT = pages
OUTPUT = target
RES = res
TMP = tmp
JSONIN = $(TMP)/json-in
JSONOUT = $(TMP)/json-out
AUX = $(TMP)/aux
DEPS = $(TMP)/deps
GENDEPS = $(TMP)/gen-deps
REFS = $(TMP)/refs
INDICES = $(TMP)/indices.db

GIT = git
PYTHON = python
PANDOC = pandoc

PREPROCESSOR = $(RES)/preprocess.py
POSTPROCESSOR = $(RES)/postprocess.py
SCHEMACHECK = $(RES)/check-schema.py
WRITER = $(RES)/writer.lua
PURGESTRAY = $(RES)/purge-stray.py

LANGS = ko en ja
DOMAINNAME = neu.mearie.org

SOURCES := $(wildcard $(INPUT)/*.md $(INPUT)/*/*.md $(INPUT)/*/*/*.md)
PREPROCJSONS = $(patsubst $(INPUT)/%.md,$(JSONIN)/%.json,$(SOURCES))
POSTPROCJSONS = $(patsubst $(INPUT)/%.md,$(JSONOUT)/%.json,$(SOURCES))
TARGETS = $(patsubst $(INPUT)/%.md,$(OUTPUT)/%.html,$(SOURCES))
INCLUDES = $(sort \
	$(patsubst $(INPUT)/%.md,$(DEPS)/%.d,$(SOURCES)) \
	$(foreach LANG,$(LANGS),$(patsubst $(INPUT)/%.$(LANG).md,$(GENDEPS)/%_multichoice.d,\
		$(filter $(INPUT)/%.$(LANG).md,$(SOURCES)))))
GENERATED :=

ORIGIN = https://github.com/mearie/mearie.github.io
BRANCH = master

I = printf '  %s%-12s%s%s\n' "$$(tput setaf $(1))$$(tput bold)" $(2) "$$(tput sgr0)" "$$(echo $(3))"
EMPTY =
SPACE = $(EMPTY) $(EMPTY)
COMMA = ,

.PHONY: all
all: $(OUTPUT) purge-unused-target
	@$(MAKE) targets

# TODO ordering
.PHONY: travis
travis: $(OUTPUT) prepare-autobuild update-source purge-unused-target
	@$(MAKE) targets
	@$(MAKE) commit-target
	@$(MAKE) push-target

# separate target so that we can add more deps to this later
.PHONY: targets
targets: $(TARGETS) | purge-unused-target

$(OUTPUT): $(OUTPUT)/.git

$(OUTPUT)/.git:
	@$(call I, 7, ===, initializing git repository)
	@$(GIT) init --quiet $(OUTPUT)
	@cd $(OUTPUT) && $(GIT) config --local user.email ''
	@cd $(OUTPUT) && $(GIT) config --local user.name 'Travis fairy for mearie.org'
	@cd $(OUTPUT) && $(GIT) remote add origin $(ORIGIN)

$(OUTPUT)/res: | $(OUTPUT)
	@$(call I, 7, mkdir, /res)
	@mkdir -p $@

.PRECIOUS: $(RES)/styles/%.css
$(RES)/styles/%.css: $(RES)/styles/%.scss
	@$(call I, 4, sass, $*.css)
	@sassc -t compressed $< $@

override GENERATED += $(OUTPUT)/favicon.ico
$(OUTPUT)/favicon.ico: $(RES)/mearie.ico
	@$(call I, 1, copy, /favicon.ico)
	@cp $< $@

override GENERATED += $(wildcard $(OUTPUT)/res/*.css)
$(OUTPUT)/res/%.css: $(RES)/styles/%.css | $(OUTPUT)/res
	@$(call I, 1, copy, /res/$*.css)
	@cp $< $@

override GENERATED += $(wildcard $(OUTPUT)/res/*.js)
$(OUTPUT)/res/%.js: $(RES)/scripts/%.js | $(OUTPUT)/res
	@$(call I, 1, copy, /res/$*.js)
	@cp $< $@

$(RES)/templates/%.html $(LANGS:%=$(RES)/templates/\%.%.html): $(RES)/templates/src/templates.m4 | $(RES)/templates/Makefile
	@$(call I, 4, maketmpl, $(notdir $@))
	@$(MAKE) -C $(dir $@) $(notdir $@)

# we may automatically generate dependencies for them, but we've done enough
define TEMPLATE_UPDATE_RULE
$$(LANGS:%=$$(RES)/templates/$(1).%.html): $$(RES)/templates/src/$(1).m4
endef
$(foreach TMPL,index softwares documents sitemap keywords journal,$(eval $(call TEMPLATE_UPDATE_RULE,$(TMPL))))

.PHONY: prepare-autobuild
prepare-autobuild: $(OUTPUT)
	@$(call I, 7, ===, preparing autobuild)
	@cd $(OUTPUT) && $(GIT) pull --quiet --depth=1 origin $(BRANCH) || echo 'Warning: We are creating a branch now!'
	@cd $(OUTPUT) && $(GIT) checkout $(BRANCH) && $(GIT) branch -D autobuild && $(GIT) checkout --orphan autobuild

.PHONY: update-source
update-source: $(OUTPUT) prepare-autobuild
	@$(call I, 7, ===, updating source)
	@$(GIT) ls-tree --name-only -zrt HEAD | xargs -0 touch -t 197101010000
	@-$(GIT) diff --name-only -z $$($(GIT) rev-list -n1 --before="$$(cd $(OUTPUT) && $(GIT) log -1 --format=format:%ad $(BRANCH))" HEAD) HEAD | xargs -0 touch -c

.PHONY: check-schema
check-schema:
	@$(call I, 7, ===, checking index schema)
	@mkdir -p $(dir $(INDICES))
	@$(PYTHON) $(SCHEMACHECK) $(INDICES)

# http://make.mad-scientist.net/secondary-expansion/
# we need it in the following rules (in particular, md-to-json rules)
.SECONDEXPANSION:

# the order of dependencies is important:
# the config cannot be overwritten, but the per-directory default can.
# also note the wildcard guard as the per-directory default may be absent.
.SECONDARY: $(PREPROCJSONS)
$(JSONIN)/%.json: $(RES)/config.yaml $(INPUT)/%.md $$(wildcard $$(dir $(INPUT)/$$*)/default.yaml)
	@$(call I, 6, parse, /$*)
	@mkdir -p $(dir $@)
	@$(PANDOC) -f markdown-auto_identifiers-citations-example_lists+link_attributes -S -t json $^ -o $@

# normally, auto-dependency generation should *not* have *.d files in the targets
# as otherwise the Makefile will be rebuilt in every possible occasion.
# however, this principle cannot be applied in this case because we need to use
# generated dependencies as soon as *.d files are built (unlike normal compilation).
# therefore we have this ugly hack: break the dependency chain only when required.
.SECONDARY: $(POSTPROCJSONS) $(INCLUDES)
ifeq ($(findstring clean,$(MAKECMDGOALS)),)
$(DEPS)/%.d $(JSONOUT)/%.json: $(JSONIN)/%.json $(PREPROCESSOR) | check-schema
else
$(JSONOUT)/%.json: $(JSONIN)/%.json $(PREPROCESSOR) | check-schema
endif
	@$(call I, 5, preprocess, /$*)
	@mkdir -p $(dir $(DEPS)/$*.d $(GENDEPS)/$*.d $(JSONOUT)/$*.json)
	@$(PYTHON) $(PREPROCESSOR) $(INDICES) $(INPUT)/%.md $(JSONIN)/%.json $(JSONOUT)/%.json $(AUX)/%.json $(DEPS)/%.d $(GENDEPS)/%.d $(REFS)/% $(OUTPUT)/%.html $(OUTPUT)/% /$*
	@mkdir -p $(dir $(REFS)/$*) && touch $(REFS)/$* $(basename $(REFS)/$*)

# preprocessor implicitly updates the indices
$(INDICES): $(POSTPROCJSONS)

# $(1): json in
# $(2): reference out
# $(3): html out
# $(4): url
# $(5): raw stem
# $(6): template name
# $(7): language
# $(8): variable name for space-separated list of other languages (for lazy resolution)
# $(9): more dependencies to track (typically reference files)
# e.g. LANGS = ko en
#      $(eval $(call JSON_TO_HTML_RULE,$(JSONOUT)/%.json,\
#                                      $(REFS)/%,\
#                                      $(OUTPUT)/%.html,\
#                                      /%,\
#                                      $(basename %),\
#                                      main,\
#                                      ko,\
#                                      LANGS,\
#                                      $(REFS)/keywords/foo.ko $(REFS)/keywords/bar.ko))
#
# no comment offered for the massively obfuscated recipe, sorry
#
# the empty prerequisites are required to suppress some annoying errors
# http://make.mad-scientist.net/papers/advanced-auto-dependency-generation/#norule
define JSON_TO_HTML_RULE
$(2): $(1)
$(3): $(1) $$(RES)/templates/$(6).html $$(WRITER) $$(POSTPROCESSOR) $$(REFS)/$(5) $(9) | $$(OUTPUT) $$(OUTPUT)/favicon.ico $$(OUTPUT)/res/main.css $$(OUTPUT)/res/mearie.js purge-unused-target
	@$$(call I, 3, html, $(4))
	@mkdir -p $$(dir $$@)
	@printf '[{"unMeta":{"otherlangs":{"t":"MetaList","c":[$$(subst $$(SPACE),$$(COMMA),$$(patsubst %,{"t":"MetaString"$$(COMMA)"c":"%"},$$(filter-out $(7),$$($(8)))))]}}},[]]' | $$(PANDOC) --webtex --standalone --data-dir=$$(RES) --template=$(6).html -f json -t $$(WRITER) $$(filter $$(JSONOUT)/$(5).$(7)%.json,$$^) - | $$(PYTHON) $$(POSTPROCESSOR) $$(INDICES) > $$@
$(1):
endef

# $(1): space-separated list of json out (for dependencies)
# $(2): redirected html
# $(3): redirected url
# $(4): redirection target html
# $(5): redirection target url
# e.g. $(eval $(call REDIRECT_RULE,$(JSONOUT)/path/to/long.json,\
#                                  $(OUTPUT)/short.html,\
#                                  /short,\
#                                  $(OUTPUT)/path/to/long.html,\
#                                  /path/to/long))
define REDIRECT_RULE
override GENERATED += $(2)
targets: $(2)
$(2): $(1) $$(RES)/templates/redirect.html $$(RES)/config.yaml $$(WRITER) | $$(OUTPUT)
	@$$(call I, 2, redirect, $(3) '->' $(5))
	@mkdir -p $$(dir $$@)
	@$$(PANDOC) --standalone --data-dir=$$(RES) --template=redirect.html -f markdown -t $$(WRITER) $$(RES)/config.yaml '-Vself=$(5:/%=%)' -o $$@
$(1):
endef

# $(1): space-separated list of json out
# $(2): space-separated list of languages
# $(3): html
# $(4): url
define MULTICHOICE_RULE
override GENERATED += $(3)
targets: $(3)
$(3): $(1) $$(RES)/templates/multichoice.html $$(RES)/config.yaml $$(WRITER) | $$(OUTPUT)
	@$$(call I, 2, multichoice, $(4))
	@mkdir -p $$(dir $$@)
	@printf '\055--\nself: "$(4:/%=%)"\navailable_lang: [$(subst $(SPACE),$(COMMA),$(2))]\n...' | $$(PANDOC) --standalone --data-dir=$$(RES) --template=multichoice.html -t $$(WRITER) $$(RES)/config.yaml - -o $$@
$(1):
endef

# this should go before anything depends on GENERATED
-include $(INCLUDES)

# /index
INDEX_BUILD = $(RES)/pages/index.py
define INDEX_RULE
$$(OUTPUT)/index.$(1).html: $$(JSONOUT)/index.$(1).gen.json
$$(JSONOUT)/index.$(1).gen.json: $$(INDICES) $$(INDEX_BUILD)
	@$$(call I, 1, generate, /index.$(1))
	@$$(PYTHON) $$(INDEX_BUILD) $$< $(1) > $$@
endef
$(foreach LANG,$(LANGS),$(eval $(call INDEX_RULE,$(LANG))))

# /sitemap
SITEMAP_BUILD = $(RES)/pages/sitemap.py
define SITEMAP_RULE
$$(OUTPUT)/sitemap.$(1).html: $$(JSONOUT)/sitemap.$(1).gen.json
$$(JSONOUT)/sitemap.$(1).gen.json: $$(INDICES) $$(SITEMAP_BUILD)
	@$$(call I, 1, generate, /sitemap.$(1))
	@$$(PYTHON) $$(SITEMAP_BUILD) $$< $(1) > $$@
endef
$(foreach LANG,$(LANGS),$(eval $(call SITEMAP_RULE,$(LANG))))

# /w/
KEYWORDS_BUILD = $(RES)/pages/keywords.py
$(OUTPUT)/w/index.ko.html: $(JSONOUT)/w/index.ko.gen.json
$(JSONOUT)/w/index.ko.gen.json: $(INDICES) $(KEYWORDS_BUILD)
	@$(call I, 1, generate, /w/index.ko)
	@$(PYTHON) $(KEYWORDS_BUILD) $< ko > $@

define COPY_RULE
$$(OUTPUT)/%.$(1): $$(INPUT)/%.$(1) | $$(OUTPUT)
	@$$(call I, 1, copy, /$$*.$(1))
	@mkdir -p $$(@D)
	@cp $$< $$@
endef

COPY_EXTENSIONS=jpg png svg
$(foreach EXTENSION,$(COPY_EXTENSIONS),$(eval $(call COPY_RULE,$(EXTENSION))))

TARGETS += $(OUTPUT)/404.html
targets: $(OUTPUT)/404.html
$(OUTPUT)/404.html: $(RES)/templates/notfound.html | $(OUTPUT)
	@$(PANDOC) --standalone --data-dir=$(RES) --template=notfound.html -f markdown -t $(WRITER) $(RES)/config.yaml -o $@

TARGETS += $(OUTPUT)/CNAME
targets: $(OUTPUT)/CNAME
$(OUTPUT)/CNAME: | $(OUTPUT)
	@$(call I, 1, generate, /CNAME)
	@echo $(DOMAINNAME) > $@

TARGETS += $(OUTPUT)/.nojekyll
targets: $(OUTPUT)/.nojekyll
$(OUTPUT)/.nojekyll: | $(OUTPUT)
	@$(call I, 1, generate, /.nojekyll)
	@touch $@

# how unfortunate, isn't it
TARGETS += $(OUTPUT)/.travis.yml
targets: $(OUTPUT)/.travis.yml
$(OUTPUT)/.travis.yml: | $(OUTPUT)
	@$(call I, 1, generate, /.travis.yml)
	@echo 'branches:' > $@
	@echo '  only:' >> $@
	@echo '    - source' >> $@

.PHONY: purge-unused-target
purge-unused-target: $(OUTPUT) | check-schema
	@$(PYTHON) $(PURGESTRAY) $(INDICES) $(OUTPUT) $(REFS)/% -- $(patsubst $(OUTPUT)/%,%,$(TARGETS) $(GENERATED)) | while read f; do $(call I, 7, purge, /$$f); done

.PHONY: commit-target
commit-target:
	@$(call I, 7, ===, making a new commit)
	@cd $(OUTPUT) && $(GIT) add -f -A . && $(GIT) commit -m '' --allow-empty-message

.PHONY: push-target
push-target:
	@$(call I, 7, ===, pushing a new commit)
	@cd $(OUTPUT) && $(GIT) config --local credential.helper 'store --file=.git/credentials' && echo "https://$${GH_TOKEN}@github.com/" > .git/credentials
	@cd $(OUTPUT) && $(GIT) push -f -q origin autobuild:$(BRANCH)

.PHONY: clean
clean: clean-templates
	@$(call I, 7, ===, removing any generated files)
	@rm -rf $(OUTPUT) $(TMP)

.PHONY: clean-templates
clean-templates: $(RES)/templates/Makefile
	@$(call I, 7, ===, removing generated template files)
	@$(MAKE) -C $(dir $<) clean

.PHONY: print-%
print-%:
	@echo $*=$($*)

