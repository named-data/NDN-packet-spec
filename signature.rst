.. _signature:

Signature
---------

.. code-block:: none

    Signature ::= SIGNATURE-TYPE TLV-LENGTH
                    ( DigestSha256 |
                      SignatureSha256WithRsa |
                      SignatureSha256WithRsaAndMerkle |
                      ... 
                    )

Signature TLV is a general container of signature, which contains an inner signature TLV. 
The type field of the inner signature TLV indicates the signing method of the signature, for example,

- ``DigestSha256`` indicates that the integrity of Data is protected by a SHA-256 digest in ``DigestSha256``;

- ``SignatureSha256WithRsa`` indicates that the integrity and provenacne of Data is protected by a RSA signature over a SHA-256 digest;

- ``SignatureSha256WithRsaAndMerkle`` indicates that the integrity and provenance of Data is protected by a RSA signature over SHA-256-Merkle-Hash digest.

If some other types of signatures are required, a new inner signature TLV will be defined.


For each inner signature TLV, the last embedded TLV must be a SignatureBits TLV, for example:

.. code-block:: none

    DigestSha256 ::= DIGEST-SHA256-TYPE TLV-LENGTH(=32) SignatureBits(=BYTE[32])
    
    SignatureSha256WithRsa ::= SIGNATURE-SHA256-WITH-RSA-TYPE TLV-LENGTH
                                 KeyLocator
                                 SignatureBits(=BYTE[32])
    
    SignatureSha256WithRsaAndMerkle ::= SIGNATURE-SHA256-WITH-RSA-AND-MERKLE-TYPE 
                                        TLV-LENGTH
                                          KeyLocator
                                          Witness
                                          SignatureBits(=BYTE[32])

Which fields are covered by the ``SignatureBits`` TLV is up to the signing mechanism.
A valid signing mechanism, however, must cover following TLVs: Name, MetaInfo (if present), and Content.
Some signing mechansims may also require the SignatureBits TLV to cover more TLVs.
For example, ``SignatureSha256WithRsa`` requires the KeyLocator TLV to be signed, 
and ``SignatureSha256WithRsaAndMerkle`` requires both KeyLocator TLV and Witness TLV to be signed.

For inner signature TLVs that use public key cryptography, the first embedded TLV must be a KeyLocator TLV, e.g., as shown in ``SignatureSha256WithRsa`` and ``SignatureSha256WithRsaAndMerkle`` above.

.. code-block:: none

    KeyLocator ::= KEY-LOCATOR-TYPE TLV-LENGTH CertificateName |
                   (other types of KeyLocators)
    CertificateName ::= CERTIFICATE-NAME-TYPE TLV-LENGTH Name

A KeyLocator tells where to find the public key to verify this Data packet. 
For example, one can specify the name of the certificate of the public key (by CertificateName).
Name conventions can be used to find the name of the key for a piece of content from the name of the Data packet.

All the other embedded TLVs in an inner signature TLV (such as Witness) are the signature-specific meta information and may vary from a signature type to another.

Changes from CCNx
~~~~~~~~~~~~~~~~~

- ``Signature`` is moved to the end of Data packet.

- ``KeyLocator`` is moved to be an inner signature block, making the inner signature block self-contained and self-sufficient.

- Signature type (or signing method information) is expressed by the type of inner signature TLV, rather than OID.

- Added support for cheaper signatures

