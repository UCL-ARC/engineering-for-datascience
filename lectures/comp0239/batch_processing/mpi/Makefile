CXX=mpic++

binaries: hello ring rung monte_carlo_π

hello: hello.cpp Makefile
	$(CXX) -o hello hello.cpp

ring: ring.cpp Makefile
	$(CXX) -o ring ring.cpp

rung: rung.cpp Makefile
	$(CXX) -o rung rung.cpp

monte_carlo_π: monte_carlo_π.cpp Makefile
	$(CXX) -o monte_carlo_π -O3 monte_carlo_π.cpp

clean:
	rm -f *.o  hello ring rung monte_carlo_π
