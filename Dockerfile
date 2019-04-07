FROM quay.io/pypa/manylinux1_x86_64
COPY --from=rust:latest /usr/local/cargo/ /usr/local/cargo/
COPY --from=rust:latest /usr/local/rustup/ /usr/local/rustup/

WORKDIR /root/
COPY . .

ENV CARGO_HOME=/usr/local/cargo \
    PATH="/usr/local/cargo/bin:/opt/python/cp37-cp37m/bin:$PATH" \
    RUSTUP_HOME=/usr/local/rustup

RUN rustc --version && \
    cargo --version

RUN python setup.py bdist_wheel && \
    pip install dist/*.whl
