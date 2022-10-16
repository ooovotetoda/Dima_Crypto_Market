import json
from typing import Optional

from bipwallet import wallet
from hdwallet import HDWallet
from hdwallet.symbols import TRX as SYMBOL
from hdwallet.utils import generate_entropy, generate_mnemonic

global hdwallet


def gen_wallet():
    # Choose strength 128, 160, 192, 224 or 256
    STRENGTH: int = 128  # Default is 128

    # Choose language
    LANGUAGE: str = "english"  # Default is english

    # Generate new entropy hex string
    ENTROPY: str = generate_entropy(strength=STRENGTH)

    # Secret passphrase for mnemonic
    PASSPHRASE: Optional[str] = 'backwater'
    MNEMONIC: str = generate_mnemonic()

    # Initialize Bitcoin mainnet HDWallet
    hdwallet: HDWallet = HDWallet(symbol=SYMBOL, use_default_path=False)

    # Get HDWallet from entropy
    # hdwallet.from_entropy(
    #     entropy=ENTROPY, language=LANGUAGE, passphrase=PASSPHRASE
    # )

    # Get HDWallet from private_key
    # hdwallet.from_private_key('3b3c3bb15121f9935696b066e70609672aa98e262d128669247fdbe4cadd702f')

    # Get Bitcoin HDWallet from mnemonic
    hdwallet.from_mnemonic(mnemonic='gold climb sting above accuse awkward theme merit second lava salad short')

    # Derivation from path
    hdwallet.from_path("m/44'/195'/0'/0/0")
    hdwallet.xprivate_key()
    hdwallet.xpublic_key()
    hdwallet.private_key()
    hdwallet.public_key()
    # Print all Bitcoin HDWallet information's
    wald = hdwallet.dumps()
    print(wald, end='\n')
    with open('j_data.json', 'w') as a:
        a.write(json.dumps(hdwallet.dumps(), indent=4, ensure_ascii=False))


gen_wallet()
