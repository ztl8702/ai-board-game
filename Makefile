SUBMISSION = parta.py ai_part_1_dfs.py common.py

submission: $(SUBMISSION)
	tar -czvf tlua-tianleiz1.tar.gz $(SUBMISSION)

test:
	python3 test.py