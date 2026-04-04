from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# $12$SKCIVK3vIS.OklGImi3K0uR7sJ1V54SLfERMrIXQZQss4Y6dpQ1ZG
if __name__ == "__main__":
    print(pwd_context.hash("123123123"))