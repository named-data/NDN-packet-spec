.. _name:

Name
----

An NDN Name is a hierarchical name for NDN content, which contains a sequence of name components.  

NDN Name Format
~~~~~~~~~~~~~~~

We use a 2-level nested TLV to represent a name.
The Type in the outer TLV indicates this is a Name.
All inner TLVs have the same Type indicating that they each contain a name component.
There is no restriction on the Value field in a name component and it may not contain any bytes::

    Name ::= NAME-TYPE TLV-LENGTH NameComponent*
    NameComponent ::= NAME-COMPONENT-TYPE TLV-LENGTH BYTE+

.. % 0 or many name components in name
.. % 0 or many bytes in name component


NDN URI Scheme
~~~~~~~~~~~~~~

For textual representation, it is often convenient to use URI to represent NDN names.
Please refer to RFC 3986 (URI Generic Syntax) for background.

- The scheme identifier is ``ndn``. 

- When producing a URI from an NDN Name, only the generic URI unreserved characters are left unescaped. 
  These are the US-ASCII upper and lower case letters (A-Z, a-z), digits (0-9), and the four specials PLUS (+), PERIOD (.), UNDERSCORE (\_), and HYPHEN (-). 
  All other characters are escaped using either the percent-encoding method of the URI Generic Syntax or a ``ndn`` scheme specific hexadecimal string escape starting with the EQUALS (=) and an even number of characters from the set of hex digits.
  Once an EQUALS has been encountered in a component the hexadecimal encoding persists until the end of the component.
  The hex digits in these escaped encodings should always use upper-case letters, i.e., A-Z.

- To unambiguously represent name components that would collide with the use of . and .. for relative URIs, any component that consists solely of zero or more periods is encoded using three additional periods.

- The authority component (the part after the initial ``//`` in the familiar http and ftp URI schemes) is not relevant to NDN.
  It should not be present, and it is ignored if it is present. 

Implicit Digest Component
~~~~~~~~~~~~~~~~~~~~~~~~~

The Name of every piece of content includes as its final component a derived digest that ultimately makes the name unique.
This digest may occur in an Interest Name as an ordinary Component (the last one in the name).
This final component in the name is never included explicitly in the Data packet when it is transmitted on the wire.
It can be computed by any node based on the Data packet content.

The **implicit digest component** consists of the SHA-256 digest of the entire Data packet without the signature component.  Having this digest as the last name component enables us to achieve the following two goals:

- Identify one specific Data packet and no other. 

- Exclude a specific Data packet in an Interest (independent from whether it has a valid signature).

Canonical Order
~~~~~~~~~~~~~~~

In several contexts in NDN packet processing, it is useful to have a consistent ordering of names and name components. NDN names consist of a sequence of NameComponents, and each NameComponent is a sequence of zero or more 8-bit bytes. The ordering for components is such that:

- If *a* is shorter than *b* (i.e., has fewer bytes), then *a* comes before *b*.

- If *a* and *b* have the same length, then they are compared in ASCII lexicographic order (e.g., ordering based on memcmp() operation.)


For Names, the ordering is just based on the ordering of the first component where they differ.
If one name is a proper prefix of the other, then it comes first.

Changes from CCNx
~~~~~~~~~~~~~~~~~

- The name encoding is changed from binary XML to TLV format.

- The discussions on naming conventions and the use of special markers inside NameComponents are removed from packet specification, and will be covered by a separate technical document

.. (\cite{NamingConvention}).

- Deprecated zero-length name component.
