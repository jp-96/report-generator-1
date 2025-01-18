# Use the base image from ghcr.io/unoconv/unoserver-docker
FROM ghcr.io/unoconv/unoserver-docker

# Add custom fonts, copy and set up the font script, and run it as root
USER root
ADD unoserver/customfonts /usr/local/customfonts
COPY unoserver/customfonts/install_fonts.sh /usr/local/bin/install_fonts.sh
RUN chmod +x /usr/local/bin/install_fonts.sh
RUN /usr/local/bin/install_fonts.sh

# Switch back to the worker user
USER worker

# # Install Japanese fonts
# # ###################################
# #   IPA FONT LICENSE AGREEMENT V1.0
# # https://moji.or.jp/ipafont/license/
# # ###################################
# RUN mkdir -p ~/.local/share/fonts
# RUN cd /usr/local/customfonts/archiveipa \
# 	# IPAmj Mincho Font
#     && unzip ipamjm00601.zip -d ~/.local/share/fonts/ipamjm00601 \
#     # IPAex Font（2 fonts）
#     && unzip IPAexfont00401.zip -d ~/.local/share/fonts/IPAexfont00401 \
#     # IPA Font（4 fonts）
#     && unzip IPAfont00303.zip -d ~/.local/share/fonts/IPAfont00303 \
#     # Build font information cache files
#     && fc-cache -vf
