from __future__ import annotations

from ..ecc.curve import Curve
from ..ecc.ec import ECPublicKey
from ..kdf.hkdf import HKDF
from ..state.sessionstate import SessionState
from ..util.byteutil import ByteUtil
from .aliceaxolotlparameters import AliceAxolotlParameters
from .bobaxolotlparamaters import BobAxolotlParameters
from .chainkey import ChainKey
from .rootkey import RootKey


class RatchetingSession:
    @staticmethod
    def initializeSessionAsAlice(
        sessionState: SessionState,
        sessionVersion: int,
        parameters: AliceAxolotlParameters,
    ) -> None:
        sessionState.setSessionVersion(sessionVersion)
        sessionState.setRemoteIdentityKey(parameters.getTheirIdentityKey())
        sessionState.setLocalIdentityKey(parameters.getOurIdentityKey().getPublicKey())

        sendingRatchetKey = Curve.generateKeyPair()
        secrets = bytearray()

        if sessionVersion >= 3:
            secrets.extend(RatchetingSession.getDiscontinuityBytes())

        secrets.extend(
            Curve.calculateAgreement(
                parameters.getTheirSignedPreKey(),
                parameters.getOurIdentityKey().getPrivateKey(),
            )
        )
        secrets.extend(
            Curve.calculateAgreement(
                parameters.getTheirIdentityKey().getPublicKey(),
                parameters.getOurBaseKey().getPrivateKey(),
            )
        )
        secrets.extend(
            Curve.calculateAgreement(
                parameters.getTheirSignedPreKey(),
                parameters.getOurBaseKey().getPrivateKey(),
            )
        )

        if sessionVersion >= 3 and parameters.getTheirOneTimePreKey() is not None:
            secrets.extend(
                Curve.calculateAgreement(
                    parameters.getTheirOneTimePreKey(),
                    parameters.getOurBaseKey().getPrivateKey(),
                )
            )

        derivedKeys = RatchetingSession.calculateDerivedKeys(sessionVersion, secrets)
        sendingChain = derivedKeys.getRootKey().createChain(
            parameters.getTheirRatchetKey(), sendingRatchetKey
        )

        sessionState.addReceiverChain(
            parameters.getTheirRatchetKey(), derivedKeys.getChainKey()
        )
        sessionState.setSenderChain(sendingRatchetKey, sendingChain[1])
        sessionState.setRootKey(sendingChain[0])

    @staticmethod
    def initializeSessionAsBob(
        sessionState: SessionState,
        sessionVersion: int,
        parameters: BobAxolotlParameters,
    ) -> None:
        sessionState.setSessionVersion(sessionVersion)
        sessionState.setRemoteIdentityKey(parameters.getTheirIdentityKey())
        sessionState.setLocalIdentityKey(parameters.getOurIdentityKey().getPublicKey())

        secrets = bytearray()

        if sessionVersion >= 3:
            secrets.extend(RatchetingSession.getDiscontinuityBytes())

        secrets.extend(
            Curve.calculateAgreement(
                parameters.getTheirIdentityKey().getPublicKey(),
                parameters.getOurSignedPreKey().getPrivateKey(),
            )
        )

        secrets.extend(
            Curve.calculateAgreement(
                parameters.getTheirBaseKey(),
                parameters.getOurIdentityKey().getPrivateKey(),
            )
        )
        secrets.extend(
            Curve.calculateAgreement(
                parameters.getTheirBaseKey(),
                parameters.getOurSignedPreKey().getPrivateKey(),
            )
        )

        if sessionVersion >= 3 and parameters.getOurOneTimePreKey() is not None:
            secrets.extend(
                Curve.calculateAgreement(
                    parameters.getTheirBaseKey(),
                    parameters.getOurOneTimePreKey().getPrivateKey(),
                )
            )

        derivedKeys = RatchetingSession.calculateDerivedKeys(sessionVersion, secrets)
        sessionState.setSenderChain(
            parameters.getOurRatchetKey(), derivedKeys.getChainKey()
        )
        sessionState.setRootKey(derivedKeys.getRootKey())

    @staticmethod
    def getDiscontinuityBytes() -> bytearray:
        return bytearray([0xFF] * 32)

    @staticmethod
    def calculateDerivedKeys(sessionVersion: int, masterSecret: bytes) -> DerivedKeys:
        if sessionVersion <= 3:
            domain_separator = "WhisperText"
        else:
            domain_separator = "OMEMO Payload"
        kdf = HKDF(sessionVersion)
        derivedSecretBytes = kdf.deriveSecrets(
            masterSecret, bytearray(domain_separator.encode()), 64
        )
        derivedSecrets = ByteUtil.split(derivedSecretBytes, 32, 32)
        return RatchetingSession.DerivedKeys(
            RootKey(kdf, derivedSecrets[0]), ChainKey(kdf, derivedSecrets[1], 0)
        )

    @staticmethod
    def isAlice(ourKey: ECPublicKey, theirKey: ECPublicKey) -> bool:
        return ourKey < theirKey

    class DerivedKeys:
        def __init__(self, rootKey: RootKey, chainKey: ChainKey):
            self.rootKey = rootKey
            self.chainKey = chainKey

        def getRootKey(self):
            return self.rootKey

        def getChainKey(self):
            return self.chainKey
