from google.protobuf.message import DecodeError

from ..ecc.curve import Curve
from ..exceptions import InvalidKeyException
from ..exceptions import InvalidMessageException
from ..identitykey import IdentityKey
from . import omemo_pb2 as omemoprotos
from .ciphertextmessage import CiphertextMessage
from .omemo_message import OMEMOMessage


class OMEMOKeyExchange(CiphertextMessage):
    def __init__(
        self,
        messageVersion=None,
        registrationId=None,
        preKeyId=None,
        signedPreKeyId=None,
        ecPublicBaseKey=None,
        identityKey=None,
        omemo_message=None,
        serialized=None,
    ):
        if serialized:
            try:
                omemo_keyexchange = omemoprotos.OMEMOKeyExchange()
                omemo_keyexchange.ParseFromString(serialized)

                if (
                    omemo_keyexchange.spk_id is None
                    or not omemo_keyexchange.ek
                    or not omemo_keyexchange.ik
                    or not omemo_keyexchange.message
                ):
                    raise InvalidMessageException("Incomplete message")

                self.serialized = serialized
                self.preKeyId = omemo_keyexchange.pk_id
                self.signedPreKeyId = omemo_keyexchange.spk_id

                self.baseKey = Curve.decodePoint(bytearray(omemo_keyexchange.ek), 0)

                self.identityKey = IdentityKey(
                    Curve.decodePoint(bytearray(omemo_keyexchange.ik), 0)
                )

                self.message = OMEMOMessage(serialized=omemo_keyexchange.message)

            except (InvalidKeyException, DecodeError) as error:
                raise InvalidMessageException(str(error))

        else:
            self.preKeyId = preKeyId
            self.signedPreKeyId = signedPreKeyId
            self.baseKey = ecPublicBaseKey
            self.identityKey = identityKey
            self.message = omemo_message

            keyexchange = omemoprotos.OMEMOKeyExchange()
            keyexchange.spk_id = signedPreKeyId
            keyexchange.pk_id = preKeyId
            keyexchange.ek = ecPublicBaseKey.serialize()
            keyexchange.ik = identityKey.serialize()
            keyexchange.message = omemo_message.serialize()

            self.serialized = keyexchange.SerializeToString()

    def getMessageVersion(self):
        return 4

    def getIdentityKey(self):
        return self.identityKey

    def getRegistrationId(self):
        return self.registrationId

    def getPreKeyId(self):
        return self.preKeyId

    def getSignedPreKeyId(self):
        return self.signedPreKeyId

    def getBaseKey(self):
        return self.baseKey

    def getWhisperMessage(self):
        return self.message

    def serialize(self):
        return self.serialized

    def getType(self):
        return CiphertextMessage.PREKEY_TYPE
