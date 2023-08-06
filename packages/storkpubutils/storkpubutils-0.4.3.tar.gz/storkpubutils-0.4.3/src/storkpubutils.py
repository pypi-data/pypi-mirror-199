import decimal
import json
import os
import sys
import statistics
import time
import uuid

from dotenv import load_dotenv
from eth_abi.packed import encode_abi_packed
from eth_account.messages import encode_defunct
from eth_utils import keccak
from web3.auto import w3

from starkware_helpers.signature import get_price_msg, sign

from aptos_sdk.account import Account
from aptos_sdk.bcs import Serializer

import logging
from watchtower import CloudWatchLogHandler

import hashlib

load_dotenv()


def setup_lib(
    oracle_name,
    starkex_private_key,
    evm_address,
    evm_private_key,
    aptos_address = None,
    aptos_private_key = None,
    enable_cloudwatch_logs = False,
    cloudwatch_log_group = None,
    cloudwatch_log_stream = None,
):
    '''
    Setup constants for the lib to use.

    :param oracle_name: oracle name string
    :param starkex_private_key: private key used to generate stark signed price
    :param evm_address: evm address used for signing
    :param evm_private_key: private key used to generate evm signed price
    :param aptos_address: aptos address used for signing
    :param aptos_private_key: private key used to generate aptos signed price
    :param cloudwatch_log_group: AWS Cloudwatch log group to send messages to
    :param cloudwatch_log_stream: AWS Cloudwatch log stream (within cloudwatch_log_group) to send messages to
    '''

    global ORACLE_NAME, ORACLE_NAME_HEX, ORACLE_NAME_INT, STARKEX_PRIVATE_KEY, EVM_ADDRESS, EVM_PRIVATE_KEY, APTOS_ADDRESS, APTOS_PRIVATE_KEY, STABLECOIN_THRESHOLD, LOG_PARAMS

    ORACLE_NAME = oracle_name
    ORACLE_NAME_HEX = ORACLE_NAME.encode("utf-8").hex()
    ORACLE_NAME_INT = int(ORACLE_NAME_HEX, 16)
    STARKEX_PRIVATE_KEY = starkex_private_key
    EVM_ADDRESS = evm_address
    EVM_PRIVATE_KEY = evm_private_key
    APTOS_ADDRESS = aptos_address
    APTOS_PRIVATE_KEY = aptos_private_key
    STABLECOIN_THRESHOLD = 0.25 # maximum allowed deviation from parity for stablecoins

    init_logger(enable_cloudwatch_logs, cloudwatch_log_group, cloudwatch_log_stream)


def init_logger(enable_cloudwatch_logs, cloudwatch_log_group, cloudwatch_log_stream):
    """
    Init the global root logger and set default console handler and, if applicable, AWS Cloudwatch.

    :param enable_cloudwatch_logs: Whether or not to enable sending logs to Cloudwatch
    :param cloudwatch_log_group: AWS Cloudwatch log group to send messages to
    :param cloudwatch_log_stream: AWS Cloudwatch log stream (within cloudwatch_log_group) to send messages to
    """
    global root_logger

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(stream_handler)

    if enable_cloudwatch_logs and bool(cloudwatch_log_group) and bool(cloudwatch_log_stream):
        cw_handler = CloudWatchLogHandler(
            log_group_name=cloudwatch_log_group,
            log_stream_name=cloudwatch_log_stream,
            create_log_group=False,
        )
        cw_handler.setLevel(logging.INFO)
        root_logger.addHandler(cw_handler)
        root_logger.info(f"Cloudwatch logs enabled: log_group = {cloudwatch_log_group}, log_stream = {cloudwatch_log_stream}")
    else:
        root_logger.info("Cloudwatch logs not enabled")

    root_logger.info("Oracle started")


def starkex_sign(external_asset_padded, timestamp, external_price):
    """
    Starkex signs the given asset and price

    :param external_asset_padded: external asset being signed
    :param timestamp: timestamp of function invocation
    :param external_price: external price of given asset
    :return signed: returns struct for starkex with signature, timestamp, and hash
    """
    data = get_price_msg(ORACLE_NAME_INT, external_asset_padded, timestamp, external_price)
    r, s = sign(data, int(STARKEX_PRIVATE_KEY, 16))
    signed = {"signature": {"r": hex(r), "s": hex(s)}, "timestamp": str(timestamp), "msg_hash": str(hex(data))}
    return signed


def evm_pack(asset_pair: str, timestamp: int, price: int):
    """
    Equivalent to StarkEx's get_price_msg without hashing

    :param asset_pair: asset pair for the given price
    :param timestamp: timestamp of function invocation
    :param price: price of given asset-pair
    :return encode_defunct(hash): returns encoded hash for signing
    """
    concat_hash = keccak(encode_abi_packed(["address", "string", "uint256", "uint256"], [EVM_ADDRESS, asset_pair, timestamp, price]))
    return encode_defunct(concat_hash)


def evm_sign(asset, timestamp, external_price):
    """
    EVM signs the given asset and price

    :param asset: name of asset for the given external_price
    :param timestamp: timestamp of when the signing function is invoked
    :param external_price: price of given asset
    :return signed: returns struct with signature, timestamp, and hash
    """
    evm_packed_hash = evm_pack(asset, timestamp, external_price)
    signed_evm_message = w3.eth.account.sign_message(evm_packed_hash, private_key=EVM_PRIVATE_KEY)
    signature = {"r": hex(signed_evm_message.r), "s": hex(signed_evm_message.s), "v": hex(signed_evm_message.v)}
    signed = {"signature": signature, "timestamp": str(timestamp), "msg_hash": "0x" + evm_packed_hash.body.hex()}
    return signed


def aptos_sign(asset, timestamp, external_price):
    """
    Signs the given asset and price with an Aptos-Move compliant ed25519 signature

    :param asset: name of asset for the given external_price
    :param timestamp: timestamp of when the signing function is invoked
    :param external_price: price of given asset
    :return signed: returns struct with signature, timestamp, and hash
    """
    def build_aptos_msg_hash(aptos_address, asset, timestamp, external_price):
        hash = hashlib.sha3_256()
        hash.update(b"APTOS::RawTransaction")
        prefix_hash = hash.digest()

        hash = hashlib.sha3_256()
        ser = Serializer()
        ser.str(aptos_address)
        ser.str(asset)
        ser.u128(timestamp)
        ser.u128(external_price)
        hash.update(ser.output())
        msg_hash = hash.digest()

        return prefix_hash + msg_hash

    acct = Account.load_key(APTOS_PRIVATE_KEY)
    msg_hash = build_aptos_msg_hash(APTOS_ADDRESS, asset, timestamp, external_price)
    signature = acct.sign(msg_hash)
    signed = {"signature": "0x" + signature.signature.hex(), "timestamp": str(timestamp), "msg_hash": "0x" + msg_hash.hex()}
    return signed


def sign_prices(asset, external_price):
    """
    Signs the given asset price using the provider's private key

    :param asset: name of asset (e.g. BTCUSD)
    :param external_price: asset price to sign
    :return starkex_signed_price, evm_signed_price, aptos_signed_price: returns objects containing signed price dicts
    """
    now = time.time()
    timestamp = int(now)
    asset_hex = asset.encode("utf-8").hex()
    external_asset_padded_hex = "0x" + asset_hex + (32 - len(asset_hex)) * "0"

    stark_signed_price = {
        "external_asset_id": external_asset_padded_hex + ORACLE_NAME_HEX,
        "price": str(external_price),
    }
    evm_signed_price = stark_signed_price.copy()

    external_asset_padded = int(external_asset_padded_hex, 16)
    stark_signed_price["timestamped_signature"] = starkex_sign(external_asset_padded, timestamp, external_price)

    evm_signed_price["external_asset_id"] = asset
    evm_signed_price["timestamped_signature"] = evm_sign(asset, timestamp, external_price)

    if APTOS_ADDRESS and APTOS_PRIVATE_KEY:
        aptos_signed_price = evm_signed_price.copy()
        aptos_signed_price["timestamped_signature"] = aptos_sign(asset, timestamp, external_price)
        return stark_signed_price, evm_signed_price, aptos_signed_price

    return stark_signed_price, evm_signed_price


async def send(stork_endpoint, asset, starkex_signed_price, evm_signed_price, aptos_signed_price = None):
    """
    This function takes the give oracle and price data, and forwards it to the stork websocket

    :param stork_endpoint: stork websocket connection
    :param asset: name of asset (e.g. BTCUSD)
    :param starkex_signed_price: price value signed using starkex
    :param evm_signed_prices: price value signed using evm
    :param aptos_signed_price: price value signed using aptos
    """
    correlation_id = str(uuid.uuid4())
    message = {
        "action": "price_update",
        "oracle_name": ORACLE_NAME,
        "asset": asset,
        "signed_price": starkex_signed_price,
        "evm_signed_price": evm_signed_price,
        "correlation_id": correlation_id,
    }
    if aptos_signed_price:
        message["aptos_signed_price"] = aptos_signed_price

    root_logger.debug(f"Sending message for asset {asset} to stork, {correlation_id}.")
    await stork_endpoint.send(json.dumps(message))


def median_price_update(close, prices, total, current_exchange, current_asset):
    """
    This function updates the given price dict and returns the median price for the given asset.

    :param close: close price of the given asset
    :param prices: dict containing prices of various assets
    :param total: array that stores current exchange prices for the given asset
    :param current_exchange: current exchange (e.g. cbse)
    :param current_asset: current asset (e.g. BTCUSD)
    :returns external_price: returns the calculated external price if data is valid

    Structure for the `prices` object is as follows:
    prices[]: Array containing asset names
    asset: Dict containing exchange namesb/values mapped to price objects
    current_exchange: set containing price and timestamp of price update

    Overall: prices[current_asset:{current_exchange:{"price":price, "timstamp":time}}]
    """
    if current_asset in prices:
        prices[current_asset].update(
            {
                current_exchange: {
                    "price": close,
                    "timestamp": int(time.time()),
                }
            }
        )
    else:
        # Add new entry if exchange data does not exist
        prices.update(
            {
                current_asset: {
                    current_exchange: {
                        "price": close,
                        "timestamp": int(time.time()),
                    }
                }
            }
        )

    # Remove data older than 10 seconds
    for exch in list(prices[current_asset]):
        timestamp = prices[current_asset][exch]["timestamp"]
        exch_price = prices[current_asset][exch]["price"]
        if (int(time.time()) - timestamp) < 10:
            total.append(exch_price)
        else:
            del prices[current_asset][exch]

    # Calculate and return the median price
    if len(total) > 0:
        median_price = statistics.median(total)
        return median_price


def quantize_price(median_price, exponent=18):
    """
    This function takes a given median price, and quantizes it to avoid float imprecisions.

    :param median_price: given median asset price
    :param exponent: optional param defines the exponent when multiplying(default = 18)
    :returns external_price: returns price after quantizing and multiplying by exponent
    """
    decimal_price = decimal.Decimal(median_price)
    quantized_price = decimal_price.quantize(decimal.Decimal("0.0001"))
    external_price = int(quantized_price * (10**exponent))

    return external_price


def parse_env_vars(var_name):
    """
    This function takes a given environment variable name, and parses it from the .env file

    :param var_name: given key of environment variable, which corresponds to a hex value stored in the .env file
    :returns parsed_var: returns env var converted into hexadecimal
    """
    parsed_var = hex(int(os.getenv(var_name), 16))

    return parsed_var


def store_exchange_asset_timestamp(last_updates, asset, exchange, exchange_timestamp):
    exchange_asset_time_update = {"last_time": exchange_timestamp}
    exchange_body = last_updates.get(exchange)

    if not bool(exchange_body):
        last_updates.update({exchange: {asset: exchange_asset_time_update}})
        return

    exchange_body[asset] = exchange_asset_time_update
    last_updates.update({exchange: exchange_body})


def can_skip_update(current_asset, median_price, last_updates, exchange=None, exchange_timestamp=None):
    """
    This function checks the last_updates object to verify if a new update is needed to be sent or not.
    Uses a 10 basis points and 5 second check to decide whether or not to send a new update.
    Also checks whether timestamp coming from exchange is a newer price than one previously received
    for a given exchange/asset pair

    :param current_asset: name of current asset being checked
    :param median_price: current median price of the given asset
    :param last_updates: stores the median and timestamp value of the last update for each asset sent by stork
    :returns bool: returns true if update should be ignored, and false if the update should be sent
    """
    if bool(exchange) and bool(exchange_timestamp):
        # check for existing data and compare
        if (
            bool(exchange_data := last_updates.get(exchange)) and
            bool(exchange_asset_data := exchange_data.get(current_asset)) and
            exchange_timestamp <= (t := exchange_asset_data["last_time"])
        ):
            return True

    last_median = last_updates[current_asset]["last_update"]["last_median"]
    last_time = last_updates[current_asset]["last_update"]["last_time"]
    if (int(time.time()) - last_time) < 5 and abs((median_price / last_median) - 1) < 0.001:
        return True

    return False

def convert_to_usd(price, current_quote, exchange_rates):
    """
    This function converts price from current_quote to USD based on exchange_rates, or returns None.

    :param price: price of current asset
    :param current_quote: the quote currency of the current asset
    :param exchange_rates: dict containing exchange rates for various assets
    :returns float: returns the converted price if data is valid, or None if data is invalid
    """
    if current_quote in exchange_rates:
        exchange_rate = exchange_rates[current_quote]

        # this is a sanity check to make sure the exchange rate is not too far off
        if abs(exchange_rate - 1) > STABLECOIN_THRESHOLD:
            return None

        return float(price) * exchange_rate
    else:
        root_logger.info(f"No exchange rate for {current_quote} to USD")
        return None