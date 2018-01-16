.. _Name:

Name
----

An NDN Name is a hierarchical name for NDN content, which contains a sequence of name components.

NDN Name Format
~~~~~~~~~~~~~~~

We use a 2-level nested TLV to represent a name.
The Type in the outer TLV indicates this is a Name.
Inner TLVs should be one of ``NameComponent`` blocks, as defined in the following:

::

    Name ::= NAME-TYPE TLV-LENGTH NameComponent*

    NameComponent ::= GenericNameComponent |
                      ImplicitSha256DigestComponent |
                      OtherTypeComponent

    GenericNameComponent ::= NAME-COMPONENT-TYPE TLV-LENGTH
                               BYTE*

    ImplicitSha256DigestComponent ::= IMPLICIT-SHA256-DIGEST-COMPONENT-TYPE TLV-LENGTH(=32)
                                        BYTE{32}

    OtherTypeComponent ::= OTHER-TYPE-COMPONENT-TYPE TLV-LENGTH
                             BYTE*

    OTHER-TYPE-COMPONENT-TYPE ::= number in the range 2-65535 inclusive except 8

- ``GenericNameComponent`` is a generic name component, without any restrictions on the content of the value.

- ``ImplicitSha256DigestComponent`` is an implicit SHA256 digest component and it is required to contain a value of 32 octets.

In addition to two component types, ``Name`` can include other component types governed by `Name Component Assignment policy <https://redmine.named-data.net/projects/ndn-tlv/wiki/NameComponentType>`__.

TLV-TYPE of name component MUST be in the range ``1-65535`` (inclusive).
``Name`` element containing a sub-element out of this range is invalid and the packet SHOULD be dropped.

Name component with TLV-TYPE ``0`` (zero) is reserved to indicate an invalid name component.

NDN URI Scheme
~~~~~~~~~~~~~~

For textual representation, it is often convenient to use URI to represent NDN names.
Please refer to RFC 3986 (URI Generic Syntax) for background.

- The scheme identifier is ``ndn``.

- The authority component (the part after the initial ``//`` in the familiar http and ftp URI schemes) is not relevant to NDN.
  It should not be present, and it is ignored if it is present.

- Component types have the following URI representations:

  * ``GenericNameComponent``

    + When producing a URI from an NDN Name, only the generic URI unreserved characters are left unescaped.
      These are the US-ASCII upper and lower case letters (A-Z, a-z), digits (0-9), and the four specials HYPHEN (-), PERIOD (.), UNDERSCORE (\_), and TILDE (~).
      All other characters are escaped using the percent-encoding method of the URI Generic Syntax.

    + To unambiguously represent name components that would collide with the use of . and .. for relative URIs, any component that consists solely of zero or more periods is encoded using three additional periods.

  * ``ImplicitSha256DigestComponent``

    + Implicit SHA256 digest component starts with ``sha256digest=`` prefix (case sensitive), followed by the digest represented as a sequence of 64 hexadecimal numbers.

      For example, ``sha256digest=893259d98aca58c451453f29ec7dc38688e690dd0b59ef4f3b9d33738bff0b8d``

  * Other component types

    + Start with ``<number>=`` prefix (e.g., ``42=...``), followed by the value encoded in the same way as for ``GenericNameComponent``

.. _Implicit Digest Component:

Implicit Digest Component
~~~~~~~~~~~~~~~~~~~~~~~~~

The full name of every Data packet includes a logical final implicit digest component, which makes the name of every Data packet unique.
The implicit digest (``ImplicitSha256DigestComponent``) MAY appear in an Interest, either as the last component of Interest Name to request a specific Data packet, or in the Exclude selector to exclude specific Data packet(s).
``ImplicitSha256DigestComponent`` is never included explicitly in the Data packet when it is transmitted on the wire and, if needed, must be computed by all nodes based on the Data packet content.

The **implicit digest component** consists of the SHA-256 digest of the entire Data packet bits.  Having this digest as the last name component enables us to achieve the following two goals:

- Identify one specific Data packet and no other.

- Exclude a specific Data packet in an Interest (independent from whether it has a valid signature).

Canonical Order
~~~~~~~~~~~~~~~


In several contexts in NDN packet processing, it is necessary to have a consistent ordering of names and name components.

The order between individual name components is defined as follows:

- If components have different type ``component1`` and ``component2``, then

  + ``component1`` is less than ``component2`` if  numerical value of ``TLV-CODE(component1)`` is less than numerical value of ``TLV-CODE(component2)``

    .. note::
        Type code ``ImplicitSha256DigestComponent`` is guaranteed to be less than type code of any other valid name component.

- If components have the same type, then

    + If *a* is shorter than *b* (i.e., has fewer bytes), then *a* comes before *b*.

    + If *a* and *b* have the same length, then they are compared in lexicographic order based on absolute value of octet values (e.g., ordering based on memcmp() operation.)

For Names, the ordering is just based on the ordering of the first component where they differ.
If one name is a proper prefix of the other, then it comes first.

.. note::
   The canonical order can be enforced by directly comparing the wire encoding of the ``Name`` field's TLV-VALUE (i.e., excluding TLV-TYPE and TLV-LEGNTH of the whole Name TLV)::

       int
       canonicalOrder(Name lhs, Name rhs) {
          int result = memcmp(lhs.value(), rhs.value(), min(lhs.value_size(), rhs.value_size());
          if (result == 0) {
            result = lhs.value_size() - rhs.value_size();
          }
          return result;
       }
