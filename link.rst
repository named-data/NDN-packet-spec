.. _link:

Link Object
-----------

The Link Object is a specialized form of a :ref:`Data packet <data>` packet, defined as follows::

    LinkObject ::= DATA-TLV TLV-LENGTH
                     Name
                     MetaInfo (.ContentType = LINK)
                     LinkContent
                     Signature

    LinkContent ::= CONTENT-TYPE TLV-LENGTH
                      Delegation+

    Delegation ::= LINK-DELEGATION-TYPE TLV-LENGTH
                     Preference
                     Name

    Preference ::= LINK-PREFERENCE-TYPE TLV-LENGTH
                     nonNegativeInteger


Link Object is a data packet, whose content contains a list of one or more name delegations: a pair of name and the associate priority.
The semantical meaning of the delegations depends on the specific use.  For example, when LinkObject is used as part of Interest packet, each delegation implies that the requested Data packet can be retrieved by forwarding the interest along the delegation path.  Specifics of the forwarding logic for Interests with ``LinkObject`` will be defined in a separated document.

The list of delegations in ``LinkContent`` SHOULD be ordered by preference value in ascending order (i.e., the lowest value first).

In a LinkContent, each Delegation SHOULD have a distinct Name.


..
   Let’s assume that we have files that are published under /net/ndnsim, but are hosted under /att/user/alex/net/ndnsim and /verizon/user/alex/net/ndnsim. The structure of the Link would be the following:


   +-----------------+---------------------------------------------+--------------------------------------------------------------+
   | Link Field      | Value                                       | Description of the value                                     |
   +=================+=============================================+==============================================================+
   | Name            | /net/ndnsim/LINK                            | Name of the link (as a convention, the last NameComponent    |
   |                 |                                             | MAY be "LINK")                                               |
   +-----------------+---------------------------------------------+--------------------------------------------------------------+
   | MetaInfo        | ContentType = LINK                          | Field that identifies the actual data content                |
   +-----------------+---------------------------------------------+--------------------------------------------------------------+
   | Content         | (/verizon/user/alex/net/ndnsim, 10)         | Content in the form of (alias, preference) pairs             |
   |                 | (/att/user/alex/net/ndnsim, 100)            |                                                              |
   +-----------------+---------------------------------------------+--------------------------------------------------------------+
   | Signature       | Varying                                     | Signed by the publisher of the Link                          |
   +-----------------+---------------------------------------------+--------------------------------------------------------------+
