.. _Signed Interest:

Signed Interest
===============

**Signed Interest** is a mechanism to issue an authenticated Interest.

A signed Interest is an Interest where:

* Name ends with ``ParametersSha256DigestComponent``.
* ``InterestSignature`` is present.

See :ref:`Interest Signature section <InterestSignature>` for details on ``InterestSignature``.

Construction of Signed Interest
-------------------------------

The following procedure describes the signing of an Interest:

1. Remove all ``ParametersSha256DigestComponent`` components from ``Name`` if present, regardless of the location.

2. If ``ApplicationParameters`` element is absent, append a zero-length ``ApplicationParameters`` element to the Interest.

3. Prepare an ``InterestSignatureInfo`` element and append it at the end of the Interest.

4. Compute the cryptographic signature according to :ref:`Interest Signature section <InterestSignature>`.

5. Insert the computed signature as an ``InterestSignatureValue`` element at the end of the Interest.

6. Compute the ``ParametersSha256DigestComponent`` according to :ref:`Interest Parameters Digest Component <Interest Parameters Digest Component>` section and append it at the end of ``Name``.

Signed Interest processing
--------------------------

Upon receiving an Interest, the producer, according to the Interest name prefix, should be able to tell whether the Interest is required to be signed.
If the received Interest is required to be signed, the application protocol or the producer should also explicitly define whether ``SignatureNonce``/``SignatureTime``/``SignatureSeqNum`` must be present in the ``InterestSignatureInfo`` or not.
If any of the required elements is missing, treat the Interest as invalid.
Additionally, a signed Interest must be treated as invalid if any of the following conditions is true:

1. The last name component is not ``ParametersSha256DigestComponent``, or its TLV-VALUE is incorrect according to :ref:`Interest Parameters Digest Component <Interest Parameters Digest Component>` section.

2. The ``InterestSignatureInfo`` element is missing or any mandatory sub-element is missing from the ``InterestSignatureInfo`` element.

3. The ``InterestSignatureValue`` element is missing.

4. The signature cannot be cryptographically verified.

5. The key used to create the signature is not trusted for signing the Interest.

6. If ``SignatureTime`` (`t`) is present in the ``InterestSignatureInfo``:

   Lookup the last recorded ``SignatureTime`` (`t0`) used in conjunction with the same key. Use ``CurrentTime - GracePeriod`` if no previous record exists. The recommended grace period is 60 seconds.
   If `t0` >= `t`, consider the Interest as invalid.
   Update `t0` to `t` if the signed Interest has been validated according to this and all other rules.

  .. note::
     Sharing private keys is not recommended. If private key sharing is inevitable, it is the key owner's responsibility to keep clocks synchronized.

7. If ``SignatureNonce`` is present:

   To perform this check, the recipient must remember a list of ``SignatureNonce`` carried in previously received Signed Interests used in conjunction with the specific signing key.
   Check whether the ``SignatureNonce`` carried in the current signed Interest is a repetition of a recorded ``SignatureNonce`` used with the same key.
   If it is a repetition, treat the Interest as invalid.
   Add the newly received ``SignatureNonce`` into the ``SignatureNonce`` list if the signed Interest has been validated according to this and all other rules.

  .. note::
     The size of the ``SignatureNonce`` list and the lifetime of each ``SignatureNonce`` remembered by the receiver depend on the application protocol's need.

8. If ``SignatureSeqNum`` (`s`) is present:

   Lookup the last recorded ``SignatureSeqNum`` (`s0`) used in conjunction with the same key. If `s0` >= `s`, consider the Interest as invalid.
   If no previous record exists, check `s` against the application policy.
   If `s` does not satisfy the application policy, treat the signed Interest as invalid.
   Update `s0` to `s` if the signed Interest has been validated according to this and all other rules.

  .. note::
     The first ``SignatureSeqNum`` received is considered valid only if it satisfies the application's policy. For example, application can decide the first ``SeqNum`` can only be a minimum value like 0 or 1, or a value that both sender and receiver agree on.
