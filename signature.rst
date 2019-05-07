Signature
=========

.. _Signature:

Data Signature
--------------

NDN Data Signature is defined as two consecutive TLV blocks: ``SignatureInfo`` and ``SignatureValue``.
The following general considerations about SignatureInfo and SignatureValue blocks that apply for all signature types:

1. ``SignatureInfo`` is **included** in signature calculation and fully describes the signature, signature algorithm, and any other relevant information to obtain parent certificate(s), such as :ref:`KeyLocator`.

2. ``SignatureValue`` is **excluded** from signature calculation and represent actual bits of the signature and any other supporting signature material.

The reason for separating the signature into two separate TLV blocks is to allow efficient signing of a contiguous memory block (e.g., for Data packet this block starts from Name TLV and ends with SignatureInfo TLV).

::

    DataSignature = SignatureInfo SignatureValue

    SignatureInfo = SIGNATURE-INFO-TYPE TLV-LENGTH
                      SignatureType
                      [KeyLocator]

    SignatureValue = SIGNATURE-VALUE-TYPE TLV-LENGTH *OCTET

.. _InterestSignature:

Interest Signature
------------------

NDN Interest Signature is defined as two consecutive TLV blocks: ``InterestSignatureInfo`` and ``InterestSignatureValue``.

To ensure uniqueness of the signed Interest name and to mitigate potential replay attacks, the ``InterestSignatureInfo`` element can include a ``SignatureNonce`` element, ``SignatureTime`` element, and/or ``SignatureSeqNum`` element.

The cryptographic signature in the ``InterestSignatureValue`` element covers all the ``NameComponent`` elements inside ``Name`` up to but not including ``ParametersSha256DigestComponent`` component, and the complete TLVs starting from ``ApplicationParameters`` up until but not including ``InterestSignatureValue``.


::

    InterestSignature = InterestSignatureInfo InterestSignatureValue

    InterestSignatureInfo = INTEREST-SIGNATURE-INFO-TYPE TLV-LENGTH
                              SignatureType
                              [KeyLocator]
                              [SignatureNonce]
                              [SignatureTime]
                              [SignatureSeqNum]

    InterestSignatureValue = INTEREST-SIGNATURE-VALUE-TYPE TLV-LENGTH *OCTET

Signature Elements
------------------

SignatureType
~~~~~~~~~~~~~

::

    SignatureType = SIGNATURE-TYPE-TYPE TLV-LENGTH nonNegativeInteger


This specification defines the following SignatureType values:

+---------+----------------------------------------+-------------------------------------------------+
| Value   | Reference                              | Description                                     |
+=========+========================================+=================================================+
| 0       | :ref:`DigestSha256`                    | Integrity protection using SHA-256 digest       |
+---------+----------------------------------------+-------------------------------------------------+
| 1       | :ref:`SignatureSha256WithRsa`          | Integrity and provenance protection using       |
|         |                                        | RSA signature over a SHA-256 digest             |
+---------+----------------------------------------+-------------------------------------------------+
| 3       | :ref:`SignatureSha256WithEcdsa`        | Integrity and provenance protection using       |
|         |                                        | an ECDSA signature over a SHA-256 digest        |
+---------+----------------------------------------+-------------------------------------------------+
| 4       | :ref:`SignatureHmacWithSha256`         | Integrity and provenance protection using       |
|         |                                        | SHA256 hash-based message authentication codes  |
+---------+----------------------------------------+-------------------------------------------------+
| 2,5-200 |                                        | reserved for future assignments                 |
+---------+----------------------------------------+-------------------------------------------------+
| >200    |                                        | unassigned                                      |
+---------+----------------------------------------+-------------------------------------------------+

.. _KeyLocator:

KeyLocator
~~~~~~~~~~

A ``KeyLocator`` specifies either ``Name`` that points to another Data packet containing certificate or public key or ``KeyDigest`` to identify the public key within a specific trust model (the trust model definition is outside the scope of the current specification).
Note that although ``KeyLocator`` is defined as an optional field in ``SignatureInfo`` block, some signature types may require presence of it and some require ``KeyLocator`` absence.

::

    KeyLocator = KEY-LOCATOR-TYPE TLV-LENGTH (Name / KeyDigest)

    KeyDigest = KEY-DIGEST-TYPE TLV-LENGTH *OCTET

See :ref:`Name specification <Name>` for the definition of Name field.

The specific definition of the usage of ``Name`` and ``KeyDigest`` options in ``KeyLocator`` field is outside the scope of this specification.
Generally, ``Name`` names the Data packet with the corresponding certificate.
However, it is up to the specific trust model to define whether this name is a full name of the Data packet or a prefix that can match multiple Data packets.
For example, the hierarchical trust model :cite:`testbed-key-management` uses the latter approach, requiring clients to fetch the latest version of the Data packet pointed by the KeyLocator (the latest version of the public key certificate) in order to ensure that the public key was not yet revoked.

.. _SignatureInfoNonce:

SignatureNonce
~~~~~~~~~~~~~~

::

    SignatureNonce = SIGNATURE-NONCE-TYPE
                     TLV-LENGTH ; == 4
                     4OCTET


The ``SignatureNonce`` element adds additional assurances that a signature will be unique.

.. _SignatureTime:

SignatureTime
~~~~~~~~~~~~~

::

    SignatureTime = SIGNATURE-TIME-TYPE TLV-LENGTH nonNegativeInteger


The value of the ``SignatureTime`` element is the signature's timestamp (in terms of milliseconds since 1970-01-01 00:00:00 UTC) encoded as nonNegativeInteger.
The ``SignatureTime`` element may be used to protect against replay attacks.

.. _SignatureSeqNum:

SignatureSeqNum
~~~~~~~~~~~~~~~

::

    SignatureSeqNum = SIGNATURE-SEQ-NUM-TYPE TLV-LENGTH nonNegativeInteger


The ``SignatureSeqNum`` element adds additional assurances that a signature will be unique.
The ``SignatureSeqNum`` may be used to protect against replay attacks.


Different Types of Signature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each signature type has different requirements on the format of its ``SignatureInfo`` or ``InterestSignatureInfo`` element.
In the following sections, these requirements are specified along 2 dimensions:

* The TLV-VALUE of ``SignatureType``
* ``KeyLocator`` is required/forbidden

.. _DigestSha256:

DigestSha256
^^^^^^^^^^^^

``DigestSha256`` provides no provenance of a Data packet or any kind of guarantee that packet is from the original source.
This signature type is intended only for debug purposes and limited circumstances when it is necessary to protect only against unexpected modification during the transmission.

``DigestSha256`` is defined as a SHA256 hash of the :ref:`Name`, :ref:`MetaInfo`, :ref:`Content`, and :ref:`SignatureInfo <Signature>` TLVs:

* The TLV-VALUE of ``SignatureType`` is 0
* ``KeyLocator`` is forbidden; if present, it must be ignored

::

    SignatureValue = SIGNATURE-VALUE-TYPE
                     TLV-LENGTH ; == 32
                     32OCTET ; == SHA256{Name, MetaInfo, Content, SignatureInfo}

    InterestSignatureValue = INTEREST-SIGNATURE-VALUE-TYPE
                             TLV-LENGTH ; == 32
                             32OCTET ; == SHA256{Name(without T, L, and ParametersSha256DigestComponent),
                                     ;           ApplicationParameters, InterestSignatureInfo}

.. _SignatureSha256WithRsa:

SignatureSha256WithRsa
^^^^^^^^^^^^^^^^^^^^^^

``SignatureSha256WithRsa`` is the basic signature algorithm that MUST be supported by any NDN-compliant software.
As suggested by the name, it defines an RSA public key signature that is calculated over SHA256 hash of the :ref:`Name`, :ref:`MetaInfo`, :ref:`Content`, and :ref:`SignatureInfo <Signature>` TLVs.

* The TLV-VALUE of ``SignatureType`` is 1
* ``KeyLocator`` is required

::

    SignatureValue = SIGNATURE-VALUE-TYPE TLV-LENGTH
                       *OCTET ; == RSA over SHA256{Name, MetaInfo, Content, SignatureInfo}

    InterestSignatureValue = INTEREST-SIGNATURE-VALUE-TYPE TLV-LENGTH
                               *OCTET ; == RSA over SHA256{Name(without T, L, and ParametersSha256DigestComponent),
                                                           ApplicationParameters, InterestSignatureInfo}

.. note::

   The TLV-LENGTH of these elements varies (typically 128 or 256 bytes) depending on the private key length used during the signing process.

This type of signature ensures strict provenance of a Data packet, provided that the signature verifies and signature issuer is authorized to sign the Data packet.
The signature issuer is identified using :ref:`KeyLocator` block in :ref:`SignatureInfo <Signature>` block of ``SignatureSha256WithRsa``.
KeyDigest option in ``KeyLocator`` is defined as SHA256 digest over the DER encoding of the SubjectPublicKeyInfo for an RSA key as defined by `RFC 3279 <http://www.rfc-editor.org/rfc/rfc3279.txt>`_."
See :ref:`KeyLocator section <KeyLocator>` for more detail.

.. note::

    It is application's responsibility to define rules (trust model) of when a specific issuer (KeyLocator) is authorized to sign a specific Data packet.
    While trust model is outside the scope of the current specification, generally, trust model needs to specify authorization rules between KeyName and Data packet Name, as well as clearly define trust anchor(s).
    For example, an application can elect to use hierarchical trust model :cite:`testbed-key-management` to ensure Data integrity and provenance.

.. _SignatureSha256WithEcdsa:

SignatureSha256WithEcdsa
^^^^^^^^^^^^^^^^^^^^^^^^

``SignatureSha256WithEcdsa`` defines an ECDSA public key signature that is calculated over the SHA256 hash of the :ref:`Name`, :ref:`MetaInfo`, :ref:`Content`, and :ref:`SignatureInfo <Signature>` TLVs.
The signature algorithm is defined in `[RFC5753], Section 2.1 <http://tools.ietf.org/html/rfc5753#section-2.1>`_.

* The TLV-VALUE of ``SignatureType`` is 3
* ``KeyLocator`` is required

::

    SignatureValue = SIGNATURE-VALUE-TYPE TLV-LENGTH
                       *OCTET ; == ECDSA over SHA256{Name, MetaInfo, Content, SignatureInfo}

    InterestSignatureValue = INTEREST-SIGNATURE-VALUE-TYPE TLV-LENGTH
                               *OCTET ; == ECDSA over SHA256{Name(without T, L, and ParametersSha256DigestComponent),
                                                             ApplicationParameters, InterestSignatureInfo}

.. note::

   The TLV-LENGTH of these elements depends on the elliptic curve used during the signing process (about 63 bytes for a 224 bit key).

This type of signature ensures strict provenance of a Data packet, provided that the signature verifies and the signature issuer is authorized to sign the Data packet.
The signature issuer is identified using the :ref:`KeyLocator` block in the :ref:`SignatureInfo <Signature>` block of the ``SignatureSha256WithEcdsa``.
KeyDigest option in ``KeyLocator`` is defined as SHA256 digest over the DER encoding of the SubjectPublicKeyInfo for an EC key as defined by `RFC 5480 <http://www.ietf.org/rfc/rfc5480.txt>`_.
See the :ref:`KeyLocator section <KeyLocator>` for more detail.

The value of ``SignatureValue`` of ``SignatureSha256WithEcdsa`` is a DER encoded ECDSA signature as defined in `Section 2.2.3 in RFC 3279 <http://tools.ietf.org/html/rfc3279#section-2.2.3>`_.

::

    Ecdsa-Sig-Value  ::=  SEQUENCE  {
         r     INTEGER,
         s     INTEGER  }

.. _SignatureHmacWithSha256:

SignatureHmacWithSha256
^^^^^^^^^^^^^^^^^^^^^^^

``SignatureHmacWithSha256`` defines a hash-based message authentication code (HMAC) that is calculated over the :ref:`Name`, :ref:`MetaInfo`, :ref:`Content`, and :ref:`SignatureInfo <Signature>` TLVs, using SHA256 as the hash function, salted with a shared secret key.
The signature algorithm is defined in `Section 2 in RFC 2104 <http://tools.ietf.org/html/rfc2104#section-2>`__.

* The TLV-VALUE of ``SignatureType`` is 4
* ``KeyLocator`` is required

::

    SignatureValue = SIGNATURE-VALUE-TYPE
                     TLV-LENGTH ; == 32
                     32OCTET ; == HMAC{Name, MetaInfo, Content, SignatureInfo}

    InterestSignatureValue = INTEREST-SIGNATURE-VALUE-TYPE
                             TLV-LENGTH ; == 32
                             32OCTET ; == HMAC{Name(without T, L, and ParametersSha256DigestComponent),
                                               ApplicationParameters, InterestSignatureInfo}

.. note::

   The shared secret key is not included in the signature and must not be included anywhere in the data packet, as it would invalidate security properties of HMAC.

.. note::

   As stated in `Section 3 of RFC 2104 <http://tools.ietf.org/html/rfc2104#section-3>`__, shared keys shorter than the SHA256 output byte length (32 bytes) are strongly discouraged.

Provided that the signature verifies, this type of signature ensures provenance that the Data packet was signed by one of the parties who holds the shared key.
The shared key used to generate HMAC signature can be identified by the :ref:`KeyLocator` block in :ref:`SignatureInfo <Signature>`, e.g., by using the ``Name`` according to application's naming conventions.
It is the application's responsibility to establish association between the shared key and the identities of the parties who hold the shared key.

.. bibliography:: ndnspec-refs.bib
