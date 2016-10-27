Introduction
------------

This version of specification aims to describe the NDN packet format only, a much narrower scope than a full NDN protocol specification.
Full protocol specification will be published as a separate document.  For more information about the overall protocol refer to `"Named Data Networking" by Lixia Zhang, Alexander Afanasyev, Jeffrey Burke, Van Jacobson, kc claffy, Patrick Crowley, Christos Papadopoulos, Lan Wang, and Beichuan Zhang, ACM SIGCOMM Computer Communication Review (CCR), July 2014 <https://named-data.net/publications/named_data_networking_ccr/>`__ and other publications on `Named Data Networking website <https://named-data.net>`__.

In addition to the packet format and full protocol specification, we have published a set of technical memos and papers that explain the reasoning behind the design choices:

- `NDN Protocol Design Principles <https://named-data.net/project/ndn-design-principles/>`__

- `"Packet Fragmentation in NDN: Why NDN Uses Hop-By-Hop Fragmentation (NDN Memo)" by A. Afanasyev, J. Shi, L. Wang, B. Zhang, and L. Zhang., NDN Memo, Technical Report NDN-0032 <http://named-data.net/publications/techreports/ndn-0032-1-ndn-memo-fragmentation/>`__

- `"SNAMP: Secure Namespace Mapping to Scale NDN Forwarding" by Alexander Afanasyev, Cheng Yi, Lan Wang, Beichuan Zhang, and Lixia Zhang, 18th IEEE Global Internet Symposium, April 2015 <http://named-data.net/publications/snamp-ndn-scalability/>`__

- `"NDN Technical Memo: Naming Conventions" by NDN Project Team. NDN, Technical Report NDN-0022 <http://named-data.net/publications/techreports/ndn-tr-22-ndn-memo-naming-conventions/>`__

Acknowledgment
--------------

This NDN packet format specification is evolution of the `CCNx 0.7.2 specification <https://github.com/named-data/ndnx/releases/tag/ccnx-0.7.2-ndn-1>`__ as of May 2013.
