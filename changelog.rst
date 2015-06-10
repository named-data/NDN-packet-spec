Changes
=======

Since version 0.1.1
-------------------

- **Name**

  + Allow zero-length name component
  + Require implicit digest to be specified using ``ImplicitSha256Digest`` name component

- **Interest**

  + Delete deprecated ``Scope`` guider

Since version 0.1
-----------------

- **Signature**

  + New ``SignatureSha256WithEcdsa`` signature type for Elliptic Curve Digital Signature Algorithm (ECDSA).
  + ``KeyLocatorDigest`` renamed to ``KeyDigest``.  The specification now explicitly allows KeyDigest to be a SHA256 of any type of the key.
  + ``KeyLocator`` field is now defined to be optionally present in generic ``SignatureInfo`` block.
    ``SignatureSha256WithRsa`` and ``SignatureSha256WithEcdsa`` still require ``KeyLocator`` to be always present.

Since CCNx 0.7.2
----------------

- **General**

  + XML-based ccnb packet encoding is replaced by TLV encoding

- **Name**

  + The name encoding is changed from binary XML to TLV format
  + The discussions on naming conventions and the use of special markers inside NameComponents are removed from packet specification, and will be covered by a separate technical document
  + Deprecated zero-length name component

- **Interest Packet**

  + ``Nonce`` is changed from optional to required
  + ``PublisherPublicKeyDigest`` is replaced by ``PublisherPublicKeyLocator``
  + ``AnswerOriginKind`` is simplified from 4bits to a 1-bit ``MustBeFresh``
  + ``FaceID`` has been removed
  + ``InterestLifetime`` changes the unit to the number of milliseconds
  + Removed Bloom Filter from Exclude
  + Changed default semantics of staleness

    Specifically, NDN-TLV Interest without any selectors will bring any data that matches the name, and only when ``MustBeFresh`` selector is enabled it will try to honor freshness, specified in Data packets.
    With Binary XML encoded Interests, the default behavior was to bring "fresh" data and return "stale" data only when ``AnswerOriginKind`` was set to 3.

    Application developers must be aware of this change, reexamine the Interest expression code, and enable ``MustBeFresh`` selector when necessary.

- **Data Packet**

  + The structure of Data packet is changed:

    * ``Name``, ``MetaInfo``, ``Content``, ``Signature{SignatureInfo, SignatureValue}``

  + ``SignedInfo`` is renamed to ``MetaInfo`` and its content is changed
  + ``PublisherPublicKeyDigest`` and ``ExtOpt`` are removed.
  + ``Timestamp`` is removed
  + ``KeyLocator`` is moved to be inside the ``Signature`` (``SignatureInfo``) block
  + Three content types, ENCR, GONE, and NACK are removed
  + ``FreshnessSeconds`` is renamed to ``FreshnessPeriod`` and is expressed in units of milliseconds

- **Signature**

  + ``Signature`` is moved to the end of Data packet.
  + ``KeyLocator`` is moved to be a part of the ``SignatureInfo`` block, if it is applicable for the specific signature type.

    The rationale for the move is to make Signature (sequence of ``SignatureInfo`` and ``SignatureValue`` TLVs) self-contained and self-sufficient.

  + Signature type (or signing method information) is expressed as an assigned integer value (with no assumed default), rather than OID.
  + Added support for hash-only "signature"
  + The current specification does not define Merkle Hash Tree Aggregated Signatures, but it is expected that such (or similar) signatures will be defined in future version of this specification
