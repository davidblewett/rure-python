Python API for RUst's REgex engine
==================================
rure is the Python binding  Rust's regex library, which guarantees linear time
searching using finite automata. In exchange, it must give up some common
regex features such as backreferences and arbitrary lookaround. It does
however include capturing groups, lazy matching, Unicode support and word
boundary assertions. Its matching semantics generally correspond to Perl's,
or "leftmost first." Namely, the match locations reported correspond to the
first match that would be found by a backtracking engine.

The syntax and possibly other useful things are documented in the Rust
API documentation: http://doc.rust-lang.org/regex/regex/index.html


Examples
--------

This package presents 2 entry points to the regex engine: ``Rure``,
an OO wrapper of the underlying Rust API, and a drop-in replacement for the
stdlib ``re`` module (``compile``, ``search``, ``match``, ``findall``, ``finditer``,
``RegexObject`` and ``MatchObject``).

The ``Rure`` interface exposes the "pay for what you use" API, enabling
you to request the minimum computation you need: does the text match (``is_match``),
where does it match (``find``, ``find_iter``), and where are the submatches
(``captures``, ``captures_iter``).

The drop-in replacement should be as simple as ``import rure as re``,
and using the API as documented in the Python documentation
( https://docs.python.org/3/library/re.html , https://docs.python.org/2/library/re.html).
The flags supported by ``re`` are automatically translated to those
supported by ``rure``.

One important note regarding this shim: the Rust engine operates on
byte offsets in the given search text, while Python operates on Unicode
code points. The Rust engine guarantees returning offsets that correspond
to valid UTF8 segments. By default, the  ``MatchObject`` that is returned by
this library will decode the captured text. The offsets returned by ``start``,
``end``, and ``span``, however, are byte offsets and not character offsets.
Using them with the ``string`` attribute is safe, so you can do:

>>> email = u"tony@tiremove_thisger.net"
>>> m = re.search(u"remove_this", email)
>>> m.string[:m.start()] + m.string[m.end():].decode('utf8')
u'tony@tiger.net'

This package also includes an ``is_match(pattern, string, flags=0)`` function
(and corresponding method on ``RegexObject``), that only returns a boolean.


Performance
-----------
It's fast. Its core matching engine is a lazy DFA, which is what GNU grep
and RE2 use. Like GNU grep, this regex engine can detect multi byte literals
in the regex and will use fast literal string searching to quickly skip
through the input to find possible match locations.

All memory usage is bounded and all searching takes linear time with respect
to the input string.

For more details, see the PERFORMANCE guide:
https://github.com/rust-lang-nursery/regex/blob/master/PERFORMANCE.md


Missing
-------
There are a few things missing from this package that are present in the Rust API.
There's no particular (known) reason why they don't, they just haven't been
implemented yet.

* Splitting a string by a regex.
* Replacing regex matches in a string with some other text.


Install
-------
Binary wheels are provided for MacOS. The specific versions of the Rust
compiler, `rure` and `regex` crates will be available in the changelog.

Installing from a source tarball requires manually building the Rust `rure` crate and
pointing at the built directory. If you are wanting to take advantage of a modern CPU,
it's likely that you'll want to build the `regex` crate with SSE3 and SIMD. To do so,
you will need to update the `regex/regex-capi/Cargo.toml` to include the `simd-accel`
feature: `regex = { version = "0.2.2", path = "..", features=["simd-accel"] }`.

* git clone https://github.com/rust-lang-nursery/regex
* `cargo build --release --manifest-path /path/to/regex/regex-capi/Cargo.toml`

    * To build with SSE3: `RUSTFLAGS="-C target-feature=+ssse3" cargo build --release --features simd-accel`

* `RURE_DIR=/path/to/regex/regex-capi python setup.py bdist_wheel`
* `pip install rure --no-index -f ./dist`
