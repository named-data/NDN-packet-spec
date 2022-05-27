Signature
=========

.. _DataSignature:

Data Signature
--------------

The NDN Data packet signature is defined as two consecutive TLV elements: ``SignatureInfo`` and ``SignatureValue``.

::

    DataSignature = SignatureInfo SignatureValue

    SignatureInfo = SIGNATURE-INFO-TYPE TLV-LENGTH
                      SignatureType
                      [KeyLocator]

    SignatureValue = SIGNATURE-VALUE-TYPE TLV-LENGTH *OCTET

The ``SignatureInfo`` element fully describes the digital signature algorithm utilized and any other relevant information to locate its parent certificate(s), such as :ref:`KeyLocator`.

The ``SignatureValue`` element holds the actual bits of the signature. The exact encoding of the TLV-VALUE of this element depends on the specific signature type. See :ref:`SignatureTypes` for details.

The cryptographic signature contained in ``SignatureValue`` covers all TLV elements inside ``Data``, starting from ``Name`` and up to, but not including, ``SignatureValue``.
These TLV elements are hereby referred to as the "*signed portion*" of a Data packet.


.. _InterestSignature:

Interest Signature
------------------

The NDN Interest packet signature is defined as two consecutive TLV elements: ``InterestSignatureInfo`` and ``InterestSignatureValue``.

::

    InterestSignature = InterestSignatureInfo InterestSignatureValue

    InterestSignatureInfo = INTEREST-SIGNATURE-INFO-TYPE TLV-LENGTH
                              SignatureType
                              [KeyLocator]
                              [SignatureNonce]
                              [SignatureTime]
                              [SignatureSeqNum]

    InterestSignatureValue = INTEREST-SIGNATURE-VALUE-TYPE TLV-LENGTH *OCTET

The ``InterestSignatureInfo`` element fully describes the digital signature algorithm utilized and any other relevant information to locate its parent certificate(s), such as :ref:`KeyLocator`.
To ensure the uniqueness of a signed Interest and to mitigate potential replay attacks, the ``InterestSignatureInfo`` element SHOULD include at least one of the following elements (described below): ``SignatureNonce``, ``SignatureTime``, ``SignatureSeqNum``.

The ``InterestSignatureValue`` element holds the actual bits of the signature. The exact encoding of the TLV-VALUE of this element depends on the specific signature type. See :ref:`SignatureTypes` for details.

The cryptographic signature contained in ``InterestSignatureValue`` covers all the ``NameComponent`` elements in the Interest's ``Name`` up to, but not including, ``ParametersSha256DigestComponent``, and the complete TLV elements starting from ``ApplicationParameters`` up to, but not including, ``InterestSignatureValue``.
These TLV elements are hereby referred to as the "*signed portion*" of an Interest packet.


Signature Elements
------------------

SignatureType
^^^^^^^^^^^^^

::

    SignatureType = SIGNATURE-TYPE-TYPE TLV-LENGTH NonNegativeInteger

This specification defines the following values for ``SignatureType``:

+---------+----------------------------------------+-------------------------------------------------+
| Value   | Reference                              | Description                                     |
+=========+========================================+=================================================+
| 0       | :ref:`DigestSha256`                    | Integrity protection using a SHA-256 digest     |
+---------+----------------------------------------+-------------------------------------------------+
| 1       | :ref:`SignatureSha256WithRsa`          | Integrity and provenance protection using       |
|         |                                        | an RSA signature over a SHA-256 digest          |
+---------+----------------------------------------+-------------------------------------------------+
| 3       | :ref:`SignatureSha256WithEcdsa`        | Integrity and provenance protection using       |
|         |                                        | an ECDSA signature over a SHA-256 digest        |
+---------+----------------------------------------+-------------------------------------------------+
| 4       | :ref:`SignatureHmacWithSha256`         | Integrity and provenance protection using       |
|         |                                        | a SHA-256 hash-based message authentication code|
+---------+----------------------------------------+-------------------------------------------------+
| 5       | :ref:`SignatureEd25519`                | Integrity and provenance protection using       |
|         |                                        | an Ed25519 signature                            |
+---------+----------------------------------------+-------------------------------------------------+
| 2,6-200 |                                        | Reserved for future assignments                 |
+---------+----------------------------------------+-------------------------------------------------+
| >200    |                                        | Unassigned                                      |
+---------+----------------------------------------+-------------------------------------------------+

.. _KeyLocator:

KeyLocator
^^^^^^^^^^

A ``KeyLocator`` specifies either a ``Name`` that points to another Data packet containing a certificate or public key, or a ``KeyDigest`` that identifies the public key within a specific trust model (definition of the trust model is outside the scope of this specification).
Note that although ``KeyLocator`` is defined as an optional field in ``SignatureInfo`` and ``InterestSignatureInfo``, specific signature types may require its presence or absence.

::

    KeyLocator = KEY-LOCATOR-TYPE TLV-LENGTH (Name / KeyDigest)

    KeyDigest = KEY-DIGEST-TYPE TLV-LENGTH *OCTET

See :ref:`Name specification <Name>` for the definition of ``Name``.

The specific definition of the proper usage of the ``Name`` and ``KeyDigest`` options in the ``KeyLocator`` field is outside the scope of this specification.
Generally, ``Name`` names the Data packet containing the corresponding certificate.
However, it is up to the specific trust model to define whether this name is the full name of the Data packet or a prefix that can match multiple Data packets.
For example, the `hierarchical trust model`_ uses the latter approach, requiring clients to fetch the latest version of the Data packet pointed to by ``KeyLocator`` (the latest version of the public key certificate) in order to ensure that the public key was not yet revoked.

SignatureNonce
^^^^^^^^^^^^^^

::

    SignatureNonce = SIGNATURE-NONCE-TYPE TLV-LENGTH 1*OCTET

The ``SignatureNonce`` element adds additional assurances that a signature will be unique.
The recommended minimum length for a ``SignatureNonce`` element is 8 octets.

SignatureTime
^^^^^^^^^^^^^

::

    SignatureTime = SIGNATURE-TIME-TYPE TLV-LENGTH NonNegativeInteger

The value of the ``SignatureTime`` element is the timestamp of the signature, represented as the number of milliseconds since 1970-01-01T00:00:00Z (Unix epoch).
This element can be used to indicate that the packet was signed at a particular point in time.

SignatureSeqNum
^^^^^^^^^^^^^^^

::

    SignatureSeqNum = SIGNATURE-SEQ-NUM-TYPE TLV-LENGTH NonNegativeInteger

The ``SignatureSeqNum`` element adds additional assurances that a signature will be unique.
The ``SignatureSeqNum`` may be used to protect against replay attacks.


.. _SignatureTypes:

Different Types of Signatures
-----------------------------

Each signature type has different requirements on the format of its ``SignatureInfo`` and ``InterestSignatureInfo`` elements.
In the following sections, these requirements are specified along 2 dimensions:

* The TLV-VALUE of ``SignatureType``
* Whether ``KeyLocator`` is required/forbidden

.. _DigestSha256:

DigestSha256
^^^^^^^^^^^^

``DigestSha256`` provides no information about the provenance of a packet or any guarantee that the packet is from the original source.
This signature type is intended only for debug purposes and in the limited circumstances when it is necessary to protect only against unexpected modification during transmission.

``DigestSha256`` is defined as the SHA-256 hash of the "signed portion" of an Interest or Data packet:

* The TLV-VALUE of ``SignatureType`` is 0
* ``KeyLocator`` is forbidden; if present, it must be ignored

::

    SignatureValue = SIGNATURE-VALUE-TYPE
                     TLV-LENGTH ; == 32
                     32OCTET ; == SHA-256{Data signed portion}

    InterestSignatureValue = INTEREST-SIGNATURE-VALUE-TYPE
                             TLV-LENGTH ; == 32
                             32OCTET ; == SHA-256{Interest signed portion}

.. _SignatureSha256WithRsa:

SignatureSha256WithRsa
^^^^^^^^^^^^^^^^^^^^^^

``SignatureSha256WithRsa`` defines an RSA public key signature that is calculated over the SHA-256 hash of the "signed portion" of an Interest or Data packet.
It uses the RSASSA-PKCS1-v1_5 signature scheme, as defined in :rfc:`RFC 8017, Section 8.2 <8017#section-8.2>`.

* The TLV-VALUE of ``SignatureType`` is 1
* ``KeyLocator`` is required

::

    SignatureValue = SIGNATURE-VALUE-TYPE
                     TLV-LENGTH
                     1*OCTET ; == RSA over SHA-256{Data signed portion}

    InterestSignatureValue = INTEREST-SIGNATURE-VALUE-TYPE
                             TLV-LENGTH
                             1*OCTET ; == RSA over SHA-256{Interest signed portion}

.. note::
   The TLV-LENGTH of these elements varies depending on the length of the private key used for signing (e.g., 256 bytes for a 2048-bit key).

This type of signature, if verified, provides very strong assurances that a packet was created by the claimed producer (authentication/provenance) and was not tampered with while in transit (integrity).
The ``KeyDigest`` option in :ref:`KeyLocator` is defined as the SHA-256 digest over the DER encoding of the ``SubjectPublicKeyInfo`` for an RSA key as defined by :rfc:`3279`.

.. note::
   It is the application's responsibility to define rules (a trust model) concerning when a specific issuer (``KeyLocator``) is authorized to sign a specific packet.
   While trust models are outside the scope of this specification, generally, trust models need to specify authorization rules between key names and Data packet names, as well as clearly define trust anchor(s).
   For example, an application can elect to use a `hierarchical trust model`_ to ensure Data integrity and provenance.

.. _SignatureSha256WithEcdsa:

SignatureSha256WithEcdsa
^^^^^^^^^^^^^^^^^^^^^^^^

``SignatureSha256WithEcdsa`` defines an ECDSA public key signature that is calculated over the SHA-256 hash of the "signed portion" of an Interest or Data packet.
This signature algorithm is defined in :rfc:`RFC 5753, Section 2.1 <5753#section-2.1>`.
All NDN implementations MUST support this signature type with the NIST P-256 curve.

* The TLV-VALUE of ``SignatureType`` is 3
* ``KeyLocator`` is required

::

    SignatureValue = SIGNATURE-VALUE-TYPE
                     TLV-LENGTH
                     1*OCTET ; == ECDSA over SHA-256{Data signed portion}

    InterestSignatureValue = INTEREST-SIGNATURE-VALUE-TYPE
                             TLV-LENGTH
                             1*OCTET ; == ECDSA over SHA-256{Interest signed portion}

.. note::
   The TLV-LENGTH of these elements depends on the specific elliptic curve used for signing (e.g., up to 72 bytes for the NIST P-256 curve).

This type of signature, if verified, provides very strong assurances that a packet was created by the claimed producer (authentication/provenance) and was not tampered with while in transit (integrity).
The ``KeyDigest`` option in :ref:`KeyLocator` is defined as the SHA-256 digest of the DER encoding of the ``SubjectPublicKeyInfo`` for an EC key as defined by :rfc:`5480`.

The value of ``SignatureValue`` of ``SignatureSha256WithEcdsa`` is a DER-encoded ``Ecdsa-Sig-Value`` structure as defined in :rfc:`RFC 3279, Section 2.2.3 <3279#section-2.2.3>`.

.. _SignatureHmacWithSha256:

SignatureHmacWithSha256
^^^^^^^^^^^^^^^^^^^^^^^

``SignatureHmacWithSha256`` defines a hash-based message authentication code (HMAC) that is calculated over the "signed portion" of an Interest or Data packet, using SHA-256 as the hash function, salted with a shared secret key.
This signature algorithm is defined in :rfc:`RFC 2104, Section 2 <2104#section-2>`.

.. warning::
   As stated in :rfc:`RFC 2104, Section 3 <2104#section-3>`, shared keys shorter than the SHA-256 output length (32 bytes) are strongly discouraged.

* The TLV-VALUE of ``SignatureType`` is 4
* ``KeyLocator`` is required

::

    SignatureValue = SIGNATURE-VALUE-TYPE
                     TLV-LENGTH ; == 32
                     32OCTET ; == HMAC-SHA-256{Data signed portion}

    InterestSignatureValue = INTEREST-SIGNATURE-VALUE-TYPE
                             TLV-LENGTH ; == 32
                             32OCTET ; == HMAC-SHA-256{Interest signed portion}

Provided that the signature verifies, this type of signature ensures the authenticity of the packet, namely, that it was signed by a party possessing the shared key, and that it was not altered in transit (integrity).
The shared key used to generate the HMAC signature can be identified by the :ref:`KeyLocator` element, e.g., by using the ``Name`` according to the application's naming conventions.
It is the application's responsibility to associate the shared key with the identities of the parties who hold the shared key.

.. danger::
   The shared secret key is not included in the signature and must not be included anywhere in the packet, as this would invalidate the security properties of HMAC.

.. _SignatureEd25519:

SignatureEd25519
^^^^^^^^^^^^^^^^

``SignatureEd25519`` defines an Ed25519 public key signature that is calculated over the "signed portion" of an Interest or Data packet.
This signature algorithm is defined in :rfc:`RFC 8032, Section 5.1 <8032#section-5.1>`.

* The TLV-VALUE of ``SignatureType`` is 5
* ``KeyLocator`` is required

::

    SignatureValue = SIGNATURE-VALUE-TYPE
                     TLV-LENGTH
                     64OCTET ; == Ed25519{Data signed portion}

    InterestSignatureValue = INTEREST-SIGNATURE-VALUE-TYPE
                             TLV-LENGTH
                             64OCTET ; == Ed25519{Interest signed portion}

This type of signature, if verified, provides very strong assurances that a packet was created by the claimed producer (authentication/provenance) and was not tampered with while in transit (integrity).
The ``KeyDigest`` option in :ref:`KeyLocator` is defined as the SHA-256 digest over the DER encoding of the ``SubjectPublicKeyInfo`` for an Ed25519 key as defined by :rfc:`RFC 8410, Section 4 <8410#section-4>`.

.. _hierarchical trust model: https://named-data.net/publications/techreports/trpublishkey-rev2/
