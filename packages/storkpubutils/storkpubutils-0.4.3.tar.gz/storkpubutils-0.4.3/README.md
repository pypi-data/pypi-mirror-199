# storkpubutils

## Usage

This package contains commonly used stork publisher utilities.

`sign_prices` uses `starkware_helpers` to generate starkware and evm signatures for the given asset and external price.

`send` takes the current asset and price data, and forwards it to the stork websocket.

`update_prices` takes price data from providers and stores it inside of a `prices` object, while also removing stale data.

`quantize_price` takes the given price and quantizes it before multiplying it to avoid float inaccuracies

`starkex_sign` and `evm_sign` take given assets and prices, and sign them with the relevant information

`evm_pack` is equivalent to StarkEx's `get_price_msg` without hashing

## Notes
Only folders with `__init__.py` in it them will be included when built.
