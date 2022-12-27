# Generate lib
gcc -fPIC -Ofast -c ./c/main.c
gcc -shared -Ofast -o ./bin/libsolver.so main.o

# Remove intermediate file
rm main.o