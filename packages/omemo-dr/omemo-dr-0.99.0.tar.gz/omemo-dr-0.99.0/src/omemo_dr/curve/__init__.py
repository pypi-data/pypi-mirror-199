from .. import _curve


def calculate_signature(random: bytes, privatekey: bytes, message: bytes) -> bytes:
    return _curve.calculateSignature(random, privatekey, message)


def verify_signature_curve(publickey: bytes, message: bytes, signature: bytes) -> int:
    return _curve.verifySignatureCurve(publickey, message, signature)


def verify_signature_ed(publickey: bytes, message: bytes, signature: bytes) -> int:
    return _curve.verifySignatureEd(publickey, message, signature)


def generate_private_key(random: bytes) -> bytes:
    return _curve.generatePrivateKey(random)


def generate_public_key(privatekey: bytes) -> bytes:
    return _curve.generatePublicKey(privatekey)


def calculate_agreement(privatekey: bytes, publickey: bytes) -> bytes:
    return _curve.calculateAgreement(privatekey, publickey)


def convert_curve_to_ed_pubkey(publickey: bytes) -> bytes:
    return _curve.convertCurveToEdPubkey(publickey)


def convert_ed_to_curve_pubkey(publickey: bytes) -> bytes:
    return _curve.convertEdToCurvePubkey(publickey)
