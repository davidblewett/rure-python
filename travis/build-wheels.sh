#!/bin/bash
set -e -x

# Install latest stable Rust
curl https://sh.rustup.rs -sSf | sh
. /root/.cargo/env

# Clone upstream repos
git clone git://github.com/rust-lang-nursery/regex
# Kick off cargo build of regex-capi (rure)
cargo build --release --manifest-path ./regex/regex-capi/Cargo.toml
# Stage build directory where setuptools expects
ln -s ./regex/regex-capi/target ./rure/

# Install a system package required by our library
#yum install -y atlas-devel

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    ${PYBIN}/pip install -r /io/dev-requirements.txt
    ${PYBIN}/pip wheel /io/ -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair $whl -w /io/wheelhouse/
done

# Install packages and test
for PYBIN in /opt/python/*/bin/; do
    ${PYBIN}/pip install python-manylinux-demo --no-index -f /io/wheelhouse
    (cd $HOME; ${PYBIN}/nosetests pymanylinuxdemo)
done
