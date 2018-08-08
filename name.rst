.. _Name:

Name
----

An NDN Name is a hierarchical name for NDN content, which contains a sequence of name components.

NDN Name Format
~~~~~~~~~~~~~~~

We use a 2-level nested TLV to represent a name.
The NAME-TYPE in the outer TLV indicates this is a Name.
Inner TLVs should be ``NameComponent`` elements, as defined in the following:

::

    Name ::= NAME-TYPE TLV-LENGTH NameComponent*

    NameComponent ::= GenericNameComponent |
                      ImplicitSha256DigestComponent |
                      ParametersSha256DigestComponent |
                      OtherTypeComponent

    GenericNameComponent ::= NAME-COMPONENT-TYPE TLV-LENGTH
                               BYTE*

    ImplicitSha256DigestComponent ::= IMPLICIT-SHA256-DIGEST-COMPONENT-TYPE TLV-LENGTH(=32)
                                        BYTE{32}

    ParametersSha256DigestComponent ::= PARAMETERS-SHA256-DIGEST-COMPONENT-TYPE TLV-LENGTH(=32)
                                          BYTE{32}

    OtherTypeComponent ::= OTHER-TYPE-COMPONENT-TYPE TLV-LENGTH
                             BYTE*

    OTHER-TYPE-COMPONENT-TYPE ::= number in the range 3-65535 inclusive except 8

- ``GenericNameComponent`` is a generic name component, without any restrictions on the content of the value.

- ``ImplicitSha256DigestComponent`` is an implicit SHA-256 digest component and it is required to contain a value of 32 octets.

- ``ParametersSha256DigestComponent`` is a component carrying the SHA-256 digest of Interest parameters and it is required to contain a value of 32 octets.

In addition to the above component types, ``Name`` can include other component types governed by `Name Component Assignment policy <https://redmine.named-data.net/projects/ndn-tlv/wiki/NameComponentType>`__.

TLV-TYPE of name component MUST be in the range ``1-65535`` (inclusive).
``Name`` element containing a sub-element out of this range is invalid and the packet SHOULD be dropped.
This requirement overrides the TLV evolvability guidelines.

Name component with TLV-TYPE ``0`` (zero) is reserved to indicate an invalid name component.

NDN URI Scheme
~~~~~~~~~~~~~~

For textual representation, it is often convenient to use URI to represent NDN names.
Please refer to RFC 3986 (URI Generic Syntax) for background.

The scheme identifier is ``ndn``.

The authority component (the part after the initial ``//`` in the familiar http and ftp URI schemes) is irrelevant to NDN.
It should not be present, and it is ignored if it is present.

Each name component is represented as ``<type-number>=<escaped-value>``, where:

- ``<type-number>`` is the component's TLV-TYPE in decimal format without leading zeros.

- ``<escaped-value>`` is the component's TLV-VALUE escaped according to the following rules:

  * Generic URI unreserved characters are left unescaped.
    These are the US-ASCII upper and lower case letters (A-Z, a-z), digits (0-9), and the four specials HYPHEN (-), PERIOD (.), UNDERSCORE (\_), and TILDE (~).
  * All other characters are escaped using the percent-encoding method of the URI Generic Syntax.
  * To unambiguously represent name components that would collide with the use of . and .. for relative URIs, any component that consists solely of zero or more periods is encoded using three additional periods.

For example, ``42=Hello%20world`` represents a name component of TLV-TYPE 42 and TLV-VALUE "Hello world".

Name components of the following types have alternate URI representations for better readability:

- ``GenericNameComponent`` can have its ``<type-number>=`` prefix omitted.

  For example, ``Hello%20world`` is equivalent to ``8=Hello%20world``.

- ``ImplicitSha256DigestComponent`` can be represented as ``sha256digest=<hex-value>``.
  ``ParametersSha256DigestComponent`` can be represented as ``params-sha256=<hex-value>``.

  * The ``sha256digest=`` and ``params-sha256=`` prefixes are case sensitive.
  * ``<hex-value>`` is the TLV-VALUE represented as a sequence of 64 hexadecimal digits.
    Both lower-case and upper-case letters are acceptable, but lower-case is preferred.

  For example, ``sha256digest=893259d98aca58c451453f29ec7dc38688e690dd0b59ef4f3b9d33738bff0b8d``, ``params-sha256=893259d98aca58c451453f29ec7dc38688e690dd0b59ef4f3b9d33738bff0b8d``

- Other component types may define alternate URI representations in the form of ``<prefix>=<value>``, where:

  * ``<prefix>`` is a non-empty string that starts with an upper or lower case letter and consists solely of generic URI unreserved characters.
  * ``<value>`` is a string whose interpretation differs according to the prefix.

  Such alternate representations should be defined in `Name Component Assignment policy <https://redmine.named-data.net/projects/ndn-tlv/wiki/NameComponentType>`__.

.. _Implicit Digest Component:

Implicit Digest Component
~~~~~~~~~~~~~~~~~~~~~~~~~

The full name of every Data packet includes a logical final implicit digest component, which makes the name of every Data packet unique.
The implicit digest (``ImplicitSha256DigestComponent``) MAY appear in an Interest as the last component of the Interest name to request a specific Data packet.
``ImplicitSha256DigestComponent`` is never included explicitly in the Data packet when it is transmitted on the wire and, if needed, must be computed by all nodes based on the Data packet content.

The **implicit digest component** consists of the SHA-256 digest of the entire Data packet bits.  Having this digest as the last name component allows identifying one specific Data packet and no other.

.. _Interest Parameters Digest Component:

Parameters Digest Component
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The parameters digest component consists of the SHA-256 digest computed over the type, length, and value of the ``Parameters`` element of an Interest.
This component MUST appear in an Interest name if the Interest contains a ``Parameters`` element.
The position of the component is determined by the application protocol, generally, it should be at the end of the name but before version/segment numbers.

The parameters digest (``ParametersSha256DigestComponent``) provides uniqueness of the Interest name for a given set of parameters and ensures securely that the retrieved Data packet is a response generated against the correct set of parameters.
Producers should recalculate the digest based on the actual ``Parameters`` element in the received Interest and verify that it matches the parameters digest component in the Interest name.

Canonical Order
~~~~~~~~~~~~~~~

In several contexts in NDN packet processing, it is necessary to have a consistent ordering of names and name components.

The order between individual name components is defined as follows:

- If components ``component1`` and ``component2`` have different types, then

  + ``component1`` is less than ``component2`` if numerical value of ``TLV-TYPE(component1)`` is less than numerical value of ``TLV-TYPE(component2)``

    .. note::
        Type number of ``ImplicitSha256DigestComponent`` is guaranteed to be less than type number of any other valid name component.

- If components have the same type, then

    + If *a* is shorter than *b* (i.e., has fewer bytes), then *a* comes before *b*.

    + If *a* and *b* have the same length, then they are compared in lexicographic order based on absolute value of octet values (e.g., ordering based on memcmp() operation.)

For Names, the ordering is just based on the ordering of the first component where they differ.
If one name is a proper prefix of the other, then it comes first.

.. note::
   The canonical order can be enforced by directly comparing the wire encoding of the ``Name`` field's TLV-VALUE (i.e., excluding TLV-TYPE and TLV-LEGNTH of the whole Name TLV)::

       int
       canonicalOrder(Name lhs, Name rhs) {
          int result = memcmp(lhs.value(), rhs.value(), min(lhs.value_size(), rhs.value_size()));
          if (result == 0) {
            result = lhs.value_size() - rhs.value_size();
          }
          return result;
       }
