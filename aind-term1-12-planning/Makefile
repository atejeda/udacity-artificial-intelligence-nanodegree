DOCS=heuristic_analysis research_review

all:
	@for doc in ${DOCS}; do pandoc $$doc.md -o $$doc.pdf; done;
clean:
	@for doc in ${DOCS}; do rm -f $$doc.pdf; done;

