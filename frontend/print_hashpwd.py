from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


if __name__ == "__main__":
    print(pwd_context.hash("123123123"))