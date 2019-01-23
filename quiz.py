from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABcPanKlbYRQJoFqGuPdYc4RXxqIQFqAgv4fEfPts1VwnRvvGdSDE4zyJdKmkObrmb9cjU-Ygzxn9iu-7ClerFjeW9Jn1ycKeDzaWeKEXJpZVySudd9KPGH0Ldr8NP-pgjVQNJmU2QWK58PFPn2Jcg6xeGPRRxEkdWkNgcDa9D--orBKfbpluDIwoHwpH9Fzmh9UCgF'


def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
