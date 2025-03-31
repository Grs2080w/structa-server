from dotenv import dotenv_values

config = {
    **dotenv_values(".env"),  # load shared development variables
}
