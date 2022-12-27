# Generate lib
gcc -fPIC -Ofast -c lib.c
gcc -shared -Ofast -o ../bin/lib.so lib.o

# Remove intermediate file
rm lib.o