build:
	clang++ -o eva `llvm-config --cxxflags --ldflags --system-libs --libs core` evallvm.cpp
	
run:
	./eva
	lli ./out.ll
