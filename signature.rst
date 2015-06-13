.. _Signature:

Signature
---------

NDN Signature is defined as two consecutive TLV blocks: ``SignatureInfo`` and ``SignatureValue``.
The following general considerations about SignatureInfo and SignatureValue blocks that apply for all signature types:

1. ``SignatureInfo`` is **included** in signature calculation and fully describes the signature, signature algorithm, and any other relevant information to obtain parent certificate(s), such as :ref:`KeyLocator`

2. ``SignatureValue`` is **excluded** from signature calculation and represent actual bits of the signature and any other supporting signature material.

The reason for separating the signature into two separate TLV blocks is to allow efficient signing of a contiguous memory block (e.g., for Data packet this block starts from Name TLV and ends with SignatureInfo TLV).

::

    Signature ::= SignatureInfo
                  SignatureValue

    SignatureInfo ::= SIGNATURE-INFO-TYPE TLV-LENGTH
                        SignatureType
                        KeyLocator?
                        ... (SignatureType-specific TLVs)

    SignatureValue ::= SIGNATURE-VALUE-TYPE TLV-LENGTH
                        ... (SignatureType-specific TLVs and
                        BYTE+

SignatureType
~~~~~~~~~~~~~

::

    SignatureType ::= SIGNATURE-TYPE-TYPE TLV-LENGTH
                        nonNegativeInteger


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
| 2,4-200 |                                        | reserved for future assignments                 |
+---------+----------------------------------------+-------------------------------------------------+
| >200    |                                        | unassigned                                      |
+---------+----------------------------------------+-------------------------------------------------+

.. +-------+----------------------------------------+-------------------------------------------------+
.. | 2     | :ref:`SignatureSha256WithRsaAndMerkle` | Integrity and provenance protection using       |
.. |       |                                        | RSA signature over SHA-256-Merkle-Hash digest.  |
.. |       |                                        |                                                 |
.. |       |                                        | This signature type defines an aggregated       |
.. |       |                                        | signing algorithm that reduces cost of signing  |
.. |       |                                        | of a large segmented content (e.g., video file).|


.. _KeyLocator:

KeyLocator
~~~~~~~~~~

A ``KeyLocator`` specifies either ``Name`` that points to another Data packet containing certificate or public key or ``KeyDigest`` to identify the public key within a specific trust model (the trust model definition is outside the scope of the current specification).
Note that although ``KeyLocator`` is defined as an optional field in ``SignatureInfo`` block, some signature types may require presence of it and some require ``KeyLocator`` absence.

::

    KeyLocator ::= KEY-LOCATOR-TYPE TLV-LENGTH (Name | KeyDigest)

    KeyDigest ::= KEY-DIGEST-TYPE TLV-LENGTH BYTE+

See :ref:`Name specification <Name>` for the definition of Name field.

The specific definition of the usage of ``Name`` and ``KeyDigest`` options in ``KeyLocator`` field is outside the scope of this specification.
Generally, ``Name`` names the Data packet with the corresponding certificate.
However, it is up to the specific trust model to define whether this name is a full name of the Data packet or a prefix that can match multiple Data packets.
For example, the hierarchical trust model :cite:`testbed-key-management` uses the latter approach, requiring clients to fetch the latest version of the Data packet pointed by the KeyLocator (the latest version of the public key certificate) in order to ensure that the public key was not yet revoked.

.. _DigestSha256:

DigestSha256
^^^^^^^^^^^^

``DigestSha256`` provides no provenance of a Data packet or any kind of guarantee that packet is from the original source.
This signature type is intended only for debug purposes and limited circumstances when it is necessary to protect only against unexpected modification during the transmission.

``DigestSha256`` is defined as a SHA256 hash of the :ref:`Name`, :ref:`MetaInfo`, :ref:`Content`, and :ref:`SignatureInfo <Signature>` TLVs:

::

    SignatureInfo ::= SIGNATURE-INFO-TYPE TLV-LENGTH(=3)
                        SIGNATURE-TYPE-TYPE TLV-LENGTH(=1) 0

    SignatureValue ::= SIGNATURE-VALUE-TYPE TLV-LENGTH(=32)
                         BYTE+(=SHA256{Name, MetaInfo, Content, SignatureInfo})

Note that ``SignatureInfo`` does not require ``KeyLocator`` field, since there digest calculation and verification does not require any additional information.
If ``KeyLocator`` is present in ``SignatureInfo``, it must be ignored.

.. _SignatureSha256WithRsa:

SignatureSha256WithRsa
^^^^^^^^^^^^^^^^^^^^^^

``SignatureSha256WithRsa`` is the basic signature algorithm that MUST be supported by any NDN-compliant software.
As suggested by the name, it defines an RSA public key signature that is calculated over SHA256 hash of the :ref:`Name`, :ref:`MetaInfo`, :ref:`Content`, and :ref:`SignatureInfo <Signature>` TLVs.


::

    SignatureInfo ::= SIGNATURE-INFO-TYPE TLV-LENGTH
                        SIGNATURE-TYPE-TYPE TLV-LENGTH(=1) 1
                        KeyLocator

    SignatureValue ::= SIGNATURE-VALUE-TYPE TLV-LENGTH
                         BYTE+(=RSA over SHA256{Name, MetaInfo, Content, SignatureInfo})

.. note::

   SignatureValue size varies (typically 128 or 256 bytes) depending on the private key length used during the signing process.

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

::

    SignatureInfo ::= SIGNATURE-INFO-TYPE TLV-LENGTH
                        SIGNATURE-TYPE-TYPE TLV-LENGTH(=1) 3
                        KeyLocator

    SignatureValue ::= SIGNATURE-VALUE-TYPE TLV-LENGTH
                         BYTE+(=ECDSA over SHA256{Name, MetaInfo, Content, SignatureInfo})

.. note::

   The SignatureValue size depends on the private key length used during the signing process (about 63 bytes for a 224 bit key).

This type of signature ensures strict provenance of a Data packet, provided that the signature verifies and the signature issuer is authorized to sign the Data packet.
The signature issuer is identified using the :ref:`KeyLocator` block in the :ref:`SignatureInfo <Signature>` block of the ``SignatureSha256WithEcdsa``.
KeyDigest option in ``KeyLocator`` is defined as SHA256 digest over the DER encoding of the SubjectPublicKeyInfo for an EC key as defined by `RFC 5480 <http://www.ietf.org/rfc/rfc5480.txt>`_.
See the :ref:`KeyLocator section <KeyLocator>` for more detail.

The value of ``SignatureValue`` of ``SignatureSha256WithEcdsa`` is a DER encoded DSA signature as defined in `Section 2.2.3 in RFC 3279 <http://tools.ietf.org/html/rfc3279#section-2.2.3>`_.

::

    Ecdsa-Sig-Value  ::=  SEQUENCE  {
         r     INTEGER,
         s     INTEGER  }

.. .. _SignatureSha256WithRsaAndMerkle:

.. SignatureSha256WithRsaAndMerkle
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. ::

..     SignatureInfo ::= SIGNATURE-INFO-TYPE TLV-LENGTH
..                         SIGNATURE-TYPE-TYPE TLV-LENGTH(=1) 2
..                         KeyLocator

..     SignatureValue ::= SIGNATURE-VALUE-TYPE TLV-LENGTH
..                        BYTE+(=RSA over SHA256{Name, MetaInfo, Content, SignatureInfo})
..                        Witness

..     Witness ::= WITNESS-TYPE TLV-LENGTH BYTE+

.. bibliography:: ndnspec-refs.bib
