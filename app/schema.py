instructions=[
    "SET FOREIGN_KEY_CHECKS=0",
    "DROP TABLE IF EXISTS email;",
    "DROP TABLE IF EXISTS contactos;",
    "DROP TABLE IF EXISTS user;",
    "SET FOREIGN_KEY_CHECKS=1;",
    """
        CREATE TABLE user(
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(250) NOT NULL
        )
    """,
    """
        CREATE TABLE email(
            id INT PRIMARY KEY AUTO_INCREMENT,
            from_email INT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (from_email) REFERENCES user(id)
        )
    """,
    """
        CREATE TABLE contactos(           
            id INT PRIMARY KEY AUTO_INCREMENT,
            id_user INT NOT NULL,
            fullname TEXT NOT NULL,
            phone INT,
            email TEXT NOT NULL,
            FOREIGN KEY (id_user) REFERENCES user(id)
        );
    """
]