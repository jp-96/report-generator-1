# Use the base image from ghcr.io/unoconv/unoserver-docker
FROM ghcr.io/unoconv/unoserver-docker

# Add custom fonts, copy and set up the font script
USER root
ADD unoserver/customfonts /usr/local/customfonts
COPY unoserver/customfonts/setup_asroot.sh /usr/local/bin/setup_asroot.sh
RUN chmod +x /usr/local/bin/setup_asroot.sh
COPY unoserver/customfonts/setup_asworker.sh /usr/local/bin/setup_asworker.sh
RUN chmod +x /usr/local/bin/setup_asworker.sh

# Run as root
RUN /usr/local/bin/setup_asroot.sh

# Run as worker
USER worker
RUN /usr/local/bin/setup_asworker.sh
