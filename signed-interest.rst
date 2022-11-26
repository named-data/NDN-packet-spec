.. _Signed Interest:

Signed Interest
===============

**Signed Interest** is a mechanism to issue an authenticated Interest.

A signed Interest is an Interest where:

* Name ends with ``ParametersSha256DigestComponent``.
* ``InterestSignature`` is present.

See :ref:`InterestSignature` for details on the format of the ``InterestSignature`` element.

Construction of Signed Interests
--------------------------------

The following procedure describes the signing of an Interest:

#. Remove all ``ParametersSha256DigestComponent`` components from ``Name`` if present, regardless of the location.

#. If ``ApplicationParameters`` element is absent, append a zero-length ``ApplicationParameters`` element to the Interest.

#. Prepare an ``InterestSignatureInfo`` element and append it at the end of the Interest.

#. Compute the cryptographic signature according to the :ref:`InterestSignature` section.

#. Insert the computed signature as an ``InterestSignatureValue`` element at the end of the Interest.

#. Compute the ``ParametersSha256DigestComponent`` according to the :ref:`ParametersDigestComponent` section and append it at the end of ``Name``.

Processing of Signed Interests
------------------------------

Upon receiving an Interest, the producer, according to the Interest name prefix, should be able to tell whether the Interest is required to be signed.
If the received Interest is required to be signed, the application protocol or the producer should also explicitly define whether ``SignatureNonce``, ``SignatureTime``, and/or ``SignatureSeqNum`` must be present in ``InterestSignatureInfo`` or not.
If any of the required elements is missing, treat the Interest as invalid.
Additionally, a signed Interest must be treated as invalid if any of the following conditions is true:

#. The last name component is not ``ParametersSha256DigestComponent``, or its TLV-VALUE is incorrect according to the :ref:`ParametersDigestComponent` section.

#. The ``InterestSignatureInfo`` element is missing or any mandatory sub-element is missing from the ``InterestSignatureInfo`` element.

#. The ``InterestSignatureValue`` element is missing.

#. The signature cannot be cryptographically verified.

#. The key used to create the signature is not trusted for signing the Interest.

#. If ``SignatureTime`` (*t*) is present in the ``InterestSignatureInfo``:

   Lookup the last recorded ``SignatureTime`` (*t*\ :sub:`0`) used in conjunction with the same key.
   Use ``CurrentTime - GracePeriod`` if no previous record exists. The recommended grace period is 60 seconds.
   If *t*\ :sub:`0` >= *t*, consider the Interest as invalid.
   Set *t*\ :sub:`0` to *t* if the signed Interest has been validated according to this and all other rules.

   .. note::
      Sharing private keys is not recommended. If private key sharing is inevitable, it is the key owner's responsibility to keep clocks synchronized.

#. If ``SignatureNonce`` is present:

   To perform this check, the recipient must remember a list of ``SignatureNonce`` carried in previously received Signed Interests used in conjunction with the specific signing key.
   Check whether the ``SignatureNonce`` carried in the current signed Interest is a repetition of a recorded ``SignatureNonce`` used with the same key.
   If it is a repetition, treat the Interest as invalid.
   Add the newly received ``SignatureNonce`` into the ``SignatureNonce`` list if the signed Interest has been validated according to this and all other rules.

   .. note::
      The size of the ``SignatureNonce`` list and the lifetime of each ``SignatureNonce`` remembered by the receiver depend on the application protocol's need.

#. If ``SignatureSeqNum`` (*s*) is present:

   Lookup the last recorded ``SignatureSeqNum`` (*s*\ :sub:`0`) used in conjunction with the same key.
   If *s*\ :sub:`0` >= *s*, consider the Interest as invalid.
   If no previous record exists, check *s* against the application policy.
   If *s* does not satisfy the application policy, treat the signed Interest as invalid.
   Set *s*\ :sub:`0` to *s* if the signed Interest has been validated according to this and all other rules.

   .. note::
      The first ``SignatureSeqNum`` received is considered valid only if it satisfies the application's policy.
      For example, application can decide the first ``SeqNum`` can only be a minimum value like 0 or 1, or a value that both sender and receiver agree on.
