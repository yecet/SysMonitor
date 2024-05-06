import paramiko

def connect_to_server(ip, username, password):
    # Verilen IP adresi, kullanıcı adı ve şifre ile bir SSH bağlantısı kurar.
    # Args:
    #     ip (str): Bağlanılacak sunucunun IP adresi.
    #     username (str): SSH bağlantısı için kullanılacak kullanıcı adı.
    #     password (str): SSH bağlantısı için kullanılacak şifre.
    # Returns:
    #     paramiko.SSHClient: Başarılı bir bağlantı durumunda SSH istemcisini döndürür.
    #                         Bağlantı başarısız olduğunda None döndürür.
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=username, password=password)
    return ssh

def execute_command(ssh, command):
    # Verilen SSH bağlantısı üzerinde belirtilen komutu çalıştırır ve çıktıyı döndürür.
    #
    # Args:
    #     ssh (paramiko.SSHClient): Komutun çalıştırılacağı SSH istemcisi.
    #     command (str): Çalıştırılacak komut.
    #
    # Returns:
    #     str: Komutun çıktısı (stdout).
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode()

def main():
    commands = [
        # /etc/passwd dosyasını görüntüler
        "cat /etc/passwd",
        # /etc/group dosyasını görüntüler
        "cat /etc/group",
        # Sudo yetkilendirme dosyasını görüntüler
        "cat /etc/sudoers",
        # Sistem ne kadar süredir çalışıyor (uptime)
        "uptime",
        # Bellek bilgilerini görüntüler
        "cat /proc/meminfo",
        # Tüm çalışan süreçleri listeler
        "ps aux",
        # DNS yapılandırma dosyasını görüntüler
        "cat /etc/resolv.conf",
        # Hosts dosyasını görüntüler
        "cat /etc/hosts",
        # Iptables kurallarını listeler
        "iptables -L -v -n",
        # Ağ arabirimlerini ve IP adreslerini listeler
        "ip a",
        # Ağ bağlantılarını ve bağlantı noktalarını listeler
        "netstat -nap",
        # ARP önbelleğini listeler
        "arp -a",
        # PATH ortam değişkenini görüntüler
        "echo $PATH",
        # Son kullanıcı oturumlarını görüntüler
        "lastlog"

    ]
# cred_list.txt dosyasını okuyarak her bir satırda belirtilen sunuculara SSH bağlantısı kurar ve
# belirlenen komutları çalıştırır. Bağlantı kurulduktan sonra her komut için çıktıyı ekrana yazdırır
# ve bağlantıyı kapatır. Bağlantı kurarken herhangi bir hata oluşursa bunu bildirir.
    with open(r"\cred_list.txt") as f:
        lines = f.readlines()
        for line in lines:
            IP_address, user, passw = line.strip().split("|")
            print(f"Connecting to {IP_address}...")
            try:
                ssh = connect_to_server(IP_address, user, passw)
                print(f"Connected to {IP_address}.")
                for command in commands:
                    print(f"Running command: {command}")
                    output = execute_command(ssh, command)
                    print(output)
                ssh.close()
                print("Connection closed.")
            except Exception as e:
                print(f"Error connecting to {IP_address}: {str(e)}")
            print("=============")

if __name__ == "__main__":
    main()
