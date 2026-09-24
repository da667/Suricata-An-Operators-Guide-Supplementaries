# Purpose of this directory:

SSLproxy is very complex software, that requires a lot of scaffolding to work right. To help aid in that, in this directory I have two files:
 - `sslproxy.conf`
 - `sslproxy.service`
 
 `sslproxy.conf` is a configuration file to use with sslproxy's -f option to define how it operates. This configuration file has the following settings:
  
  - Enables daemon mode. That means no debug logs unless daemon mode is disabled. But also means its ready for systemd service integration
  - Does NOT enable divert mode, but instead operates in split/mirror mode. We want Suricata to sit passively on the mirror interface and sniff network traffic.
  - To that effect, the `MirrorIf` directive is set to mirror traffic to interface ens20. If you plan on mirroring decrypted TLS traffic from the SSLProxy software to a different interface name, you will need to change this line.
  - There is an HTTPS proxyspec configured to generate a connection log, and a decrypted pcap. The HTTPS Proxyspec configures the listener for SSLProxy for the IP address `10.0.30.5` and the port `8443`. If you plan on utilizing a different IP address or port for the SSLProxy service, the HTTPS proxyspec will need to be modified.
  - As mentioned in *Suricata: An Operator's Guide*, SSLProxy relies on being somewhere in the path between the client and the server. In our lab environment, we have the SSLProxy system acting as a router. This means you'll need sysctl tunables `net.ipv4.ip_forward`, and `'net.ipv4.ip_nonlocal_bind` enabled. Additionally, you'll need an `iptables` NAT PREROUTING rule to direct traffic from port 443 to port 8443, or whatever port you have configured for the SSLProxy service to listen on. 
  
 `sslproxy.service` is a systemd service file with the following settings:
  
   - Sets up sslproxy as a forking service
   - Has an `ExecStartPre` line that configures ens20 as an interface with ARP and Multicast disabled, meaning that network connectivity on this interface is effectively disabled entirely. Its only purpose is to serve as a destination to mirror network traffic from the SSLProxy service. If you need to change the interface name (default interface name is `ens20`), or ensure that the network interface is available for network connectivity for some weird reason, you'll need to reconfigure the `ExecStartPre` line.
   - installing the service file is an exercise left to the user. Detailed instructions are available in Chapter 10, section *10.3.2.2*. 