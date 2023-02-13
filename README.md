# Network Testing Framework &nbsp;

Первый наш сетевой фреймворк. Скрипт преднозначен для blue teaming-а. Каждый может отправить pull request внеся свои идеи в этот скрипт и стать частью создателей этого фреймворка !

## Установка на Linux/Debian
```
sudo apt install git
git clone https://github.com/cyberdome-tj/nt_framework
cd nt_framework
sudo bash install.sh
sudo ntf
```
# Installation on MacOS 
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install git
git clone https://github.com/cyberdome-tj/nt_framework
brew install acrogenesis/macchanger/macchanger
brew install python arp-scan figlet neofetch systemc
cd nt_framework
sudo pip3 install -r requirements.txt
sudo python3 ntf.py
```
# Команды:
<ul>
   <li> <a href="https://itigic.com/ru/what-is-whois-and-what-is-it-for/">whois</a> - поиск информации о домене (включая .tj из сайта <a href="http://www.nic.tj/whois.html">nic.tj</a>)</li>
   <li>publip - показать публичный IP адрес устройства из <a href="https://icanhazip.com">icanhazip</a></li>
   <li>ping - проверить соединение домена. Отправляет 3 заросов ICMP</li>
   <li>tor - включить TOR сервис</li>
   <li>mac - изменить MAC адрес интерфейса. (ens33, wlan0 и другие)</li>
   <li>devices - искать доступные устройства LAN через ARP протокол</li>
   <li>scap - отсканировать все открытые порты устройств по LAN через ARP протокол</li>
   <li>info - показать полную информацию о ПК с помощью <a href="https://github.com/dylanaraps/neofetch">neofetch</a></li>
   <li>back - вернуться назад </li>
   <li>banner - показать баннер</li>
   <li>exit - выйти</li>
</ul>

# Стандартные команды:

<ul>
 <li>ifconfig - показать сетевые интерфейсы 
 <li>clear - очистка терминала 
 <li>ls - показать текущую директорию
</ul>

# Дополнительные функции скрипта :

<ul>
 <li>Дополнение слов через клавишу <code>TAB</code> 
 <li>Поддержка истории команд
 <li>Очистка истории команд и выключение TOR соединение после выхода.
</ul>

# Скриншот
<kbd>
   <img src="https://user-images.githubusercontent.com/109206637/218330244-6067987b-b398-405e-ae94-6bef6f13cf74.png">
</kbd>
<br>

# Наша команда
<ul>
<li><a href="https://github.com/tr34x0r">tr34x0r</a></li>
<li><a href="https://github.com/r3x08">r3x08</a></li>
</ul>

<a href="https://github.com/cyberdome-tj"><img src="https://img.shields.io/badge/Made%20with%20%E2%99%A5%20%20by -CyberDome-black"></a>
