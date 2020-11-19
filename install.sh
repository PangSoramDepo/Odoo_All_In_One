apt-get update

apt-get install -y git python3.7 postgresql nano virtualenv xz-utils wget fontconfig libfreetype6 libx11-6 libxext6 libxrender1 xfonts-75dpi

wget -O wkhtmltox.tar.xz \https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
tar xvf wkhtmltox.tar.xz
mv wkhtmltox/lib/* /usr/local/lib/
mv wkhtmltox/bin/* /usr/local/bin/
mv wkhtmltox/share/man/man1 /usr/local/share/man/

apt-get install -y gcc libxml2-dev \libxslt1-dev libevent-dev libsasl2-dev libssl1.0-dev libldap2-dev \libpq-dev libpng-dev libjpeg-dev

service postgresql start
sudo -u postgres createuser --createdb $(whoami)
createdb $(whoami)

git config --global user.name "pangsoramdepo"
git config --global user.email pangsoramdepo@gmail.com

mkdir ~/odoo-dev
cd ~/odoo-dev
git clone -b 12.0 --single-branch --depth 1 https://github.com/odoo/odoo.git
cd odoo

virtualenv -p python3 ~/odoo-12.0
source ~/odoo-12.0/bin/activate

pip3 install -r requirements.txt

createdb odoo-test
python3 odoo-bin -d odoo-test --addons-path=addons \--db-filter=odoo-test -i base
