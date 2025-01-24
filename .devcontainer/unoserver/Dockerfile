# Use the base image from ghcr.io/unoconv/unoserver-docker
FROM ghcr.io/unoconv/unoserver-docker

# As root
USER root

# Install custom fonts
ADD unoserver/customfonts /usr/local/customfonts
WORKDIR /usr/local/customfonts

# Install Japanese fonts
# ###################################
#   IPA FONT LICENSE AGREEMENT V1.0
# https://moji.or.jp/ipafont/license/
# ###################################
RUN cd archiveipa \
    # Install folder
    && mkdir -p /usr/share/fonts/ipa \
	# IPAmj Mincho Font
    && unzip ipamjm00601.zip -d /usr/share/fonts/ipa/ipamjm0601 \
    # IPAex Font（2 fonts）
    && unzip IPAexfont00401.zip -d /usr/share/fonts/ipa/ipaexfont00401 \
    # IPA Font（4 fonts）
    && unzip IPAfont00303.zip -d /usr/share/fonts/ipa/ipafont00303 \
    # Build font information cache files
    && fc-cache -vf

# As worker
USER ${UID}
