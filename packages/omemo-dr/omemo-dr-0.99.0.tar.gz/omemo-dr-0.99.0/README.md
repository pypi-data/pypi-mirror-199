Initial codebase was forked from https://github.com/tgalal/python-axolotl

This is a python port of [libsignal-protocol-java](https://github.com/WhisperSystems/libaxolotl-android) originally written by [Moxie Marlinspike](https://github.com/moxie0)


# Dependencies

 - [protobuf 3.0+](https://github.com/google/protobuf/)
 - [cryptography](https://cryptography.io)

## Linux

```
pip install .
```

# Usage

This python port is done in an almost 1:1 mapping to the original java code. Therefore any original documentation for the java code can be easily mapped and used with this python port.

## Install time

At install time, a libaxolotl client needs to generate its identity keys, registration id, and
prekeys.

```python
    identityKeyPair = KeyHelper.generateIdentityKeyPair()
    registrationId  = KeyHelper.generateRegistrationId()
    preKeys         = KeyHelper.generatePreKeys(startId, 100)
    lastResortKey   = KeyHelper.generateLastResortKey()
    signedPreKey    = KeyHelper.generateSignedPreKey(identityKeyPair, 5)

    #Store identityKeyPair somewhere durable and safe.
    #Store registrationId somewhere durable and safe.

    #Store preKeys in PreKeyStore.
    #Store signed prekey in SignedPreKeyStore.
```

## Building a session

A libaxolotl client needs to implement four interfaces: IdentityKeyStore, PreKeyStore, 
SignedPreKeyStore, and SessionStore.  These will manage loading and storing of identity, 
prekeys, signed prekeys, and session state.

Once those are implemented, building a session is fairly straightforward:

```python
sessionStore      = MySessionStore()
preKeyStore       = MyPreKeyStore()
signedPreKeyStore = MySignedPreKeyStore()
identityStore     = MyIdentityKeyStore()

# Instantiate a SessionBuilder for a remote recipientId + deviceId tuple.
sessionBuilder = SessionBuilder(sessionStore, preKeyStore, signedPreKeyStore,
                                                   identityStore, recipientId, deviceId)

# Build a session with a PreKey retrieved from the server.
sessionBuilder.process(retrievedPreKey)

sessionCipher = SessionCipher(sessionStore, recipientId, deviceId)
message       = sessionCipher.encrypt("Hello world!")

deliver(message.serialize())
```

# Development

## Generating protobuf files

Download the protobuf-compiler and execute

`protoc -I=omemo_dr/protobuf --python_out=omemo_dr/protobuf OMEMO.proto WhisperTextProtocol.proto LocalStorageProtocol.proto`
