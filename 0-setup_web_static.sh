#!/usr/bin/env bash
# Bash script to set up web servers for web_static deployment

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create necessary directories if they don't exist
directories=("/data" "/data/web_static" "/data/web_static/releases"
    "/data/web_static/shared" "/data/web_static/releases/test")
for dir in "${directories[@]}"; do
    sudo mkdir -p "$dir"
done

# Create a fake HTML file for testing
echo "<html><head></head><body>Holberton School</body></html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create a symbolic link /data/web_static/current
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Give ownership of /data/ to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_content="location /hbnb_static {\n\talias /data/web_static/current/;\n\tindex index.html;\n}"
sudo sed -i "/^\s*server_name _;/a $config_content" /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart
