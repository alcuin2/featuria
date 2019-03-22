from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABckglQVk4KBGh5lHjmqsS2KtMHItBlR-oNt-G55MUDPwvOKcR85xRivj8zqTf99vU6W5yqEOj5YgPz5HXtb7ugkAtL8d0177CyGpnOKofqgkFWfB5JT1Q97VUNXsY3RMnlHyhSHgr0loisamunDAoP37qoJEmmDgCYss2lfJVz7xQZBt7Xb7WT-Byz9XuHDh9PUjae'


def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
