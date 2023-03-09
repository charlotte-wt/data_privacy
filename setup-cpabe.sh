ls

apt-get update

# Install dependencies
apt-get -y install libssl-dev
apt-get -y install libgtk-3-dev
apt-get -y install libgmp-dev
apt-get -y install pkg-config

apt-get -y install bison
apt-get -y install flex

# Setup pbc-0.5.14
echo "pbc-0.5.14 setup"
cd /usr/src/pbc-0.5.14
sh ./configure
make
make install
echo "ldconfig pbc"
ldconfig

# Setup libbswabe-0.9
echo "libbswabe setup"
cd /usr/src/libbswabe-0.9
sh ./configure
make
make install
ldconfig

# Setup cpabe-0.11
cd /usr/src/cpabe-0.11
make
make install
ldconfig

# Check if installation successful
cpabe-setup -h