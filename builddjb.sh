tar xzf djbdns-1.05.tar.gz
cd djbdns-1.05/
make dns.a env.a libtai.a alloc.a buffer.a unix.a byte.a iopause.o
./makelib iopause.a iopause.o
cd ..
