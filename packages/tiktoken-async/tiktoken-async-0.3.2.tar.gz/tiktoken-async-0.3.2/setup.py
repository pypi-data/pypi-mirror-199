from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    name="tiktoken_async",
    rust_extensions=[
        RustExtension(
            "tiktoken_async._tiktoken",
            binding=Binding.PyO3,
            # Between our use of editable installs and wanting to use Rust for performance sensitive
            # code, it makes sense to just always use --release
            debug=False,
        )
    ],
    package_data={"tiktoken_async": ["py.typed"]},
    packages=["tiktoken_async", "tiktoken_async_ext"],
    zip_safe=False,
)
