#!/bin/bash
set -e -x

## Update Rust
. /root/.cargo/env
rustup update

### Build rure
## Clone upstream repos
cd /opt/regex
git pull
git checkout "${REGEX_TAG}"
## Kick off cargo build of regex-capi (rure)
cargo build --release --manifest-path /opt/regex/regex-capi/Cargo.toml

## Compile wheels
for PYBIN in /opt/python/*/bin; do
    #${PYBIN}/pip install -r /io/dev-requirements.txt
    ${PYBIN}/pip wheel /io/ -w /io/wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in /io/wheelhouse/rure*.whl; do
    auditwheel repair $whl -w /io/wheelhouse/
done

## Install packages and test
for PYBIN in /opt/python/*/bin/; do
    ${PYBIN}/pip install rure --no-index -f /io/wheelhouse
    (cd $HOME; ${PYBIN}/nosetests rure)
done
