CXX=g++

binaries: monte_carlo_π

monte_carlo_π: monte_carlo_π.cpp Makefile
	$(CXX) -o monte_carlo_π -O3 -fopenmp monte_carlo_π.cpp

clean:
	rm -f *.o  monte_carlo_π
