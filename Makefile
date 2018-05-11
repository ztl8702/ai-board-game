# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = comp30024
SOURCEDIR     = docs
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	rm -rf ./**/__pycache__/ && \
	rm -rf ./submission
	
submit:
	mkdir ./submission && \
	cp -r ./ai ./submission/ && \
	cp ./*_player.py ./submission && \
	cp ./bakeoff.py ./submission && \
	cp ./perf.py ./submission && \
	cp ./comments.txt ./submission && \
	cp ./wyb-online.zip ./submission