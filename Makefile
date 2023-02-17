clean:
	python3 file_j_write.py 

build:
	python3 working.py -r

run:
	python3 working.py -r & python3 test_new\ \(1\).py 

default: clean build run