Changes
=======

Version 0.3
-----------

- Rewrite TLV syntax specifications using `IETF Augmented BNF (RFC 5234) <https://tools.ietf.org/html/rfc5234>`__

- Require shortest encoding for TLV-TYPE and TLV-LENGTH numbers

- **Interest**

  + Remove ``Selectors`` element
  + Add optional ``CanBePrefix`` element after Name
  + Move optional ``MustBeFresh`` element after ``CanBePrefix``
  + Move optional ``ForwardingHint`` element after ``MustBeFresh`` (before ``Nonce``)
  + Add optional ``HopLimit`` element
  + Add optional ``ApplicationParameters`` element
  + Define a new specification for Signed Interest using two new elements: ``InterestSignatureInfo`` and ``InterestSignatureValue``

- **Data**

  + Make ``MetaInfo`` and ``Content`` elements optional
  + Change semantics of omitted (or set to zero) ``FreshnessPeriod`` element: it cannot be used to satisfy Interests with ``MustBeFresh``

- **Name**

  + Lift restriction on name component types, allowing types in the range 1-65535
  + Correct definition of name URI encoding: disallow unescaped encoding of PLUS (``+``) and allow TILDE (``~``)
  + Add well-known special-use component types:

    - ``ParametersSha256DigestComponent`` (type 2)
    - ``KeywordNameComponent`` (type 32)
    - ``SegmentNameComponent`` (type 50)
    - ``ByteOffsetNameComponent`` (type 52)
    - ``VersionNameComponent`` (type 54)
    - ``TimestampNameComponent`` (type 56)
    - ``SequenceNumNameComponent`` (type 58)

- **Signature**

  + Require all compliant implementations to support the ``SignatureSha256WithEcdsa`` signature type using NIST curve P-256
  + Redefine the signed portion of Data packets to be more future-proof

Version 0.2.1
-------------

- Add definition of Link Object

- **Interest**

  + Add default of leftmost child if ChildSelector element not present
  + Add specification of ForwardingHint element

- **Data**

  + Updated Content Store semantics for Data packets that do not carry FreshnessPeriod.

Version 0.2
-----------

- **Name**

  + Allow zero-length name component
  + Require implicit digest to be specified using ``ImplicitSha256Digest`` name component

- **Signature**

  + Add spec for ``SignatureHmacWithSha256``

- **Interest**

  + Delete deprecated ``Scope`` guider
  + Restrict Interest to have name with at least one name component

- **Data**

  + Redirect ContentType number assignments to the `wiki page <https://redmine.named-data.net/projects/ndn-tlv/wiki/ContentType>`__

- **TLV-TYPE**

  + Reserve 800-1000 range for link protocol

Version 0.1.1
-------------

- **Signature**

  + New ``SignatureSha256WithEcdsa`` signature type for Elliptic Curve Digital Signature Algorithm (ECDSA).
  + ``KeyLocatorDigest`` renamed to ``KeyDigest``.  The specification now explicitly allows KeyDigest to be a SHA256 of any type of the key.
  + ``KeyLocator`` element is now defined to be optionally present in generic ``SignatureInfo`` element.
    ``SignatureSha256WithRsa`` and ``SignatureSha256WithEcdsa`` still require ``KeyLocator`` to be always present.

Version 0.1
-----------

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
  + ``KeyLocator`` is moved to be inside the ``Signature`` (``SignatureInfo``) element
  + Three content types, ENCR, GONE, and NACK are removed
  + ``FreshnessSeconds`` is renamed to ``FreshnessPeriod`` and is expressed in units of milliseconds

- **Signature**

  + ``Signature`` is moved to the end of Data packet.
  + ``KeyLocator`` is moved to be a part of the ``SignatureInfo`` element, if it is applicable for the specific signature type.

    The rationale for the move is to make Signature (sequence of ``SignatureInfo`` and ``SignatureValue`` TLVs) self-contained and self-sufficient.

  + Signature type (or signing method information) is expressed as an assigned integer value (with no assumed default), rather than OID.
  + Added support for hash-only "signature"
  + The current specification does not define Merkle Hash Tree Aggregated Signatures, but it is expected that such (or similar) signatures will be defined in future version of this specification
