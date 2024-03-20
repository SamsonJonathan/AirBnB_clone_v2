#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static
# 	Install Nginx if it not already installed
#	Create the folder /data/ if it doesn’t already exist
# 	Create the folder /data/web_static/ if it doesn’t already exist
# 	Create the folder /data/web_static/releases/ if it doesn’t already exist
#	Create the folder /data/web_static/shared/ if it doesn’t already exist
# 	Create the folder /data/web_static/releases/test/ if it doesn’t already exist
# 	Create a fake HTML file /data/web_static/releases/test/index.html (with simple content, to test your Nginx configuration)
# 	Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder. If the symbolic link already exists, it should be deleted and recreated every time the script is ran.
# 	Give ownership of the /data/ folder to the ubuntu user AND group (you can assume this user and group exist). This should be recursive; everything inside should be created/owned by this user/group.
# 	Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_stati (ex: https://mydmainame.ch/hbb_satic).Dn’t orgetto restart Nginx after updating the confcontent of iguration:

ADD_HBNBSTATIC="\\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n"
TEST_HTML="
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"

sudo apt-get -y update
sudo apt-get -y install nginx
sudo mkdir -p /data/ /data/web_static/ /data/web_static/releases/ /data/web_static/shared/ /data/web_static/releases/test/

echo "$TEST_HTML" | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -hR ubuntu:ubuntu /data/
sudo sed -i "41i $ADD_HBNBSTATIC" /etc/nginx/sites-available/default
sudo service nginx restart
